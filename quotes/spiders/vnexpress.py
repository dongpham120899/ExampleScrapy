import scrapy


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    url = 'https://vnexpress.net/'
    categories = [
        'thoi-su',
        'the-gioi',
        'kinh-doanh',
        'giai-tri',
        'the-thao',
        'phap-luat',
        'giao-duc',
        'suc-khoe',
        'doi-song',
        'du-lich',
        'khoa-hoc',
        'so-hoa',
        'oto-xe-may',
    ]

    def start_requests(self):
        for category in self.categories:
            url = '%s%s' % (self.url, category)

            for i in range(1,2000):
                url_ca = '%s-p%s' % (url, i)
                yield scrapy.Request(url=url_ca, callback=self.parse)

    def parse(self, response):
        list_news = response.css('section.section')

        for news in list_news.css('div.col-left '):
            try:
                # ref chua trang tung bai bao
                ref = news.css('h3 a::attr(href)').extract_first()
                yield scrapy.Request(
                    url=ref,
                    callback=self.parse_news
                )

            except:
                print('Error')

    def parse_news(self, response):

        title = self.get_title(response)
        summary = self.get_summary(response)
        content = self.get_content(response)
        date_time = self.get_date_time(response)
        author = self.get_auhtor(response)
        links = self.get_links_list(response)
        category = self.get_category(response)

        yield {
            'title' : title,
            'summary' : summary,
            'content' : content,
            'date_time' : date_time,
            'author' : author,
            'link' : links,
            'category' : category
        }


    def get_title(self, response):
        title = response.css('h1::text').get()
        return title

    def get_summary(self, response):
        summary = response.css('p.description::text').get()
        return summary

    def get_content(self, response):
        content = response.css('article.fck_detail p::text').getall()
        return content

    def get_date_time(self, response):
        date_time = response.css('span.date::text').get()
        return date_time

    def get_auhtor(self, response):
        author = response.css('p.Normal strong::text').get()
        return author

    def get_links_list(self, response):
        links = response.css('ul.list-news a::text').getall()
        return links

    def get_category(self, response):
        category = response.css('ul.breadcrumb a::text').get()
        return category


