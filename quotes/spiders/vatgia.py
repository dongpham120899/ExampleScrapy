import scrapy


URL = 'https://vatgia.com'
class LazadaSpiders(scrapy.Spider):
    name = 'vatgia'
    url = 'https://vatgia.com/raovat/'
    categoris = [
        '2588/bat-dong-san.html',
        '2603/viec-lam-tuyen-dung.html',
        '1717/dich-vu-giai-tri.html',
        '1527/vien-thong.html,',
        '3254/may-tinh-may-van-phong.html',
        '1528/oto-xe-may.html',
        '7184/do-gia-dung.html',
        '1753/thoi-trang.html',
        '7182/am-thanh-hinh-anh.html',
        '1765/hang-hieu.html',
        '2613/my-pham.html',
        '2748/cong-nghiep-xay-dung.html',
        '3205/noi-ngoai-that.html',
        '1982/du-lich.html',
        '3247/mua-sam.html',
        '1754/me-be.html',
        '7185/giao-duc-dao-tao.html',
        '1763/hoa-qua-tang-my-nghe.html'
    ]

    def start_requests(self):
        for category in self.categoris:
            url = '%s%s' %(self.url, category)

            # for i in range(1,3):
            #     url_ca = '%s/?page=%s' %(url, i)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        list_item = response.css('div.list-post-category')

        for item in list_item.css('div.info-post'):
            try:
                ref = item.css('a::attr(href)').extract_first()
                url = '%s%s' %(URL, ref)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_item
                )
            except:
                print('error')

    def parse_item(self, response):
        title = self.extract_title(response)
        price = self.extract_price(response)
        comments = self.extract_comments(response)

        yield {
            'title': title,
            'price': price,
            'comments': comments
        }

    def extract_title(self, response):
        title = response.css('div.title-price-product h1::text').get()
        return title

    def extract_price(self, response):
        price = response.css('div.title-price-product p.price::text').get()
        return price

    def extract_comments(self, response):
        comments = response.css('div.comment-post')
        for cmt in comments:
            list = comments.css('p.content-cmt-pc::text').extract_first()
            return list

