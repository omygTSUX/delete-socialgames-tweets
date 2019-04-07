# -*- coding:utf-8 -*-
import json
import os
from requests_oauthlib import OAuth1Session


def main():
    ck = os.environ['CONSUMER_KEY']
    cs = os.environ['CONSUMER_SECRET']
    at = os.environ['ACCESS_TOKEN']
    ats = os.environ['ACCESS_TOKEN_SECRET']
    my_session = OAuth1Session(ck, cs, at, ats)

    # result = search(search_words, my_session)
    # delete_auto_tweets(result, my_session)
    tweets = get_timeline(my_session)
    delete_gbf_tweets(tweets, my_session)
    # post_tweet("テスト", my_session)


# ツイート検索
def search(words, session):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    search_result = []
    for word in words:
        params = {'q':  word, 'count': 100}

        req = session.get(url, params=params)

        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            search_result.append(search_timeline)

        else:
            print("ERROR: %d" % req.status_code)
        return search_result


# 自分のツイート取得
def get_timeline(session):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    params = {'count': 200, 'include_rts': 'false'}
    req = session.get(url, params=params)

    if req.status_code == 200:
        timeline = json.loads(req.text)
        return timeline
    else:
        print("ERROR: %d" % req.status_code)
        exit()


# グラブルから送信されたツイートの削除
def delete_gbf_tweets(tweets, session):
    for tweet in tweets:
        if tweet['source'] == source_string:
            delete_tweet(tweet, session)


# 検索結果のツイートをすべて削除
def delete_auto_tweets(result, session):
    for tweets in result:
        for tweet in tweets:
            delete_tweet(tweet, session)


# 指定したツイートの削除
def delete_tweet(tweet, session):
    url = "https://api.twitter.com/1.1/statuses/destroy/"+tweet['id_str']+".json"
    req = session.post(url)
    if req.status_code == 200:
        print("delete success!")
    else:
        print("ERROR: %d" % req.status_code)


# ツイートをする
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
