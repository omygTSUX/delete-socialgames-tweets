import os
import oauth2 as oauth
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

request_token_url = 'https://twitter.com/oauth/request_token'
access_token_url = 'https://twitter.com/oauth/access_token'
authenticate_url = 'https://twitter.com/oauth/authorize'
callback_url = 'https://delete-socialgames-tweets.herokuapp.com'
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']


# リクエストトークンを取得する関数
def get_request_token():
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    resp, content = client.request('%s?&oauth_callback=%s' % (request_token_url, callback_url))
    content = content.decode('utf-8')
    request_token = dict(parse_qsl(content))
    return request_token['oauth_token']


# 成型
def parse_qsl(url):
    param = {}
    try:
        for i in url.split('&'):
            _p = i.split('=')
            param.update({_p[0]: _p[1]})
    except:
        param['oauth_token'] = 'failed'
        param['oauth_token_secret'] = 'failed'
    return param


# アクセストークンを取得する関数
def get_access_token(oauth_token, oauth_verifier):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(oauth_token, oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request("https://api.twitter.com/oauth/access_token", "POST", body="oauth_verifier={0}".format(oauth_verifier))
    return content


@app.route("/")
def check_token():
    oauth_token = request.args.get('oauth_token', default="failed", type=str)
    oauth_verifier = request.args.get('oauth_verifier', default="failed", type=str)

    if oauth_token != "failed" and oauth_verifier != "failed":
        response = get_access_token(oauth_token, oauth_verifier).decode('utf-8')
        response = dict(parse_qsl(response))
        oauth_token = response['oauth_token']
        oauth_token_secret = response['oauth_token_secret']
        db_url = os.environ['DATABASE_URL']
        conn = psycopg2.connect(db_url, sslmode='require')
        cur = conn.cursor()
        cur.execute("insert into token (access_token, access_token_secret) values (%s, %s)", (oauth_token, oauth_token_secret))
        conn.commit()
        return render_template('cer.html', url="NoNeed")
    else:
        # リクエストトークンを取得する
        request_token = get_request_token()
        authorize_url = '%s?oauth_token=%s' % (authenticate_url, request_token)
        print(authorize_url)
        return render_template('cer.html', url=authorize_url, res="NoParams")
