# -*- coding:utf-8 -*-
import json
import os
import sys
from requests_oauthlib import OAuth1Session
import psycopg2.extras


def main():
    cur_select = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur_update = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur_select.execute("select * from token")
    for row in cur_select:
        at = row['access_token']
        ats = row['access_token_secret']
        session = OAuth1Session(ck, cs, at, ats)
        status_code, screen_name = get_user_screen_name(session)
        if screen_name is None:
            if status_code == 401:
                cur_update.execute("delete from token where id = %s", (row['id'],))
            continue
        cur_update.execute("update token set screen_name = %s where id = %s", (screen_name, row['id']))
        # result = search(screen_name, search_words, session)
        # delete_auto_tweets(result, session)
        tweets = get_timeline(session)
        delete_gbf_tweets(tweets, session)
        # delete_selected_tweets(tweets, session)
        if screen_name == owner:
            post_tweet("削除成功", session)
    conn.commit()
    conn.close()


# ツイート検索
def search(id_str, words, session):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    search_result = []
    for word in words:
        print(word+" from:"+id_str)
        params = {'q':  word+" from:"+id_str, 'count': 100}

        req = session.get(url, params=params)

        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            search_result.append(search_timeline)

        else:
            print("ERROR: %d" % req.status_code)
    return search_result


# ユーザーのスクリーンネーム取得
def get_user_screen_name(session):
    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    req = session.get(url)
    if req.status_code == 200:
        user_info = json.loads(req.text)
        print(user_info['screen_name'])
        return req.status_code, user_info['screen_name']
    else:
        print("ERROR: %d" % req.status_code)
        return req.status_code, None


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
        if tweet['source'] in source_strings:
            for word in search_words:
                if word in tweet['text']:
                    print(tweet['text'])
                    delete_tweet(tweet, session)
                    break


# 対象文字列が含まれるツイートを削除
def delete_selected_tweets(tweets, session):
    for tweet in tweets:
        for word in search_words:
            if word in tweet['text']:
                print(tweet['text'])
                delete_tweet(tweet, session)
                break


# 検索結果のツイートをすべて削除
def delete_auto_tweets(result, session):
    for tweets in result:
        for tweet in tweets['statuses']:
            print(tweet['text'])
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


# 検索文字列ファイルの読み込み
def read_search_words(txt_path):
    with open(txt_path, 'r') as f:
        text_list = f.read().split('\n')
        search_words_list = []
        source_strings_list = []
        mode = 0
        for s in text_list:
            if s == 'search_words':
                mode = 0
            elif s == 'source_strings':
                mode = 1
            elif mode == 0:
                search_words_list.append(s)
            elif mode == 1:
                source_strings_list.append(s)

    return search_words_list, source_strings_list


if __name__ == "__main__":
    # 手元かどうか判定
    if len(sys.argv) > 2:
        import config
        ck = config.CONSUMER_KEY
        cs = config.CONSUMER_SECRET
        conn = psycopg2.connect("dbname=%s host=localhost user=%s" % (config.DB_NAME, config.DB_USER))
    else:
        ck = os.environ['CONSUMER_KEY']
        cs = os.environ['CONSUMER_SECRET']
        db_url = os.environ['DATABASE_URL']
        conn = psycopg2.connect(db_url, sslmode='require')

    words_txt_path = sys.argv[1]
    search_words, source_strings = read_search_words(words_txt_path)
    owner = 'gikolarge'
    print(search_words)
    print(source_strings)

    main()
