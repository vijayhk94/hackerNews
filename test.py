from HnScraper import HnScraper
from HnItemDao import HnItemDao
from HnItem import HnItem

test = []

test = HnScraper.getHnItems(3)
#print('From test.py, test is as below:')
#print(test)
HnItemDao.insertHnItems(test)
list_ = HnItemDao.getHnItems()
for x in list_:
	print(x)
	print()
#print()
#print()
"""for x in list_:
	print(HnItem(x).id)
	print(HnItem(x).postedHoursBefore)
	print(HnItem(x).comments)
	print(HnItem(x).upvotes)
	print(HnItem(x).title)
	print(HnItem(x).url)
	print(HnItem(x).hnUrl)"""