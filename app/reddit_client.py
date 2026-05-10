import requests


def fetch_post_and_comments(url: str):

    if not url.endswith(".json"):
        url = url.rstrip("/") + ".json"

    headers = {
        "User-Agent": "Mozilla/5.0 RedditSummarizerBot/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    if response.status_code != 200:

        raise Exception(
            f"Failed to fetch Reddit post: {response.status_code}"
        )

    data = response.json()

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