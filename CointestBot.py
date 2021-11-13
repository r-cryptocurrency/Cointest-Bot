import praw
import time
import os
import io
import os
import requests

url = 'https://discord.com/api/webhooks/900414122955505774/X6t7seZ3gefJHb5ZL26ZHBvDZciVsybd2j4XuwgxUUvuYrjyrDLm3YXUfO4CRkPZ9Sb5'


first = 'na'
links = {}
undone = []
scores = {}
reddit = praw.Reddit(client_id='XGXe8jL8VNnKaTWKuaI05w', \
                     client_secret='c7qatNw4QWMBXuzPBjaeb9dFoMyoDA', \
                     user_agent='CointestMaster', \
                     refresh_token='1039453707688-_9VabNb5veb7IfsfWYqZHyNV0vN86Q', \
                     redirect_url='http://localhost:8080')

cc = reddit.subreddit('CryptoCurrency')
posted = reddit.subreddit('CointestAdmin')
answer = input('Do you want to crosspost, copy all comments, tally scores, declare winners, or congratulate winners? \n')
search = "author:CointestAdmin title:'r/CC Cointest'"


def reportDiscordEntry(author, title, link):
    repl = 'ENTRY - An entry was submitted by u/' + author + '  in the "' + title + '" thread. You can judge it here: https://old.reddit.com' + link
    data = {"content" : repl, "username" : "Cointest_Notifier"}
    result = requests.post(url, json = data)

def reportDiscordEdit(author, title, link):
    repl = 'EDIT - An entry was edited by u/' + author + '  in the "' + title + '" thread. You can re-judge it here: https://old.reddit.com' + link
    data = {"content" : repl, "username" : "Cointest_Notifier"}
    result = requests.post(url, json = data)

def locatenumbers(s):
    l = 0
    for t in s.split():
        try:
            l += float(t)
        except ValueError:
            pass
    return l

def locatenumber(a):
    b = a.index('of ')
    b += 3
    d = a.index('. The')
    c = float(a[b:d])
    return c

def getkey(val):
    for key, value in scores.items():
         if val == value:
             return key

def isolatelink(lin):
    first = lin.index('(')
    second = lin.index(')')
    return lin[first+1:second]

def few(text):
    return text.rfind('https://', 0, text.rfind('https://'))

def isolatelinkl(lin):
    ff = lin.rfind('https://')
    second = lin.rfind('_')
    k = lin[ff+1:second]
    return k




if answer == 'crosspos ':
    clist = []
    result = cc.search(search, sort='new', limit=500)
    compare = posted.new(limit=100)
        
    for submission in compare:
        if 'Pro-' in submission.title or 'Con-' in submission.title:
            try:
                if submission.is_self!=True:
                    clist.append(reddit.submission(url=submission.url).id)
                else:
                    clist.append(reddit.submission(url=isolatelink(submission.selftext)).id)
            except:
                pass

            
    result = cc.search(search, sort='new', limit=500)
    for submission in result:
        print(submission.title)
        if submission.id not in clist:
            content = 'A [Cointest thread](' + 'https://old.reddit.com' + str(submission.permalink) + ') with the title above was submitted by CointestAdmin on r/CryptoCurrency. \n \n Use __this post__ to help organize judging. Rate arguments on a scale of 1 to 10. Add the scores given from all the judges to determine the winner. \n \n Administrators who participated in the linked thread must recuse themselves from judging.'           
            made = posted.submit(submission.title, content)
            print('posted')
            made.mod.flair(flair_template_id='da856a0e-1529-11ec-be69-d6749aa5e15f')

