from django.shortcuts import render, redirect
from django.views.generic import View
from datetime import datetime, date
from django.utils.timezone import localtime
from django.conf import settings
import requests
import json
import math
import pandas as pd



# Instagram Graph APIの認証情報を取得する関数
def get_credentials():
    credentials = {}
    credentials['access_token'] = settings.ACCESS_TOKEN
    credentials['instagram_account_id'] = settings.INSTAGRAM_ACCOUNT_ID
    credentials['graph_domain'] = 'https://graph.facebook.com/'
    credentials['graph_version'] = 'v13.0'
    credentials['endpoint_url'] = credentials['graph_domain'] + credentials['graph_version'] + '/'
    credentials['Ig_username'] = xxxxxxxxxxxx # 自分のアカウントID
    return credentials



# Instagram Graph APIを呼び出す関数
def call_api(url, endpoint_params):
    # APIを送信
    data = requests.get(url, endpoint_params)
    response = {}
    # API送信結果をJSON形式で保存
    response['json_data'] = json.loads(data.content)
    return response


# ユーザーのアカウント情報を取得する関数
def get_account_info(params):
    # エンドポイント
    # https://graph.facebook.com/{graph-api-version}/{ig-user-id}?fields={fields}&access_token={access-token}

    endpoint_params = {}
    # ユーザ名、プロフィール画像、フォロワー数、フォロー数、投稿数、メディア情報を取得
    endpoint_params['fields'] = 'business_discovery.username(' + params['ig_username'] + '){\
        username,profile_picture_url,follows_count,followers_count,media_count,\
        media.limit(10){comments_count,like_count,caption,media_url,permalink,timestamp,media_type,\
        children{media_url,media_type}}}'
    endpoint_params['access_token'] = params['access_token']
    url = params['endpoint_base'] + params['instagram_account_id']
    return call_api(url, endpoint_params)



# それぞれの関数を実行するクラス
class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Instagram Graph APIの認証情報を取得
        params = get_credentials()
        # アカウントの情報を取得
        account_response = get_account_info(params)
        business_discovery = account_response['json_data']['business_discovery']
        print(business_discovery)
