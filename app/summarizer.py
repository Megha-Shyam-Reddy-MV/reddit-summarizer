from openai import OpenAI

from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_reddit_thread(data):

    comments_text = "\n\n".join([
        f"""
        Comment:
        {comment["body"]}

        Score:
        {comment["score"]}
        """
        for comment in data["comments"]
    ])

    prompt = f"""
    Summarize this Reddit discussion.

    POST TITLE:
    {data["title"]}

    POST CONTENT:
    {data["post_text"]}

    COMMENTS:
    {comments_text}

    Return:
    1. Overall Summary
    2. Main Positive Opinions
    3. Main Negative Opinions
    4. Community Consensus
    5. Most Interesting Insights
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content