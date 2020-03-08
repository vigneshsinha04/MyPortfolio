import requests
from bs4 import BeautifulSoup
import unicodecsv as csv
import pandas as pd

res = requests.get('https://www.imdb.com/list/ls002448041/')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.lister-item-content')

def curate_hacker_news(links, filter_upvote):
	curate_list = []
	for i in range(len(links)):
		title = links[i].a.text
		href = links[i].a.get('href', None)
		points = links[i].find('span', class_ = 'ipl-rating-star__rating').text
		if points:
			if float(points) > float(filter_upvote):
				curate_list.append({'Title': title, 'Link': 'imdb.com'+href, 'Upvotes': points})
	deceding_list_by_votes = sorted(curate_list, key = lambda k: k['Upvotes'], reverse=True)
	return deceding_list_by_votes

def curated_links(votes):
	with open('./static/files/links.csv', 'wb') as csvfile:
		fieldnames = ['Title', 'Link', 'Upvotes']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in curate_hacker_news(links, votes):
			writer.writerow(item)
	return 'Successfully completed!'


def view_csv_in_html(votes):
	curated_links(votes)
	df = pd.read_csv('./static/files/links.csv')
	html_csv = df.to_html()
	return html_csv