'''
지번주소를 알아옴
샘플
http://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDE3MTAzMDE4MDMwMjEwNzQ0NjA=&currentPage=1&countPerPage=10&resultType=xml&keyword=%EB%82%A8%EC%82%B0%ED%83%80%EC%9A%B4
'''

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup

import xmltodict
import json

from urllib import parse

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

Url = 'http://www.juso.go.kr/addrlink/addrLinkApi.do?'
confmKey='U01TX0FVVEgyMDE3MTAzMDE4MDMwMjEwNzQ0NjA='
currentPage='1'
countPerPage='10'
resultType='xml'
keyword='래미안 이문2차 101동 101호'
print(keyword)
keyword = parse.quote(keyword)
Url+= 'confmKey='+confmKey + '&currentPage='+ currentPage + '&countPerPage='+ countPerPage + '&resultType='+ resultType + '&keyword='+ keyword

# 출력 파일 명
#OUTPUT_FILE_NAME = 'output.xml'
#OUTPUT_FILE_NAME = 'output.txt'
OUTPUT_FILE_NAME = 'detail.json'


def getDetail(url):
    #print(url)
    request = Request(url)
    res_body = (urlopen(request).read())
    rp_dict = xmltodict.parse(res_body)
    rp_json = json.dumps(rp_dict, ensure_ascii=False, indent=4, cls=DecimalEncoder)
    
    #print(rp_json)
	
    soup = BeautifulSoup(res_body, 'xml')
	
    jusos = soup.findAll('juso')
    result = jusos[0].admCd.string[0:5], jusos[0].admCd.string[5:10], jusos[0].lnbrMnnm.string, jusos[0].lnbrSlno.string, jusos[0].roadAddr.string, jusos[0].jibunAddr.string
    return result
    #print(items)
#    for juso in jusos:
#        result = [juso.roadAddr.string, juso.jibunAddr.string, juso.lnbrMnnm.string, juso.lnbrSlno.string]
#        print(result.string)

ret = getDetail(Url)		
print(ret)

getDetail(Url)

