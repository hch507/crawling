from bs4 import BeautifulSoup
import urllib.request
import pandas as pd



def Pascucci_store(result):
    for page in range(1,4):
        Pascucci_url= 'https://www.caffe-pascucci.co.kr/store/storeList.asp?searchRegion=20046000&page=%d='%page
        print(Pascucci_url)
        html = urllib.request.urlopen(Pascucci_url)
        soupPascucci= BeautifulSoup(html, 'html.parser')
        tag_tbody= soupPascucci.find('tbody')
        for store in tag_tbody.find_all('tr'):
            
            store_td= store.find_all('td')
            store_addr = store.find('p',attrs={'class': 'addr'})
            store_name= store_td[1].string
            store_sido= store_td[2].string
            
            result.append([store_name]+[store_sido]+[store_addr])
    return

def main():
    result = []
    print('Pasccucci store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    Pascucci_store(result)
    Pascucci_tbl= pd.DataFrame(result, columns = ('store', 'sido-gu','address'))
    Pascucci_tbl.to_csv('pascu1.csv',encoding = 'cp949', mode = 'w', index = True)
    del result[:]

    if __name__ == '__main__':
        main()
                        


    
