import requests
from bs4 import BeautifulSoup
import pprint
import unicodecsv as csv
import pandas as pd

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.storylink')
scores = soup.select('.score')

def curate_hacker_news(links,scores, filter_upvote):
	curate_list = []
	for i in range(len(links)):
		title = links[i].text
		href = links[i].get('href', None)
		points = scores[i].text
		if points:
			range_scores = int(points.replace(' points', ''))
			if range_scores > filter_upvote:
				curate_list.append({'Title': title, 'Link': href, 'Upvotes': range_scores})
	deceding_list_by_votes = sorted(curate_list, key = lambda k: k['Upvotes'], reverse=True)
	return deceding_list_by_votes

def curated_links(votes):
	with open('./static/files/links.csv', 'wb') as csvfile:
		fieldnames = ['Title', 'Link', 'Upvotes']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in curate_hacker_news(links,scores, votes):
			writer.writerow(item)
	return 'Successfully completed!'


def view_csv_in_html(votes):
	curated_links(votes)
	df = pd.read_csv('./static/files/links.csv')
	html_csv = df.to_html()
	return html_csv