if answer == 'crosspost':
    clist = []
    result = cc.search(search, sort='new', limit=500)
    compare = posted.new(limit=100)
        
    for submission in compare:
        if 'Pro-' in submission.title or 'Con-' in submission.title:
            try:
                if submission.is_self!=True:
                    clist.append(reddit.submission(url=submission.url).id)
                else:
                    clist.append(reddit.submission(url=isolatelink(submission.selftext)).id)
            except:
                pass
            
    cc = reddit.redditor('CointestAdmin').submissions.new(limit=500)
    for submission in cc:
        if submission.id not in clist and submission.subreddit == 'CryptoCurrency' and 'r/CC Cointest' in submission.title and '2021' in submission.title:
            print(submission.title)
            content = 'A [Cointest thread](' + 'https://old.reddit.com' + str(submission.permalink) + ') with the title above was submitted by CointestAdmin on r/CryptoCurrency. \n \n Use __this post__ to help organize judging. Rate arguments on a scale of 1 to 10. Add the scores given from all the judges to determine the winner. \n \n Administrators who participated in the linked thread must recuse themselves from judging.'           
            made = posted.submit(submission.title, content)
            print('posted')
            made.mod.flair(flair_template_id='da856a0e-1529-11ec-be69-d6749aa5e15f')
    cc = reddit.redditor('CryptoChief').submissions.new(limit=500)
    for submission in cc:
        if submission.id not in clist and submission.subreddit == 'CryptoCurrency' and 'r/CC Cointest' in submission.title and '2021' in submission.title:
            print(submission.title)
            content = 'A [Cointest thread](' + 'https://old.reddit.com' + str(submission.permalink) + ') with the title above was submitted by CointestAdmin on r/CryptoCurrency. \n \n Use __this post__ to help organize judging. Rate arguments on a scale of 1 to 10. Add the scores given from all the judges to determine the winner. \n \n Administrators who participated in the linked thread must recuse themselves from judging.'           
            made = posted.submit(submission.title, content)
            print('posted')
            made.mod.flair(flair_template_id='da856a0e-1529-11ec-be69-d6749aa5e15f')



if answer == 'cop':
    result = posted.new(limit=80)
    for x in result:
        flair = x.link_flair_text
        if flair == 'Awaiting Submissions':
            slink = isolatelink(str(x.selftext)).replace('old.','www.')
            submission = reddit.submission(url=slink)
            flr = submission.link_flair_text
            if flr != 'CONTEST-CLOSED' or flr == 'CONTEST-LOCKED':
                print(submission.title)
                submission.comments.replace_more(limit=0)
                for comment in submission.comments:
                    if len(str(comment.body)) >= 500 and str(comment.author) != 'AutoModerator':
                        new = ''
                        co = str(comment.body)
                        for line in io.StringIO(co):
                            new = new + '> ' + line
                        c = 'u/' + str(comment.author) + ' \n \n ' + new + ' \n \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_'
                        try:
                            sk = x.reply(c)
                        except:
                            sk = x.reply('The submission was too long, so this is its link: \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_')
                        time.sleep(0.3)

                        for reply in comment.replies:
                            if str(reply.author)==str(comment.author):
                                ok = sk.reply(reply.body)
                            for repl in reply.replies:
                                if str(repl.author)==str(reply.author):
                                    ok.reply(repl.body)
                #x.mod.flair(flair_template_id='ecac4216-1529-11ec-ad2f-d6b7da15d7f5')
                
if answer == 'copi':
    while True:
        result = posted.new(limit=100)
        for x in result:
            flair = x.link_flair_text
            if flair == 'Awaiting Submissions':
                link = isolatelink(x.selftext).replace('old', 'www')
                submission = reddit.submission(url=link)
                submission.comments.replace_more(limit=0)
                x.comments.replace_more(limit=0)
                cs = [comment.body for comment in x.comments]
                ccs = []
                for comment in x.comments:
                    for reply in comment.replies:
                        ccs.append(reply.body)
                cs = ccs + cs
                cs = ' '.join(cs)
                for comment in submission.comments:
                    if comment.body[30:120] not in cs.replace('> ','') and len(comment.body) > 500 and str(comment.author) != 'AutoModerator':
                        new = ''
                        co = str(comment.body)
                        for line in io.StringIO(co):
                            new = new + '> ' + line
                        c = 'u/' + str(comment.author) + ' \n \n ' + new + ' \n \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_'
                        try:
                            sk = x.reply(c)
                        except:
                            sk = x.reply('The submission was too long, so this is its link: \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_')
                        reportDiscordEntry(str(comment.author), submission.title, sk.permalink)
                        time.sleep(60)
                        for reply in comment.replies:
                            if reply.body not in cs and str(reply.author)==str(comment.author):
                                sk.reply(reply.body)
                        sk.mod.approve()
                                                                    
                    if comment.body[30:120] in cs.replace('> ',''):
                        for ccc in x.comments:
                            og = ccc.body
                            if comment.body[30:120] in ccc.body.replace('> ', '') and comment.body not in og.replace('> ', ''):
                                new = ''
                                co = str(comment.body)
                                for line in io.StringIO(co):
                                    new = new + '> ' + line
                                c = 'u/' + str(comment.author) + ' \n \n ' + new + ' \n \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_'
                                try:
                                    sk = ccc.edit(c)
                                except:
                                    sk = ccc.edit('The submission was too long, so this is its link: \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_')


                                reportDiscordEdit(str(comment.author), submission.title, sk.permalink)
                                time.sleep(2)
                                
                    f = submission.link_flair_text
                    if f == 'CONTEST-CLOSED' or f == 'CONTEST-LOCKED':
                        x.mod.flair(flair_template_id='ecac4216-1529-11ec-ad2f-d6b7da15d7f5')
                        
