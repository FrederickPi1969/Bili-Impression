import src.backend.database.mongoDB as Database
from flask import Flask
from flask import request
from flask import abort
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS
import src.backend.database.mongoDB as db
import src.backend.scraper.scraper as scraper

app = Flask(__name__)
cors = CORS(app)


def scrape(qs_parsed):
    return scraper.start_scraping(qs_parsed["keyword"][0], int(qs_parsed["maxPage"][0]), int(qs_parsed["maxVideos"][0]),
                                           qs_parsed["rankOpt"][0], qs_parsed["tidOpt"][0], qs_parsed["sortOpt"][0])


@app.route("/scraper/comments/", methods=["GET"])
def comments():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    print(qs_parsed)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    result = scrape(qs_parsed)[1]
    all_comments = {}
    for items in result:
        value = result[items]
        comment = value["comment_list"]
        all_comments[items] = comment
    return all_comments


@app.route("/scraper/tags/", methods=["GET"])
def tags():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    result = scrape(qs_parsed)[1]
    all_tags = {}
    for items in result:
        value = result[items]
        tag = value["tags"]
        all_tags[items] = tag
    return all_tags


@app.route("/scraper/danmaku/", methods=["GET"])
def danmaku():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    result = scrape(qs_parsed)[1]
    all_danmaku = {}
    for items in result:
        value = result[items]
        danmaku_file = value["comment_list"]
        all_danmaku[items] = danmaku_file
    return all_danmaku


@app.route("/scraper/commentersInfo/", methods=["GET"])
def commenters_info():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    result = scrape(qs_parsed)[1]
    all_commenters = {}
    for items in result:
        value = result[items]
        uploader = value["sex-list"]
        all_commenters[items] = uploader
    return all_commenters


@app.route("/scraper/videoInfo/", methods=["GET"])
def video_info():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    return scrape(qs_parsed)[0]


@app.route("/visualization/wordCloud/", methods=["GET"])
def word_cloud():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    abort(400, "This function is not online now")


@app.route("/visualization/sexDistribution/", methods=["GET"])
def sex_distribution():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    abort(400, "This function is not online now")


@app.route("/visualization/topUploaders/", methods=["GET"])
def top_uploaders():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    abort(400, "This function is not online now")


@app.route("/visualization/popularityVariation/", methods=["GET"])
def popularity():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    abort(400, "This function is not online now")


@app.route("/visualization/knowledgeGraph/", methods=["GET"])
def knowledge_graph():
    print(request.url)
    url_parsed = urlparse(request.url)
    qs_parsed = parse_qs(url_parsed.query)
    if qs_parsed == {} or len(qs_parsed) != 6 or not qs_parsed["maxPage"][0].isnumeric() \
            or not qs_parsed["maxVideos"][0].isnumeric() or not qs_parsed["rankOpt"][0].isnumeric() \
            or not qs_parsed["tidOpt"][0].isnumeric() or not qs_parsed["sortOpt"][0].isnumeric():
        """ Empty keyword or incomplete/non-numeric scrape options """
        abort(400, "Bad Request: illegal scrape ")
    elif not 0 <= int(qs_parsed["maxPage"][0]) <= 20 or not 0 <= int(qs_parsed["rankOpt"][0]) <= 4 \
            or not 0 <= int(qs_parsed["tidOpt"][0]) <= 18 or not 0 <= int(qs_parsed["sortOpt"][0]) <= 2:
        """ Invalid scrape options: out of bound """
        abort(400, "Bad Request")
    abort(400, "This function is not online now")


if __name__ == "__main__":
    app.run()
