import praw
import time
import io
emp = []


reddit = praw.Reddit(client_id='XGXe8jL8VNnKaTWKuaI05w', \
                     client_secret='c7qatNw4QWMBXuzPBjaeb9dFoMyoDA', \
                     user_agent='CointestMaster', \
                     refresh_token='1039453707688-_9VabNb5veb7IfsfWYqZHyNV0vN86Q', \
                     redirect_url='http://localhost:8080')

cc = reddit.subreddit('CointestBot')

triggers = {'Bitcoin':'bitcoin ,btc ,satoshi ,bitcorn ', 'Ethereum':'ethereum ,eth ,vitalik ', 'Tether':'tether ,bitfinex ,usdt ', 'Binance Coin':'bnb ,binance ', 'Cardano':'cardano ,ada ', 'Dogecoin':'dogecoin ,doge ',
            'USD Coin':'usdc ,circle ', 'Solana':'solana ,sol ', 'Polkadot':'polkadot ,dot ,kusama ', 'Ripple':'ripple ,xrp ', 'Algorand':'algorand ,algo ,algonauts ', 'Bitcoin Cash':'bch ', 'Internet Computer':'icp ',
            'IOTA':'miota iota', 'Litecoin':'litecoin ltc', 'Monero':'monero xmr boating', 'Moons':'moons moon', 'NANO':'nano', 'Safemoon':'safemoon', 'Shiba Inu':'shiba shib inu', 'DAG':'acrylic dag',
            'DEX':'dex ', 'ETF':'etf ', 'Inflation':'inflation ,venezuela ', 'Lightning Network':'ln ,lightning ', 'NFT':'nft ,fungible ', 'Privacy':'privacy ,private ,public ', 'Proof Of Stake':'staking ,pos ',
            'Proof Of Work':'pow ', 'Regulation':'sec ,regulation ,regulate ,regulatory '}

cor = {'Bitcoin':'btc', 'Ethereum':'eth', 'Tether':'usdt', 'Binance Coin':'bnb', 'Cardano':'ada', 'Dogecoin':'doge', 'USD Coin':'usdc', 'Solana':'SOL', 'Polkadot':'dot', 'Ripple':'xrp', 'Algorand':'algo', 'Bitcoin Cash':'bch',
        'Internet Computer':'icp', 'IOTA':'iota', 'Litecoin':'LTC', 'Monero':'xmr', 'Moons':'moon', 'Nano':'nano', 'Safemoon':'safemoon', 'Shiba Inu':'shib', 'DAG':'dag', 'DEX':'dex', 'ETF':'etf', 'Inflation':'inflation',
       'Lightning Network':'ln', 'NFT':'nft', 'Privacy':'privacy', 'Proof Of Stake':'pos', 'Proof Of Work':'pow', 'Regulation':'regulation'}

hot = cc.hot(limit=50)

for submission in hot:
    if submission.num_comments > 1:
        if str(list(submission.comments)[0].author) != 'CointestAdmin' and submission.is_self == True:
            total = submission.title + submission.selftext
            total = total.lower()
            scores = []
            for key, value in triggers.items():
                temp = 0
                for element in value.split(','):
                    if element in total:
                        temp += total.count(element)
                scores.append(temp)
                
            flr = submission.link_flair_text
            if sum(scores) != 0  and flr != 'COMEDY' and submission.distinguished == None:
                ind = scores.index(max(scores))
                relevant = list(triggers)[ind]
                comment = '''* '''+relevant+''' [Pros](https://old.reddit.com/r/CryptoCurrency/wiki/cointest_archive#wiki_'''+cor[relevant]+'''_pros) & [Cons](https://old.reddit.com/r/CryptoCurrency/wiki/cointest_archive#wiki_'''+cor[relevant]+'''_cons) - Participate in the r/CC [Cointest](https://old.reddit.com/r/CryptoCurrency/wiki/cointest_policy) to potentially win moons. Prize allocations: 1st - 300, 2nd - 150, 3rd - 75.
* If you have a strong opinion on this topic, you may want to participate in the Cointest! Your knowledge can benefit others while you may get rewarded, too.
* You can sort comments as controversial by clicking [here](https://reddit.com/'''+submission.permalink+'''?sort=controversial). Unfortunately, it does not work on mobile.'''
                c = submission.reply(comment)
                c.mod.distinguish(sticky=True)
