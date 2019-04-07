# -*- coding:utf-8 -*-
import json, config
from requests_oauthlib import OAuth1Session


def main():
    ck = config.CONSUMER_KEY
    cs = config.CONSUMER_SECRET
    at = config.ACCESS_TOKEN
    ats = config.ACCESS_TOKEN_SECRET
    my_session = OAuth1Session(ck, cs, at, ats)

    # search(search_words, my_session)
    # get_timeline(my_session)
    post_tweet("テストツイット2", my_session)


def search(words, session):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    for word in words:
        params = {'q':  word, 'count': 100}

        req = session.get(url, params=params)

        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            for tweet in search_timeline['statuses']:
                # do something
                    delete_tweet(tweet, session)
        else:
            print("ERROR: %d" % req.status_code)


def get_timeline(session):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    params = {'count': 200, 'include_rts': 'false'}
    req = session.get(url, params=params)

    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:
            # do something
            if tweet['source'] == source_string:
                delete_tweet(tweet, session)
    else:
        print("ERROR: %d" % req.status_code)


def delete_tweet(tweet, session):
    url = "https://api.twitter.com/1.1/statuses/destroy/"+tweet['id_str']+".json"
    req = session.post(url)
    if req.status_code == 200:
        print("delete success!")
    else:
        print("ERROR: %d" % req.status_code)


def post_tweet(sentence, session):
    url = "https://api.twitter.com/1.1/statuses/update.json"

    params = {"status": sentence}

    req = session.post(url, params=params)

    if req.status_code == 200:
        print("Succeed!")
    else:
        print("ERROR : %d" % req.status_code)


if __name__ == "__main__":
    source_string = "<a href=\"http://granbluefantasy.jp/\" rel=\"nofollow\">グランブルー ファンタジー</a>"
    search_words = ["スマホRPG", "参加者募集", "#みんなで早押しクイズ"]
    main()
