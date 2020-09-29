# Nhận dạng thực thể tiếng Việt


```python
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

data = pd.read_csv('Vnexpress_word.csv', encoding = "ISO-8859-1")
data = data.head(90000)
data = data.drop('Sentence #', axis=1)
#data.groupby('nerLabel').size().reset_index(name='count')
len(data)
```




    90000



### Đếm số lượng nhãn xuất hiện


```python
data.groupby('nerLabel').size().reset_index(name='count')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>nerLabel</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>B-LOC</td>
      <td>1987</td>
    </tr>
    <tr>
      <td>1</td>
      <td>B-MISC</td>
      <td>69</td>
    </tr>
    <tr>
      <td>2</td>
      <td>B-ORG</td>
      <td>1111</td>
    </tr>
    <tr>
      <td>3</td>
      <td>B-PER</td>
      <td>1328</td>
    </tr>
    <tr>
      <td>4</td>
      <td>I-LOC</td>
      <td>499</td>
    </tr>
    <tr>
      <td>5</td>
      <td>I-MISC</td>
      <td>66</td>
    </tr>
    <tr>
      <td>6</td>
      <td>I-ORG</td>
      <td>1284</td>
    </tr>
    <tr>
      <td>7</td>
      <td>I-PER</td>
      <td>58</td>
    </tr>
    <tr>
      <td>8</td>
      <td>O</td>
      <td>83598</td>
    </tr>
  </tbody>
</table>
</div>



### Kiểm tra dữ liệu trống


```python
data.isnull().sum()
```




    index       0
    form        1
    posTag      0
    nerLabel    0
    dtype: int64




```python
data = data.fillna(method='ffill')
data['index'].nunique()
```




    3485



### Phân chia dữ liệu để huấn và kiểm tra


```python
X = data.drop('nerLabel', axis=1)
V = DictVectorizer(sparse=False)
X = V.fit_transform(X.to_dict('record'))
Y =  data.nerLabel.values

classes = np.unique(Y)
classes = classes.tolist()


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.333, random_state=0)
X_train.shape, Y_train.shape
```




    ((60030, 10127), (60030,))




```python
per = Perceptron(verbose=10, n_jobs=-1, max_iter=5)
per.partial_fit(X_train, Y_train, classes)
# np.isnan(X_train.any())
```

    [Parallel(n_jobs=-1)]: Using backend ThreadingBackend with 8 concurrent workers.


    -- Epoch 1
    -- Epoch 1
    -- Epoch 1-- Epoch 1
    -- Epoch 1
    -- Epoch 1
    -- Epoch 1
    
    -- Epoch 1
    Norm: 1348.24, NNZs: 67, Bias: 6.000000, T: 60030, Avg. loss: 2715.067150
    Total training time: 1.78 seconds.
    -- Epoch 1
    Norm: 387.66, NNZs: 99, Bias: -12.000000, T: 60030, Avg. loss: 3375.390871
    Total training time: 1.79 seconds.
    Norm: 1992.44, NNZs: 454, Bias: -37.000000, T: 60030, Avg. loss: 24530.093803
    Total training time: 1.80 seconds.
    Norm: 165.53, NNZs: 74, Bias: 11.000000, T: 60030, Avg. loss: 2661.931034
    Total training time: 1.80 seconds.
    Norm: 936.53, NNZs: 704, Bias: -17.000000, T: 60030, Avg. loss: 49599.206847
    Total training time: 1.81 seconds.
    Norm: 2652.21, NNZs: 1073, Bias: -12.000000, T: 60030, Avg. loss: 59690.696485
    Total training time: 1.81 seconds.
    Norm: 2802.95, NNZs: 1138, Bias: -15.000000, T: 60030, Avg. loss: 88348.412694
    Total training time: 1.84 seconds.
    Norm: 1819.86, NNZs: 883, Bias: -84.000000, T: 60030, Avg. loss: 63705.216592
    Total training time: 1.83 seconds.


    [Parallel(n_jobs=-1)]: Done   2 out of   9 | elapsed:    1.8s remaining:    6.5s
    [Parallel(n_jobs=-1)]: Done   3 out of   9 | elapsed:    1.8s remaining:    3.7s
    [Parallel(n_jobs=-1)]: Done   4 out of   9 | elapsed:    1.9s remaining:    2.3s
    [Parallel(n_jobs=-1)]: Done   5 out of   9 | elapsed:    1.9s remaining:    1.5s
    [Parallel(n_jobs=-1)]: Done   6 out of   9 | elapsed:    1.9s remaining:    0.9s
    [Parallel(n_jobs=-1)]: Done   7 out of   9 | elapsed:    1.9s remaining:    0.5s


    Norm: 3709.91, NNZs: 2971, Bias: 123.000000, T: 60030, Avg. loss: 274519.975029
    Total training time: 1.14 seconds.


    [Parallel(n_jobs=-1)]: Done   9 out of   9 | elapsed:    3.0s remaining:    0.0s
    [Parallel(n_jobs=-1)]: Done   9 out of   9 | elapsed:    3.0s finished





    Perceptron(alpha=0.0001, class_weight=None, early_stopping=False, eta0=1.0,
               fit_intercept=True, max_iter=5, n_iter_no_change=5, n_jobs=-1,
               penalty=None, random_state=0, shuffle=True, tol=0.001,
               validation_fraction=0.1, verbose=10, warm_start=False)



## Xây dựng mô hình phân lớp


```python
new_class = classes.copy()
new_class.pop()
new_class
```




    ['B-LOC', 'B-MISC', 'B-ORG', 'B-PER', 'I-LOC', 'I-MISC', 'I-ORG', 'I-PER']




```python
def report(file, c):
    d = classification_report(y_pred=c.predict(X_test),
                              y_true=Y_test,
                              labels=new_class,
                              output_dict=True)
    print(classification_report(y_pred=c.predict(X_test),
                                y_true=Y_test,
                                labels=new_class))
    clsf_report = pd.DataFrame(d).transpose()
    clsf_report.to_csv("Report/" + file + ".csv", index = True)