if answer == 'copy':
    while True:
        result = posted.new(limit=100)
        for x in result:
            flair = x.link_flair_text
            if flair == 'Awaiting Submissions':
                link = isolatelink(x.selftext).replace('old', 'www')
                submission = reddit.submission(url=link)
                submission.comments.replace_more(limit=0)
                x.comments.replace_more(limit=0)
                cauthors = []
                for comment in x.comments:
                    count = 0
                    for word in comment.body.split(' '):
                        if 'u/' in word and "'" not in word and 'https:' not in word and '.com' not in word and 'http:' not in word and count <1:
                            cauthors.append(word[2:-1]+word[-1])
                            count = 1

                
                
                for comment in submission.comments:
                    if str(comment.author) not in cauthors and len(comment.body) > 500 and str(comment.author) != 'AutoModerator' and comment.banned_by == None and comment.author != None:
                        
                        new = ''
                        co = str(comment.body)
                        for line in io.StringIO(co):
                            new = new + '> ' + line
                        c = 'u/' + str(comment.author) + ' \n \n ' + new + ' \n \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_'
                        try:
                            sk = x.reply(c)
                        except:
                            time.sleep(10)
                            sk = x.reply('The submission was too long, so this is its link: \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_ \n \n Author: u/' + str(comment.author))
        
                        reportDiscordEntry(str(comment.author), submission.title, sk.permalink)
                        time.sleep(60)
                        for reply in comment.replies:
                            if str(reply.author)==str(comment.author):
                                sk.reply(reply.body)
                            for repl in reply.replies:
                                if str(repl.author)==str(reply.author):
                                    sk.reply(repl.body)
                        sk.mod.approve()

                for c in x.comments:
                    if '[deleted]' not in c.body and '[removed]' not in c.body:
                        comment = reddit.comment(url=isolatelinkl(c.body))
                        if comment.body not in c.body.replace('> ', '') and len(c.body) > 500 and comment.edited != False and str(comment.author) != 'roberthonker' and comment.banned_by == None:
                            new = ''
                            b = str(comment.body)
                            for line in io.StringIO(b):
                                new = new + '> ' + line
                            b = 'u/' + str(comment.author) + ' \n \n ' + new + ' \n \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_'
                            if b != c.body:
                                try:
                                    sk = c.edit(b)
                                except:
                                    time.sleep(10)
                                    sk = c.edit('The submission was too long, so this is its link: \n _' + 'https://old.reddit.com' + str(comment.permalink) + '_')



                                    reportDiscordEdit(str(comment.author), submission.title, sk.permalink)
                                    time.sleep(60)
                                   
                f = submission.link_flair_text
                if f == 'CONTEST-CLOSED' or f == 'CONTEST-LOCKED':
                    x.mod.flair(flair_template_id='ecac4216-1529-11ec-ad2f-d6b7da15d7f5')      
                        
                        
                    
            

if answer == 'tally':
    result = posted.new(limit=100)
    for submission in result:
        flair = submission.link_flair_text
        if flair == 'Judgement completed. Awaiting tally.':
            for comment in submission.comments:
                authors = []
                tempscore = 0
                for x in comment.replies:
                    if len(x.body) < 200:
                        score = locatenumbers(x.body)
                        if score <= 10 and 'Total' not in x.body:
                            authors.append('u/' + str(x.author))
                            tempscore+=score
                c = comment.reply('This entry has a total score of ' + str(tempscore) + '. The votes of ' + str(authors)[1:-1].replace("'", "") + ' were counted.')
                c.mod.distinguish(how="yes", sticky=True)
                time.sleep(1)
            submission.mod.flair(flair_template_id='12152162-152a-11ec-a733-c6e0af1f0894')


