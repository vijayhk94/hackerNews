from hackerNews import mysql, db
from hackerNews.models import HnItem

class HnItemDao:
	@staticmethod
	def insertHnItems(hnItemList):
		INSERT_HN_ITEMS = getInsertQuery()
		conn=mysql.connect()
		cursor = conn.cursor()
		for x in hnItemList:
			db.session.add(x)
			db.session.commit()
	@staticmethod
	def getHnItems():
		SELECT_ITEMS = getSelectQuery()
		conn=mysql.connect()
		cursor = conn.cursor()
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