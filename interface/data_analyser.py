#! /usr/bin/env python -u
# coding=utf-8
import StringIO
import csv
import datetime
import dateutil.parser
import math

__author__ = 'xl'


def read_instagram():
    ret = []
    with open("instagram.csv", "r") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            record = {
                "date": datetime.datetime.strptime(row["date"], "%Y-%m-%d").date(),
                "like_count": int(row["like_count"]),
                "img": row["src"]
            }
            ret.append(record)
    return ret


def read_health():
    ret = []
    with open("Health Data.csv", "r") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            record = {
                "date": datetime.datetime.strptime(row["Start"], "%d-%b-%Y 00:00").date(),
                "steps": float(row["Steps (count)"])
            }
            ret.append(record)
    return ret


def normalized(data):
    activity_range = 5
    awesomeness_range = 10

    size = len(data)

    activity_sum = sum([row["activity"] for row in data])
    awesomeness_sum = max([row["awesomeness"] for row in data])

    ret = data
    for row in ret:
        row["activity"] = 1.0 * row["activity"] / activity_sum * (100.0 - activity_range * size) + activity_range
        row["awesomeness"] = 1.0 * row["awesomeness"] / awesomeness_sum * (
            100.0 - awesomeness_range) + awesomeness_range if awesomeness_sum != 0 else awesomeness_range

    return ret


def get_data(year, month, day, day_range=7):
    photo_data = {row["date"]: row for row in read_instagram()}
    activity_data = {row["date"]: row for row in read_health()}

    target_date = datetime.date(year, month, day)
    cur_date = target_date

    ret = []
    while cur_date < target_date + datetime.timedelta(day_range):
        record = {}
        record["date"] = cur_date
        record["activity"] = activity_data[cur_date]["steps"] if cur_date in activity_data else 0
        record["awesomeness"] = photo_data[cur_date]["like_count"] if cur_date in photo_data else 0
        record["img"] = photo_data[cur_date]["img"] if cur_date in photo_data else ''
        ret.append(record)
        cur_date = cur_date + datetime.timedelta(1)

    ret = normalized(ret)
    return ret


def get_data_csv(year, month, day, day_range=7):
    data = get_data(year, month, day, day_range)

    output = StringIO.StringIO()
    wr = csv.writer(output)
    wr.writerow(data[0].keys())
    for record in data:
        wr.writerow(record.values())

    return output.getvalue()


if __name__ == "__main__":
    print read_instagram()
    print read_health()


def get_records(start, end):
    ret = []
    start = start if start is datetime else dateutil.parser.parse(start)
    end = end if end is datetime else dateutil.parser.parse(end)
    days = math.ceil((end - start).days / 7.0) * 7
    data = get_data(start.date().year, start.date().month, start.date().day, days)
    max_radius_frac = max([row['awesomeness'] for row in data])
    max_radius_frac = max_radius_frac if max_radius_frac > 0 else 1
    max_width = 500

    index = 0
    while index < len(data):
        ratio = max([row['awesomeness'] for row in data[index:index + 7]]) / max_radius_frac

        row = {
            'date': data[index]['date'].isoformat(),
            'width': max_width * ratio,
            'height': max_width * ratio,
            'radius': (max_width / 2 - 5) * ratio
        }
        ret.append(row)
        index += 7

    return ret