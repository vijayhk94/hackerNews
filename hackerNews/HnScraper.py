from bs4 import BeautifulSoup
import requests
import lxml
from hackerNews.models import HnItem

class HnScraper:
	@staticmethod
	def getHnItems(pages):
		baseUrl = 'https://news.ycombinator.com/'
		relativeUrl = ''
		hnItemList = []
		for i in range(pages):
			source = requests.get(f'{baseUrl}{relativeUrl}').text
			soup = BeautifulSoup(source, 'lxml')
			body = soup.find('body')
			center = body.center
			table = center.table
			listTr = table.find_all('tr')
			itemListBody = listTr[3]
			athingList = itemListBody.td.table.find_all('tr', class_='athing')
			subtextList = []
			for item in itemListBody.td.table.find_all('tr'):
				subtextList.append(item.find('td', class_='subtext'))
			subtextList = [x for x in subtextList if x is not None]
			scoreList = []
			for subtext in subtextList:
				scoreList.append(subtext.find('span', class_='score'))
			scoreList = [x for x in scoreList if x is not None]
			ageList = []
			for subtext in subtextList:
				ageList.append(subtext.find('span', class_='age'))
			ageList = [x for x in ageList if x is not None]
			commentsList = []
			for subtext in subtextList:
				commentsList.append(subtext.find_all('a')[-1])
			commentsList = [x for x in commentsList if x is not None]
			for athing in athingList:
				id = athing['id']
				titleObj = athing.find_all('td', class_='title')[1]
				title = titleObj.find('a').contents[0]
				url = titleObj.find('a')['href']
				scoreString = next((x for x in scoreList if x['id'] == f'score_{id}'), None)
				score = 0
				if scoreString is not None:
					score = scoreString.contents[0].split(' ')[0]
				ageString = next((x for x in ageList if x.find('a')['href'] == f'item?id={id}'), None)
				age = 0
				if ageString is not None:
					age = ageString.find('a').contents[0].split(' ')[0]
				commentsString = next((x for x in commentsList if x['href'] == f'item?id={id}'), None)
				comments = 0
				if commentsString is not None:
					comments_content = commentsString.contents[0]
					comments_content = comments_content.replace('\xa0',' ')
					comments_list = comments_content.split(' ')
					comments = comments_list[0]
				if comments == 'discuss':
					comments = 0
				hnItem = HnItem(id, title, url, baseUrl, age, score, comments)
				hnItemList.append(hnItem)
			moreLink = itemListBody.td.table.find_all('tr')[-1]
			moreString = moreLink.find('td', class_='title').find('a', class_='morelink')['href']
			relativeUrl = f'{moreString}'
		return hnItemList	