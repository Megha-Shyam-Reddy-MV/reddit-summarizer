import requests
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": "Mozilla/5.0 RedditSummarizerBot/1.0"
}


def normalize_reddit_url(url: str):

    response = requests.get(
        url,
        headers=HEADERS,
        allow_redirects=True,
        timeout=20
    )

    return response.url


def build_json_url(url: str):

    normalized_url = normalize_reddit_url(url)

    parsed = urlparse(normalized_url)

    path = parsed.path.rstrip("/")

    return f"https://old.reddit.com{path}.json"


def fetch_post_and_comments(url: str):

    json_url = build_json_url(url)

    response = requests.get(
        json_url,
        headers=HEADERS,
        timeout=20
    )

    if response.status_code != 200:

        raise Exception(
            f"Failed to fetch Reddit JSON: {response.status_code}"
        )

    try:

        data = response.json()

    except Exception:

        print(response.text)

        raise Exception(
            "Reddit returned invalid JSON"
        )

    post_data = data[0]["data"]["children"][0]["data"]

    comments = []

    for comment in data[1]["data"]["children"]:

        if comment["kind"] != "t1":
            continue

        comment_data = comment["data"]

        body = comment_data.get("body")

        if not body:
            continue

        comments.append({
            "body": body,
            "score": comment_data.get("score", 0)
        })

    return {
        "title": post_data.get("title", ""),
        "post_text": post_data.get("selftext", ""),
        "comments": comments[:50]
    }