import requests
import pandas
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
#https://www.zomato.com/auckland/restaurants?gold_partner=1&page={}
list_rest =[]

def getInfo(soup):
    names = [item.text.strip() for item in soup.select('.result-title')]
    locality = [item.text.strip() for item in soup.select('.search_result_subzone')]
    addresses =  [item.text.strip() for item in soup.select('.search-result-address')]
    mobile_number =  [item.attrs.get('data-phone-no-str') for item in soup.select('.res-snippet-ph-info')]
    rating =  [item.text.strip() for item in soup.select('.res-rating-nf')]
    #cuisine = [item.text.strip() for item in soup.select('.clearfix')]
    costForTwo = [item.text.strip() for item in soup.select('.res-cost')]
    timings = [item.text.strip() for item in soup.select('.res-timing')]
    row = list(zip(names, locality, addresses, mobile_number, rating, costForTwo, timings))
    return row

with requests.Session() as s:   
        url = 'https://www.zomato.com/east-of-england/bedfordshire-restaurants?page={}'
        response = s.get(url.format(1),headers=headers)
        content = response.content
        soup = BeautifulSoup(content,"lxml")
        #print(soup);
        numPages = int(soup.select_one('.pagination-number b:last-child').text)
        print(numPages);
        list_rest.append(getInfo(soup))

        if numPages > 1:
            for page in range(2, numPages + 1):
                response = s.get(url.format(page),headers=headers)
                print(page)
                content = response.content
                soup = BeautifulSoup(content,"lxml")
                list_rest.append(getInfo(soup))

final_list = [item for sublist in list_rest for item in sublist]
print(final_list)
df = pandas.DataFrame(final_list, columns = ['Name', 'Locality', 'Address', 'Mobile Number', 'Rating', 'Cost_For_Two', 'Timings'])
df.to_csv(r"zomato_bedfordshireRestro.csv", sep=',', encoding='utf-8-sig',index = False )