import requests

HEADERS = {
    "User-Agent": "reddit-comment-summarizer"
}

def fetch_post_and_comments(url: str):

    if not url.endswith(".json"):
        url = url.rstrip("/") + ".json"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch Reddit post: {response.status_code}"
        )

    data = response.json()

    post = data[0]["data"]["children"][0]["data"]

    comments_raw = data[1]["data"]["children"]

    comments = []

    for comment in comments_raw:

        if comment["kind"] != "t1":
            continue

        comment_data = comment["data"]

        body = comment_data.get("body", "")

        if body in ["[deleted]", "[removed]"]:
            continue

        if len(body.strip()) < 30:
            continue

        comments.append({
            "author": comment_data.get("author"),
            "body": body,
            "score": comment_data.get("score", 0)
        })

    comments = sorted(
        comments,
        key=lambda x: x["score"],
        reverse=True
    )
    return {
        "title": post.get("title"),
        "post_text": post.get("selftext", ""),
        "comments": comments[:100]
    }