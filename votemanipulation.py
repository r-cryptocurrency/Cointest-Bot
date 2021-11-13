import praw
import time
import os
import io
import discord
import os
import requests
from discord import Webhook, RequestsWebhookAdapter
import random
import sentiment as sm
classifier = sm.train()


webhook = Webhook.from_url("https://discord.com/api/webhooks/894711244362235994/tPHIX_CylDUuxySE9_bf75tlvJMR6O-qUhXWx_9CFTabhYbyU8Yh-GqJ7I409nadYzWZ", adapter=RequestsWebhookAdapter())

reddit = praw.Reddit(client_id='XGXe8jL8VNnKaTWKuaI05w', \
                     client_secret='c7qatNw4QWMBXuzPBjaeb9dFoMyoDA', \
                     user_agent='CointestMaster', \
                     refresh_token='1039453707688-_9VabNb5veb7IfsfWYqZHyNV0vN86Q', \
                     redirect_url='http://localhost:8080')

cc = reddit.subreddit('CryptoCurrency')
cc = cc.hot(limit=200)
done = []

for submission in cc:
    submission.comments.replace_more(limit=0)
    if submission.stickied == False:
        indiv = []
        
        ratio = submission.upvote_ratio
        if ratio >= 0.95:
            indiv.append('Highly abnormal upvote ratio: '+ str(ratio))
        

        timeposted = int(submission.created_utc)
        timenow = int(time.time())
        score = submission.score
        oop = int((timenow-timeposted)/60)
        if score/4 > oop:
            indiv.append('Excessive upvotes: '+str(score)+' upvotes in '+str(oop)+' minutes.')

        num = submission.num_comments
        if num*4 > score:
            indiv.append('Abnormally low comments: '+str(num)+' comments within '+str(oop)+' minutes of being posted.')

        if num > 50:
            num = int(num * 0.7)
            authors = [str(comment.author) for comment in submission.comments]
            try:
                randomlist = random.sample(range(1, int(len(authors)*0.7)), 50)
            except:
                randomlist = random.sample(range(1, 20), 10)
            p = []
            for number in randomlist:
                author = authors[number]
                c = 0
                if author != 'None':
                    try:
                        for comment in reddit.redditor(author).comments.new(limit=1000):
                            if str(comment.subreddit) == 'CryptoCurrency':
                                c += 1
                    except:
                        pass
                if c < 40:
                    p.append('Low')
            if len(p) > 20:
                indiv.append('The commenters have abnormally low participation in r/CC: '+str(len(p))+' out of 50 randomly chosen commenters have below 40 lifetime comments in r/CC.')

        awards = submission.all_awardings
        awards = [element['count'] for element in awards]
        awards = sum(awards)
        if awards > score or awards*15 > oop:
            indiv.append('There seems to be an abnormal amount of awards: '+str(awards)+' within only ' + str(oop) + ' minutes of being posted')


        submission.comment_sort = 'best'
        sentlist = []
        for comment in list(submission.comments)[1:50]:
            sentlist.append(sm.classify(comment.body, classifier))
        poscount = sentlist.count('Positive')
        if poscount >= 35:
            indiv.append('The comments of this post are abnormally positive: there were '+str(poscount)+' positive comments out of the 50 newest comments.')

      
        if len(indiv) >= 3 and score < 10000:
            m = ' \n  - '.join(indiv)
            message = 'This post: https://old.reddit.com' + submission.permalink + ' has been flagged for the following reasons \n  -' + m + ' \n For more evidence, you may check https://upvotetracker.com/post' + submission.permalink
            webhook.send(message)
        
                

    
    

    
        