if answer == 'declare':
    result = posted.new(limit=100)
    fd = ''
    for submission in result:
        scores = {}
        flair = submission.link_flair_text
        if flair == 'Winner declaration done. Awaiting congratulatory message.':
            for comment in submission.comments:
                for child in comment.replies:
                    if 'This entry' in child.body and str(child.author)=='CointestAdmin':
                        scores[str(comment.id)] = locatenumber(str(child.body))
            highscores = list(scores.values())
            first = (max(highscores), getkey(max(highscores)))
            highscores.remove(max(highscores))
            second = (max(highscores), getkey(max(highscores)))
            highscores.remove(max(highscores))
            third = (max(highscores), getkey(max(highscores)))
            done = 'The 1st [submission](https://old.reddit.com' + str(reddit.comment(id=first[1]).permalink) + ') was by ' + str(reddit.comment(id=first[1]).body).split()[0] + ' and had a score of ' + str(round(first[0], 2)) + '. \n \n'
            dtwo = 'The 2nd [submission](https://old.reddit.com' + str(reddit.comment(id=second[1]).permalink) + ') was by ' + str(reddit.comment(id=second[1]).body).split()[0] + ' and had a score of ' + str(round(second[0], 2)) + '. \n \n'
            dthre = 'The 3rd [submission](https://old.reddit.com' + str(reddit.comment(id=third[1]).permalink) + ') was by ' + str(reddit.comment(id=third[1]).body).split()[0] + ' and had a score of ' + str(round(third[0], 2)) + '. \n \n'
            #final = submission.reply(done+' \n '+dtwo+' \n ' + dthre)
            #final.mod.distinguish(how="yes", sticky=True)
            time.sleep(5)
            #final.mod.approve()
            title = str(submission.title)
            title = title.replace('r/CC','CC')
            fd = fd + '# [' + title + '](https://old.reddit.com' + str(submission.permalink) + ') \n \n'
            fd = fd + done + ' \n \n'
            fd = fd + dtwo + ' \n \n'
            fd = fd + dthre + ' \n \n'
            #submission.mod.flair(flair_template_id='46c7282e-152a-11ec-be30-be04b0884f0c')
            
    fd = fd + ' \n # Best Analysis  \n u/elrond4 had the best analysis for this round in their BTC Pro-Arguments entry, with an average score of 10.0 \n PING!'        
    posted.submit(title='Cointest Winner Declaration Thread', selftext=fd)


if answer == 'congratulate':
    result = posted.new(limit=100)
    for submission in result:
        flair = submission.link_flair_text
        if flair == 'Winner declaration done. Awaiting congratulatory message.':
            for comment in submission.comments:
                if 'and had a score of' in comment.body:
                    for line in io.StringIO(comment.body):
                        try:
                            slink = isolatelink(line).replace('old.','www.')
                            body = reddit.comment(url=slink)
                            lastline = body.body.splitlines()[-1]
                            lastline = lastline.replace('_','')
                            lastline = lastline.replace('old.','www.')
                            lastline = lastline.replace(' ','')
                            ogcomment = reddit.comment(url=lastline)
                            if '1st' in line:
                                ogcomment.reply('Greetings, u/' + str(ogcomment.author) + '. You have been selected as the 1st place winner for this thread in the r/CC Cointest. Your prize will be a tip of 300 moons and corresponding trophy flair. Congratulations!')
                            if '2nd' in line:
                                ogcomment.reply('Greetings, u/' + str(ogcomment.author) + '. You have been selected as the 2nd place winner for this thread in the r/CC Cointest. Your prize will be a tip of 150 moons and corresponding trophy flair. Congratulations!')
                            if '3rd' in line:
                                ogcomment.reply('Greetings, u/' + str(ogcomment.author) + '. You have been selected as the 3rd place winner for this thread in the r/CC Cointest. Your prize will be a tip of 75 moons and corresponding trophy flair. Congratulations!')
                        except ValueError:
                            pass
            submission.mod.flair(flair_template_id='df8fb0c6-152a-11ec-a9d4-c25bc28b6afb')
            
                

        
        
        



        
        
        
        











