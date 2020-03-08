import requests
from bs4 import BeautifulSoup
import unicodecsv as csv
import pandas as pd

res = requests.get('https://www.gamepedia.com/')
res2 = requests.get('https://www.gamepedia.com/?page=2')
res3 = requests.get('https://www.gamepedia.com/?page=3')
res4 = requests.get('https://www.gamepedia.com/?page=4')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
soup3 = BeautifulSoup(res3.text, 'html.parser')
soup4 = BeautifulSoup(res4.text, 'html.parser')
links = soup.find_all('article')
links2 = soup2.find_all('article')
links3 = soup3.find_all('article')
links4 = soup4.find_all('article')
author = soup.select('.p-article-byline')
author2 = soup2.select('.p-article-byline')
author3 = soup3.select('.p-article-byline')
author4 = soup4.select('.p-article-byline')

mega_links = links + links2 + links3 + links4
mega_author = author + author2 + author3 + author4

def curate_hacker_news(links,mega_author):
	curate_list = []
	for i in range(len(mega_links)):
		title = mega_links[i].h2.a.text
		href = mega_links[i].h2.a.get('href', None)
		author = mega_author[i].a.span.text
		curate_list.append({'Title': title, 'Link': href, 'Author': author})
	return curate_list

def curated_links():
	with open('./static/files/links.csv', 'wb') as csvfile:
		fieldnames = ['Title', 'Link', 'Author']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in curate_hacker_news(mega_links,mega_author):
			writer.writerow(item)
	return 'Successfully completed!'


def view_csv_in_html():
	curated_links()
	df = pd.read_csv('./static/files/links.csv')
	html_csv = df.to_html()
	return html_csv