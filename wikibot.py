import praw
import time
import io
from datetime import date
from datetime import datetime
from pytz import timezone
tz = timezone('EST')

reddit = praw.Reddit(client_id='XGXe8jL8VNnKaTWKuaI05w', \
                     client_secret='c7qatNw4QWMBXuzPBjaeb9dFoMyoDA', \
                     user_agent='CointestMaster', \
                     refresh_token='1039453707688-_9VabNb5veb7IfsfWYqZHyNV0vN86Q', \
                     redirect_url='http://localhost:8080')

cc = reddit.subreddit('CointestOfficial')

def check(dati):
    import calendar
    #  calendar.monthrange return a tuple (weekday of first day of the 
    #  month, number  
    #  of days in month)
    last_day_of_month = calendar.monthrange(dati.year, dati.month)[1]
    # here i check if date is last day of month
    if dati == date(dati.year, dati.month, last_day_of_month):
        return True
    return False



while True:
    contentlist = []
    posted = 0
    content = reddit.subreddit("CointestAdmin").wiki["scheduledposts"].content_md
    ugh = content.index('~')
    sk = ugh
    content = content.split('\n')
    del content[1]
    del content[2]
    category = content[0]

    topics = content[1].split(',')

    title = content[2]


    dt = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
    dat = date(int(dt[6:10]), int(dt[3:5]), int(dt[0:2]))
    month = datetime.now().strftime("%B")
    print(dt[11:19])
    
    if check(dat) == True and dt[11:19] == '22:00:00':
        for topic in topics:
            post = reddit.subreddit("CointestAdmin").wiki["scheduledposts"].content_md[sk+1: -1]
            post = post.replace('{category}', category)
            post = post.replace('{topic}', topic)
            post = post.replace('{topicr}', topic.replace(' ',''))
            post = post.replace('{month}', month)

            content = reddit.subreddit("CointestAdmin").wiki["scheduledposts"].content_md.split('\n')
            del content[1]
            del content[2]
            title = content[2]

            title = title.replace('{category}', category)
            title = title.replace('{topic}', topic)
            title = title.replace('{month}', month)

            cc.submit(title, post)
            cc.submit(title.replace('Pro', 'Con'), post.replace('Pro', 'Con'))
        
        time.sleep(1)
                
    
    


