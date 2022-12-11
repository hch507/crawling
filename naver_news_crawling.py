import os
import sys
import urllib.request
import datetime
import time
import json

client_id = ''
client_secret =''

def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
        return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query = %s&start = %s&display = %s"%(urllib.parse.quote(srcText), start, display)
    start_url = base + node + parameters
    url = start_url.replace(" ","")
    responseDecode = getRequestUrl(url)
    
    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']
    
    ##pDate = datetime.datetime.strptime(post['pubDate'], '%a,%d %b %Y %H:%M:%S+0900')
    ##pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
    jsonResult.append({'cnt':cnt, 'title':title, 'description': description,
                       'org_link':org_link, 'link': org_link})

    return



def main():
    node = 'news' #크롤링할대상
    srcText = input('검색어를입력하세요: ')
    cnt = 0
    
    jsonResult = []
    jsonResponse = getNaverSearch(node, srcText, 1, 100) 
    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)
            
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)
    print('전체검색: %d 건' %total)
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8')as outfile:
        jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True,
                                  ensure_ascii = False)
        outfile.write(jsonFile)
    print("가져온데이터: %d 건" %(cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))
   
