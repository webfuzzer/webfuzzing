# from base64 import b64encode, b64decode
# from Crawler.DB import Engine

# group = {
#         'first_url':'https://www.google.com',
#         'current_url':'https://www.google.com/test',
#         'body':b64encode('<html></html>'.encode()).decode()
# }


# db = Engine()
# for i in range(1,10):
#     db.add(**group)
# for i in db.fetch():
#     print(i.first_url, i.current_url, b64decode(i.body).decode())

class Utils:
    def __init__(self) -> None:
        print(super.__init__())

class Child(Utils):
    def __init__(self) -> None:
        pass

Utils()