'''
__init__.py => 모듈화 하기 위한 파일
request.py => static, dynamic 2가지의 요청을 처리하기 위한 모듈
parsing.py => request.py 모듈을 import 하여 요청, 응답을 가지고 크롤링 처리
api.py => parsing.py 모듈을 import 하여 크롤링된 값을 가지고 시각화 처리(__str__ 등 이쁘게)
'''
from api import *
from parsing import *
from request import *