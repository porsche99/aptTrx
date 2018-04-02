

'''
주소를 받아 지번주소 및 주소 상세를 알아옴
http://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDE3MTAzMDE4MDMwMjEwNzQ0NjA=&currentPage=1&countPerPage=10&resultType=xml&keyword=%EB%82%A8%EC%82%B0%ED%83%80%EC%9A%B4

고객의 아파트 주소 정보를 받아서 해당 주소의 면적 및 층수를 리턴
건축물대장 OpenAPI 활용
샘플
http://apis.data.go.kr/1611000/BldRgstService/getBrExposPubuseAreaInfo?serviceKey=49rKGilAY%2FInAVDmv5kRUue6TsvmfpJ6t4zvl8Nzflwlmgm9rwMTsOt5NLfs7cT0z83PJbISAFCsI7jnO5HXYg%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1&sigunguCd=11170&bjdongCd=13600&platGbCd=0&bun=0151&ji=0000&dongNm=101%EB%8F%99&hoNm=703%ED%98%B8

insertAptTrx.py 를 통해 dynamodb에 넣어둔 아파트 매매가에 대한 정보인 aptTrx2 를 조회하여 아파트 가격을 리턴한다.

'''

from __future__ import print_function # Python 2/3 compatibility
import boto3
import sqlite3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup

import xmltodict

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

#입력받은 아파트 주소로 지번주소 및 주소상세를 조회한다
inputKeyword = '남산타운 31동 1701호'  # 아파트 주소(입력받아야함.)

def getDetailAddr(keyword):
    addrDetailUrl = 'http://www.juso.go.kr/addrlink/addrLinkApi.do?'
    confmKey = 'U01TX0FVVEgyMDE3MTAzMDE4MDMwMjEwNzQ0NjA='
    currentPage = '1'
    countPerPage = '10'
    resultType = 'xml'
    print("조회할 주소 : " + keyword)
    keyword = parse.quote(keyword)
    addrDetailUrl += 'confmKey=' + confmKey + '&currentPage=' + currentPage + '&countPerPage=' + countPerPage + '&resultType=' + resultType + '&keyword=' + keyword
    print(addrDetailUrl)
    request = Request(addrDetailUrl)
    res_body = (urlopen(request).read())
    #rp_dict = xmltodict.parse(res_body)
    #rp_json = json.dumps(rp_dict, ensure_ascii=False, indent=4, cls=DecimalEncoder)
    #print(rp_json)
    soup = BeautifulSoup(res_body, 'xml')
    jusos = soup.findAll('juso')
    #행정구역코드(법정동시군구코드+법정동읍면동코드), 지번본번, 지번부번, 도로명주소, 지번주소
    retDetailAddr = jusos[0].admCd.string[0:5], jusos[0].admCd.string[5:10], jusos[0].lnbrMnnm.string, jusos[0].lnbrSlno.string, jusos[0].roadAddr.string, jusos[0].jibunAddr.string
    return retDetailAddr


#지번주소를 입력받아 해당 주소 아파트의 건물 상세정보를 조회한다다 : 면적 및 층수 조회
def getDetailBuildingInfo(sigunguCd, bjdongCd, bun, ji, dongNmP, hoNmP):
    buildingInfoUrl = 'http://apis.data.go.kr/1611000/BldRgstService/getBrExposPubuseAreaInfo?'
    key = '49rKGilAY%2FInAVDmv5kRUue6TsvmfpJ6t4zvl8Nzflwlmgm9rwMTsOt5NLfs7cT0z83PJbISAFCsI7jnO5HXYg%3D%3D'
    numOfRows = '10'
    # pageSize=10&pageNo=1&startPage=1&sigunguCd=11170&bjdongCd=13600&platGbCd=0&bun=0151&ji=0000&dongNm=101%EB%8F%99&hoNm=703%ED%98%B8
    pageSize = '10'
    pageNo = '1'
    startPage = '1'
    # platGbCd = '0'      #대지구분코드(0:대지,1:산,2:블록)
    dongNm = parse.quote(dongNmP)
    hoNm = parse.quote(hoNmP)
    buildingInfoUrl += 'ServiceKey=' + key + '&numOfRows=' + numOfRows + '&pageSize=' + pageSize + '&pageNo=' + pageNo + '&startPage=' + startPage  # + '&platGbCd='+ platGbCd
    buildingInfoUrl += '&sigunguCd=' + sigunguCd + '&bjdongCd=' + bjdongCd + '&bun=' + bun + '&ji=' + ji + '&dongNm=' + dongNm  + '&hoNm='+ hoNm
    # buildingInfoUrl+='ServiceKey='+key + '&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param

    print(buildingInfoUrl)
    request = Request(buildingInfoUrl)

    res_body = urlopen(request).read()
    #rp_dict = xmltodict.parse(res_body)
    #rp_json = json.dumps(rp_dict, ensure_ascii=False)
    #print(rp_dict)
    #print(rp_json)
    #print(xmltodict.parse(res_body))
    soup = BeautifulSoup(res_body, 'xml')
	
    items = soup.findAll('item')
    for item in items:
        #item = item.text.encode('utf-8')
        #item = re.sub('<.*?>', '|', str(item))
        #parsed = item.split('||')
        #print(parsed)
        #print(parsed[8])
        #mainPurpsCdNm = item.mainPurpsCdNm.string
        exposPubuseGbCd = item.exposPubuseGbCd.string
        #if '아파트' in mainPurpsCdNm:
        if '1' in exposPubuseGbCd:
            #print(re.sub('츨','',item.flrNoNm.string))		
            retDetailBuildingInfo = item.area.string, re.sub('층','',item.flrNoNm.string)
            #print(ret)
            return retDetailBuildingInfo


