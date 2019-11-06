#! /usr/bin/env python

"""

Install guide:
pip install beautifulsoup4
pip install requests
pip install scrapy

"""
from __future__ import print_function
from bs4 import BeautifulSoup
from six.moves.urllib import parse
import requests, json, csv, time, urlparse, os
apiEndPoint = "https://mmajunkie.com/?infinity=scrolling"
csvData = []

def getShareData(url):
    r = requests.get(shareEndPoint+url)
    socialData = json.loads(r.text)
    return socialData['shares']

def getFeedData(url, currentPage):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, {'action':'infinite_scroll','page':currentPage,'order':'DESC'}, headers)
    feedData = json.loads(r.text)
    if feedData['type'] == "empty":
        return 0
    else:
        for url in feedData['postflair']:
            shares = getShareData(url)
            if not 'facebook' in shares:
                shares['facebook'] = '0'
            if not 'twitter' in shares:
                shares['twitter'] = '0'
            if not 'email' in shares:
                shares['email'] = '0'
            total_shares = str(int(shares['facebook'])+int(shares['twitter'])+int(shares['email']))
            title = url.rsplit('/', 1)[-1].replace('-', ' ').capitalize()
            csvData.append(
                {
                    'title': title,
                    'url': url,
                    'total_shares': total_shares,
                    'facebook_shares': shares['facebook'],
                    'twitter_shares': shares['twitter'],
                    'email_shares': shares['email']
                }
            )
        print(">> Fetched feed page("+str(currentPage)+"). Total URLs extracted("+str((currentPage*7))+")")
        #add or give back data for array collection
        return 1

def main():
    print(">>--------------------------------------------------------<<")
    print(">>       Infinite scroll wordpress analytics scraper      <<")
    print(">>                            L44                         <<")
    print(">>--------------------------------------------------------<<")
    print(">> API Endpoint: "+apiEndPoint)
    print(">> Extracting feed URLs with analytics.. ")
    currentPage = 1 #starting page feed
    while currentPage <= 50: #remove <= 50 for unlimited.
        feedData = getFeedData(apiEndPoint, currentPage)
        if not feedData:
            currentPage = false
            print(">> End of feed data, page "+str(currentPage)+" empty.")
            break
        currentPage = currentPage+1
        continue
    print(">> Fetch Completed.")
    print(">> Preparing CSV Export..")
    csvName = 'generated'+str(int(time.time()))+'.csv'
    with open(csvName, 'w') as csvfile:
        fieldnames = ['title', 'url', 'total_shares', 'facebook_shares', 'twitter_shares', 'email_shares']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dataRow in csvData:
            writer.writerow(dataRow)

    print(">> CSV Exported! "+csvName)

if __name__ == '__main__':
    main()
