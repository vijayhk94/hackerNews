This is a custom hackernews website with custm sorting algorithm for displaying news items.
The app is written in python flask. For database operations it uses sqlalchemy.
Major features:
1. Multiple users can sign up/sign in/sign out.
2. Home button on sign in will show news items from top 3 pages of hackernews in reverse chronological order.
3. Refresh button on Homepage refreshes the list of news items.
4. Each news item can be marked as read/unread, deleted and bookmarked.
5. Bookmarked items for the logged in user will show up in Bookmarks tab in home page.
6. An item once dleted will not be removed from db, will just not show up for that specific user.

Design:
1. 4 main componenents: page scraper, database, backend logic, frontend.
2. Flask takes care of backend logic and rendering the frontend, which uses python and html/css/bootstrap respectively.
3. Page scraper, again is written in python3 and beautifulsoup4.
4. we are using a mysql database and sqlalchemy as the interface. Main tables are: hn_items(where all news items list goes after scrapped.). read_items(user_id, news_id). deleted_items(user_id, news_id) and bookmarks(user_id, news_id)
5. each Hn_item has age, score, commentscount, url, hackernewsurl, id, title.
6. parent package is hackerNews folder, all htmls are in templates folder inside that.
7. models.py file has all database models and routes.py is responsible for routing. App definition file is run.py.

Deploying the app on local:
The commands given in these steps will work on linux systems. Please find equivalent commands for windows/mac systems. Also, make sure you are using python3 and pip3 while executing these.
1. Go to the directory where this readme file is located in terminal.
2. Execute "sh installFlaskMysql.sh".This will install flask, mysql and take you to mysql terminal.
3. Execute "source createDb.sql" on mysql terminal.
5. Execute "exit" to come out of mysql terminal.
6. Execute "source venv/bin/activate" to activate flask environment.
7. Execute "pip install -r requirements.txt" to install all requirements.
8. Execute "python3 run.py" to run the app on localhost:5000.