#주소를 입력
detailAddr = getDetailAddr(inputKeyword)
print(detailAddr)

sigunguCdIn = detailAddr[0]  # 법정동시군구코드(행정표준코드)
bjdongCdIn = detailAddr[1]  # 법정동읍면동코드
bunIn = detailAddr[2].zfill(4)  # 법정동본번코드(4자리로 '0' padding 필요)
jiIn = detailAddr[3].zfill(4)  # 법정동부번코드(4자리로 '0' padding 필요)

dongNmPIn ='31동'
hoNmPIn = '1701호'

detailBuildingInfo = getDetailBuildingInfo(sigunguCdIn, bjdongCdIn, bunIn, jiIn, dongNmPIn, hoNmPIn)
#print(detailBuildingInfo)
#print(detailBuildingInfo[0])
#print(detailBuildingInfo[1])

#dynamodb인 aptTrx2 에 저장된 아파트 실거래가 정보를 조회한다
#아파트 실거래가 api 에서는 동호수에 대한 정보는 없으며 층수 및 면적에 대한 정보만 존재

#dynamodb = boto3.resource("dynamodb")

#table = dynamodb.Table('aptTrx2')

# 도로명시군구코드+도로명코드+도로명일련번호코드+도로명지상지하코드+도로명건물본번호+부번호 => keyCodeB
#keyCode = "11140"+"3000008"+"06"+"0"+"00246"+"00020"
#keyCode += "|84.12|9"

area = detailBuildingInfo[0]
flr = detailBuildingInfo[1]
#keyCode = sigunguCdIn+bjdongCdIn+bunIn+jiIn
keyCode = sigunguCdIn+bjdongCdIn+bunIn+jiIn+"|"+area+"|"+flr
print(keyCode)
year=2006
mon=4
conn = sqlite3.connect('../aptTrx.db')
c = conn.cursor()
c.execute("SELECT * FROM trxData WHERE keyCode LIKE '"+keyCode+"'")
trxData = c.fetchall()
#print(trxData)
for trxResult in trxData:
    print("RESULT : ",trxResult)
conn.commit()


'''
year=2006
while year<2018:
	try:
		response = table.get_item(
			Key={
				'trxYear': year,
				'keyCodeB': keyCodeB,
			}
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		item = response['Item']
		#print("GetItem succeeded:")
		print(json.dumps(item, indent=4, cls=DecimalEncoder))
		print(str(year)+"년의 아파트 가격은 = "+str(item['trxPrice']))
		year += 1
		print(year)
'''
'''
try:
	response = table.get_item(
		Key={
			'trxYear': year,
			'keyCodeB': keyCodeB,
		}
	)
except ClientError as e:
	print(e.response['Error']['Message'])
else:
	item = response['Item']
	#print("GetItem succeeded:")
	print(json.dumps(item, indent=4, cls=DecimalEncoder))
	print(str(year)+"년의 아파트 가격은 = "+str(item['trxPrice']))
		
response = table.scan(
    FilterExpression= Attr('trxYear').eq(year) & Attr('keyCodeB').eq(keyCodeB)
)
items = response['Items']
print(items)
for item in items:
   print(str(item['trxYear'])+'|'+str(item['trxPrice']))
'''