```

### 1. Perceptron


```python
report("Perceptron", per)                        
```

    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
      'precision', 'predicted', average, warn_for)
    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
      'precision', 'predicted', average, warn_for)


                  precision    recall  f1-score   support
    
           B-LOC       0.00      0.00      0.00       596
          B-MISC       0.00      0.00      0.00        23
           B-ORG       0.00      0.00      0.00       371
           B-PER       0.00      0.00      0.00       429
           I-LOC       0.00      0.00      0.00       168
          I-MISC       0.00      0.00      0.00        14
           I-ORG       0.00      0.00      0.00       408
           I-PER       0.00      0.00      0.00        16
    
       micro avg       0.00      0.00      0.00      2025
       macro avg       0.00      0.00      0.00      2025
    weighted avg       0.00      0.00      0.00      2025
    


### 2. Stochastic gradient descent


```python
sgd = SGDClassifier()
sgd.partial_fit(X_train, Y_train, classes)
report("SGD", sgd)
```

    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
      'precision', 'predicted', average, warn_for)
    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 due to no predicted samples.
      'precision', 'predicted', average, warn_for)
    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
      'precision', 'predicted', average, warn_for)
    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 due to no predicted samples.
      'precision', 'predicted', average, warn_for)


                  precision    recall  f1-score   support
    
           B-LOC       0.00      0.00      0.00       596
          B-MISC       0.00      0.00      0.00        23
           B-ORG       0.00      0.00      0.00       371
           B-PER       0.00      0.00      0.00       429
           I-LOC       0.00      0.00      0.00       168
          I-MISC       0.00      0.00      0.00        14
           I-ORG       0.00      0.00      0.00       408
           I-PER       0.00      0.00      0.00        16
    
       micro avg       0.00      0.00      0.00      2025
       macro avg       0.00      0.00      0.00      2025
    weighted avg       0.00      0.00      0.00      2025
    


### 3. Naives Bayes


```python
nb = MultinomialNB(alpha=0.01)
nb.partial_fit(X_train, Y_train, classes)
report("Naives Bayes", nb)
```

                  precision    recall  f1-score   support
    
           B-LOC       0.74      0.71      0.73       596
          B-MISC       0.00      0.00      0.00        23
           B-ORG       0.33      0.85      0.48       371
           B-PER       0.56      0.87      0.68       429
           I-LOC       0.59      0.38      0.46       168
          I-MISC       0.03      0.14      0.05        14
           I-ORG       0.52      0.36      0.42       408
           I-PER       0.50      0.31      0.38        16
    
       micro avg       0.48      0.66      0.55      2025
       macro avg       0.41      0.45      0.40      2025
    weighted avg       0.55      0.66      0.57      2025
    


### 4. Passive Aggressive


```python
pa = PassiveAggressiveClassifier()
pa.partial_fit(X_train, Y_train, classes)
report("Passsive Aggressive", pa)

```

    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
      'precision', 'predicted', average, warn_for)
    /opt/anaconda3/lib/python3.7/site-packages/sklearn/metrics/classification.py:1437: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
      'precision', 'predicted', average, warn_for)


                  precision    recall  f1-score   support
    
           B-LOC       0.00      0.00      0.00       596
          B-MISC       0.00      0.00      0.00        23
           B-ORG       1.00      0.00      0.01       371
           B-PER       0.00      0.00      0.00       429
           I-LOC       0.00      0.00      0.00       168
          I-MISC       0.00      0.00      0.00        14
           I-ORG       0.00      0.00      0.00       408
           I-PER       0.00      0.00      0.00        16
    
       micro avg       1.00      0.00      0.00      2025
       macro avg       0.12      0.00      0.00      2025
    weighted avg       0.18      0.00      0.00      2025
    


### 5. Conditional Random Fields


```python
pip install sklearn-crfsuite
```


```python
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from collections import Counter

class SentenceGetter(object):
    
    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
        agg_func = lambda s: [(f, p, n) for f, p, n in zip(s['form'].values.tolist(), 
                                                           s['posTag'].values.tolist(), 
                                                           s['nerLabel'].values.tolist())]
        self.grouped = self.data.groupby('index').apply(agg_func)
        self.sentences = [s for s in self.grouped]
        
    def get_next(self):
        try: 
            s = self.grouped['Sentence: {}'.format(self.n_sent)]
            self.n_sent += 1
            return s 
        except:
            return None

getter = SentenceGetter(data)
sentences = getter.sentences
```


```python
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    
    features = {
        'bias': 1.0, 
        'word.lower()': word.lower(), 
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]
```


```python
X = [sent2features(s) for s in sentences]
y = [sent2labels(s) for s in sentences]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
```


```python
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)

```


```python
y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(y_test, y_pred, labels = new_class))
d = metrics.flat_classification_report(y_test, y_pred, labels = new_class, output_dict=True)
clsf_report = pd.DataFrame(d).transpose()
clsf_report.to_csv("Report/CRFs.csv", index = True)
```
