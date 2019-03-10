from hackerNews import mysql
from hackerNews.models import HnItem

class HnItemDao:
	@staticmethod
	def insertHnItems(hnItemList):
		INSERT_HN_ITEMS = getInsertQuery()
		conn=mysql.connect()
		#conn.set_character_set('utf8')
		cursor = conn.cursor()
		#cursor.execute('SET NAMES utf8;')
		#cursor.execute('SET CHARACTER SET utf8;')
		#cursor.execute('SET character_set_connection=utf8;')  
		#cursor.execute('use hndb')
		#conn.commit()
		for x in hnItemList:
			cursor.execute(INSERT_HN_ITEMS, (int(x.id), x.title, x.url, x.hnUrl, int(x.postedHoursBefore), int(x.upvotes), int(x.comments)))
			conn.commit()
	@staticmethod
	def getHnItems():
		SELECT_ITEMS = getSelectQuery()
		conn=mysql.connect()
		#conn.set_character_set('utf8')
		cursor = conn.cursor()
		#cursor.execute('SET NAMES utf8;')
		#cursor.execute('SET CHARACTER SET utf8;')
		#cursor.execute('SET character_set_connection=utf8;')  
		#cursor.execute('use hndb')
		#conn.commit()
		cursor.execute(SELECT_ITEMS)
		itemsList = cursor.fetchall()
		return itemsList
	@staticmethod
	def flushTable():
		conn=mysql.connect()
		cursor = conn.cursor()
		cursor.execute('TRUNCATE TABLE hn_item')
		conn.commit()
def getInsertQuery():
	return "INSERT INTO hn_item(id, title, url, hnUrl, postedHoursBefore, upvotes, comments) VALUES(%s, %s, %s, %s, %s, %s, %s)"
def getSelectQuery():
	return "SELECT * FROM hn_item ORDER BY postedHoursBefore ASC"