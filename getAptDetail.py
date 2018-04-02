'''
고객의 아파트 주소 정보를 받아서 해당 주소의 면적 및 층수를 리턴
건축물대장 OpenAPI 활용
샘플
http://apis.data.go.kr/1611000/BldRgstService/getBrExposPubuseAreaInfo?serviceKey=49rKGilAY%2FInAVDmv5kRUue6TsvmfpJ6t4zvl8Nzflwlmgm9rwMTsOt5NLfs7cT0z83PJbISAFCsI7jnO5HXYg%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1&sigunguCd=11170&bjdongCd=13600&platGbCd=0&bun=0151&ji=0000&dongNm=101%EB%8F%99&hoNm=703%ED%98%B8
http://apis.data.go.kr/1611000/BldRgstService/getBrExposPubuseAreaInfo?ServiceKey=49rKGilAY%2FInAVDmv5kRUue6TsvmfpJ6t4zvl8Nzflwlmgm9rwMTsOt5NLfs7cT0z83PJbISAFCsI7jnO5HXYg%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1&platGbCd=0&sigunguCd=11170&bjdongCd=13600&bun=0151&ji=101%EB%8F%99&dongNm=0000&hoNm=703%ED%98%B8
'''
'''
지번주소를 알아옴
샘플
http://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDE3MTAzMDE4MDMwMjEwNzQ0NjA=&currentPage=1&countPerPage=10&resultType=xml&keyword=%EB%82%A8%EC%82%B0%ED%83%80%EC%9A%B4
'''

#from __future__ import print_function # Python 2/3 compatibility
#import boto3
import sqlite3

import json
import decimal
#from boto3.dynamodb.conditions import Key, Attr
#from botocore.exceptions import ClientError


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

jusoUrl = 'http://www.juso.go.kr/addrlink/addrLinkApi.do?'
confmKey='U01TX0FVVEgyMDE3MTAzMDE4MDMwMjEwNzQ0NjA='
currentPage='1'
countPerPage='10'
resultType='xml'
keyword='래미안 이문2차 101동 101호'
print(keyword)
keyword = parse.quote(keyword)
jusoUrl+= 'confmKey='+confmKey + '&currentPage='+ currentPage + '&countPerPage='+ countPerPage + '&resultType='+ resultType + '&keyword='+ keyword

# 출력 파일 명
#OUTPUT_FILE_NAME = 'output.xml'
#OUTPUT_FILE_NAME = 'output.txt'
OUTPUT_FILE_NAME = 'detail.json'


def getDetail(url):
    print(url)
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

ret = getDetail(jusoUrl)
print(ret[0])

#getDetail(Url)


bdUrl = 'http://apis.data.go.kr/1611000/BldRgstService/getBrExposPubuseAreaInfo?'
key = '49rKGilAY%2FInAVDmv5kRUue6TsvmfpJ6t4zvl8Nzflwlmgm9rwMTsOt5NLfs7cT0z83PJbISAFCsI7jnO5HXYg%3D%3D'

numOfRows = '10'
#pageSize=10&pageNo=1&startPage=1&sigunguCd=11170&bjdongCd=13600&platGbCd=0&bun=0151&ji=0000&dongNm=101%EB%8F%99&hoNm=703%ED%98%B8
pageSize = '10'
pageNo = '1'
startPage = '1'
sigunguCd = '50110' #법정동시군구코드(행정표준코드)
bjdongCd = '10200'  #법정동읍면동코드
#platGbCd = '0'      #대지구분코드(0:대지,1:산,2:블록)
bun = '0113'        #법정동본번코드
ji = '0007'         #법정동부번코드
print(parse.quote('동'))
dongNmP = '래미안 이문2차 101동'
hoNmP ='101호'
dongNm = parse.quote(dongNmP)
hoNm = parse.quote(hoNmP)
bdUrl+= 'ServiceKey='+key + '&numOfRows='+ numOfRows + '&pageSize='+ pageSize + '&pageNo='+ pageNo + '&startPage='+ startPage# + '&platGbCd='+ platGbCd
bdUrl+= '&sigunguCd='+ sigunguCd + '&bjdongCd='+ bjdongCd + '&bun='+ bun + '&ji='+ ji + '&dongNm='+ dongNm# + '&hoNm='+ hoNm
#url+='ServiceKey='+key + '&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
# 출력 파일 명
#OUTPUT_FILE_NAME = 'output.xml'
#OUTPUT_FILE_NAME = 'output.txt'
OUTPUT_FILE_NAME = 'detail.json'


def getDetail(url):
    print(url)
    request = Request(url)

    res_body = urlopen(request).read()
    rp_dict = xmltodict.parse(res_body)
    rp_json = json.dumps(rp_dict, ensure_ascii=False)

    #print(rp_dict)
    #print(rp_json)
    '''
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    open_output_file.write(rp_json)
    open_output_file.close()
    '''
    #print(xmltodict.parse(res_body))
    soup = BeautifulSoup(res_body, 'xml')
	
    items = soup.findAll('item')
    for item in items:
        
        #item = item.text.encode('utf-8')
        #item = re.sub('<.*?>', '|', str(item))
        #parsed = item.split('||')
        #print(parsed)
        #print(parsed[8])
        mainPurpsCdNm = item.mainPurpsCdNm.string
        #print(mainPurpsCdNm)
        if '아파트' in mainPurpsCdNm:
            #print(re.sub('츨','',item.flrNoNm.string))		
            ret = item.area.string,re.sub('층','',item.flrNoNm.string)
            #print(ret)
            return ret

ret = getDetail(bdUrl)
print(ret[0])
print(ret[1])
#dynamodb = boto3.resource("dynamodb")
#table = dynamodb.Table('aptTrx')

conn = sqlite3.connect('aptTrx.db')
c = conn.cursor()

# 도로명시군구코드+도로명코드+도로명일련번호코드+도로명지상지하코드+도로명건물본번호+부번호 => keyCode
keyCode = "11140"+"3000008"+"06"+"0"+"00246"+"00020"
#keyCode = "5011030200030100334900000|84.12|9"
keyCode = "1123041153360200000300010"
area = ret[0]
flr = ret[1]

c.execute("SELECT * FROM trx WHERE keyCode LIKE '"+keyCode+"'")
trxData = c.fetchall()
print(trxData)
for trxResult in trxData:
    print("RESULT : ",trxResult)
conn.commit()

'''
try:
    response = table.get_item(
        Key={
            'trxYear': 2017,
            'area': keyCode,	
        }
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    item = response['Item']
    print("GetItem succeeded:")
    print(json.dumps(item, indent=4, cls=DecimalEncoder))
'''
