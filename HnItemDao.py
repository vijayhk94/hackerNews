import MySQLdb
from HnItem import HnItem

class HnItemDao:
	@staticmethod
	def insertHnItems(hnItemList):
		INSERT_HN_ITEMS = getInsertQuery()
		conn=MySQLdb.connect(host='localhost',user='vijay',passwd='vijay123')
		conn.set_character_set('utf8')
		cursor = conn.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SET CHARACTER SET utf8;')
		cursor.execute('SET character_set_connection=utf8;')  
		cursor.execute('use hndb')
		conn.commit()
		for x in hnItemList:
			cursor.execute(INSERT_HN_ITEMS, (int(x.id), x.title, x.url, x.hnUrl, int(x.postedHoursBefore), int(x.upvotes), int(x.comments)))
			conn.commit()
	@staticmethod
	def getHnItems():
		SELECT_ITEMS = getSelectQuery()
		conn=MySQLdb.connect(host='localhost',user='vijay',passwd='vijay123')
		conn.set_character_set('utf8')
		cursor = conn.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SET CHARACTER SET utf8;')
		cursor.execute('SET character_set_connection=utf8;')  
		cursor.execute('use hndb')
		conn.commit()
		cursor.execute(SELECT_ITEMS)
		itemsList = cursor.fetchall()
		return itemsList
def getInsertQuery():
	return "INSERT INTO hnItem(id, title, url, hnUrl, postedHoursBefore, upvotes, comments) VALUES(%s, %s, %s, %s, %s, %s, %s)"
def getSelectQuery():
	return "SELECT * FROM hnItem ORDER BY postedHoursBefore ASC"