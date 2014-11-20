#! /usr/bin/env python -u
# coding=utf-8
from collections import OrderedDict
import csv
import json
import webbrowser
import datetime
from instagram.client import InstagramAPI
import jsonpickle
from os import system

__author__ = 'xl'

client_id = "158a1eba85c94f359ef2a5034299b2ba"
client_secret = "21042e11db6144639cae8d389d07f6e7"
redirect_url = "http://localhost:31337/"
auth_url = "https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code"
access_token = "df80d53bd27142b0881f543df4e2522c"


def auth():
    webbrowser.open_new(auth_url % (client_id, redirect_url))

# api = InstagramAPI(access_token=access_token)
api = InstagramAPI(client_id=client_id, client_secret=client_secret)


def download_users(id="12"):
    ret = []
    next_ = ""
    while True:
        recent_media, next_ = api.user_recent_media(user_id=id, with_next_url=next_)
        for media in recent_media:
            ret.append(media)
            print media.images["standard_resolution"] if media.type == 'image' else "Video!"
            print
        if not next_:
            break
    with open("imgs.json", "w") as fp:
        fp.write(jsonpickle.encode(ret))
    return ret


def download_pics():
    system('mkdir imgs')
    with open("imgs.json", "r") as fp:
        records = jsonpickle.decode(fp.read())

    for media in records:
        print media.images["standard_resolution"].url
        url = media.images["standard_resolution"].url
        system('cd imgs; curl -O "%s"' % url)


def process_list():
    with open("imgs.json", "r") as fp:
        records = jsonpickle.decode(fp.read())

    ret = []
    for media in records:
        row = {
            "created_time": media.created_time,
            "src": media.images["standard_resolution"].url.split('/')[-1],
            "like_count": media.like_count,
            "comment_count": media.comment_count
        }
        ret.append(row)

    return ret


def generate_dict(records):
    ret = []
    date = min([row['created_time'] for row in records])
    max_date = max([row['created_time'] for row in records])
    while date <= max_date:
        items = [row for row in records if row["created_time"].date() == date.date()]
        row = OrderedDict()
        row['date'] = date.date()
        row["src"] = items[0]["src"] if len(items) > 0 else "none.jpg"
        row["like_count"] = sum([item["like_count"] for item in items])
        row["comment_count"] = sum([item["comment_count"] for item in items])

        ret.append(row)
        date += datetime.timedelta(1)

    return ret

def save_as_csv(data):
    with open("instagram.csv","w") as fp:
        wr = csv.writer(fp)
        wr.writerow(data[0].keys())
        for record in data:
            wr.writerow(record.values())

if __name__ == '__main__':
    # auth()
    # print api.user_search("xldrx")
    # download_users("215713069")
    data = generate_dict(process_list())
    save_as_csv(data)