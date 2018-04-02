from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup
import sqlite3
import time
import sys
import urllib.request

from datetime import date, datetime

#http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?\type=xml&LAWD_CD=11680&DEAL_YMD=201701&serviceKey=49rKGilAY%2FInAVDmv5kRUue6TsvmfpJ6t4zvl8Nzflwlmgm9rwMTsOt5NLfs7cT0z83PJbISAFCsI7jnO5HXYg%3D%3D

#url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?'
key = '49rKGilAY%2FInAVDmv5kRUue6TsvmfpJ6t4zvl8Nzflwlmgm9rwMTsOt5NLfs7cT0z83PJbISAFCsI7jnO5HXYg%3D%3D'

numOfRows = '1000'
url+= 'ServiceKey='+key + '&numOfRows='+ numOfRows
#url+='ServiceKey='+key + '&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
# 출력 파일 명
#OUTPUT_FILE_NAME = 'output.xml'
OUTPUT_FILE_NAME = 'output.txt'

#print url+queryParams

date_param = date.today().strftime('%Y%m')
conn = sqlite3.connect('loc.db')
c = conn.cursor()
c.execute('SELECT * FROM location')
locData = c.fetchall()
conn.commit()

conn = sqlite3.connect('aptTrx.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS trx(pCode text PRIMARY KEY, keyCode text, price text, conYear text, trxYear text, code1 text, code2 text, code3 text, code4 text, code5 text, code6 text, dong text, bcode1 text, bcode2 text, bcode3 text, bcode4 text, bcode5 text, apt text, trxMonth text, trxDay text, serialNo text, size text, gNo text, gCode text, floor text)')
conn.commit()

#지정된 지역코드 및 월의 아파트 거래 데이터를 받아와서 db에 insert
def howmuch(loc_param, date_param):
    numb = 0
    res_list = []
    res=''
    printed = False
    #print(loc_param, date_param)
    request = Request(url+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param)
    print(url+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param)
    res_body = urlopen(request).read()
    soup = BeautifulSoup(res_body, 'xml')

    items = soup.findAll('item')
    for item in items:
        #item = item.text.encode('utf-8')
        item = re.sub('<.*?>', '|', str(item))
        parsed = item.split('||')
        print(parsed)

        # SELECT*
        # FROMcbs0422
        # WHEREunion_bldg_mngm_noLIKE'1111041001350300000400000'
        # 도로명시군구코드+도로명코드+도로명일련번호코드+도로명지상지하코드+도로명건물본번호+부번호 => keyCode
        # keyCode = parsed[6]+parsed[9]+parsed[7]+parsed[8]+parsed[4]+parsed[5]
        keyCode = parsed[7] + parsed[10] + parsed[8] + parsed[9] + parsed[5] + parsed[6]
        pCode = loc_param + date_param + str(numb)
        print(keyCode)
        c.execute('INSERT or IGNORE INTO trx VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (pCode, keyCode ,parsed[1].strip(), parsed[2], parsed[3], parsed[4], parsed[5], parsed[6], parsed[7], parsed[8], parsed[9], parsed[10], parsed[11], parsed[12], parsed[13], parsed[14], parsed[15], parsed[16], parsed[17], parsed[18], parsed[19], parsed[20], parsed[21], parsed[22], parsed[23]))
        numb += 1

    conn.commit()

    #return res_list

cnt = 0
for loc in locData:

    loc_param = loc[1]

    end = False
    startY = 2006
    startM = 1
    endY = 2006
    endM = 2

    while (not end):

        if (startM > 9):
            date_param = str(startY) + str(startM)
        else:
            date_param = str(startY) + '0' + str(startM)

        howmuch(loc_param, date_param)

        if (endY < startY):
            end = True
        elif (endY == startY):
            if (endM <= startM):
                end = True

        if (startM == 12):
            startM = 1
            startY += 1
        else:
            startM += 1

'''
    if cnt > 1:
        break
    cnt += 1
'''
#result = howmuch('50110', date_param)
#howmuch('50130', date_param)

'''
open_output_file = open(OUTPUT_FILE_NAME, 'w')
#print(soup)
open_output_file.write(str(result))
open_output_file.close()
'''


