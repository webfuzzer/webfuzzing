import requests

'''
# fuzzing url
lambda url : http://fuzzingtest.org
# fuzzing request data
lambda **args : {'data':{'pay1':'" or 1=1 -- "'}, 'headers':{'Content-Type':'application/json'}, 'cookies':{'pay1': '" or 1=1 -- "'}}

```py
>>> r = get_req('https://www.google.com', params = {'params1':'test1'})
>>>
>>> r
<Response [200]>
>>> r.status_code
200
>> r.url
'https://www.google.com/?params1=test1'
```


'''

get_req = (
    lambda url, **args: requests.get(url, **args)
    # http request method get
)
put_req = (
    lambda url, **args: requests.put(url, **args)
    # http request method put
)
post_req = (
    lambda url, **args: requests.post(url, **args)
    # http request method post
)
head_req = (
    lambda url, **args: requests.head(url, **args)
    # http request method head
)
sess_req = (
    lambda: requests.session()
    # http request sessions
)