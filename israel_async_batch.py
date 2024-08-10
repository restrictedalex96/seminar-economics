import asyncpraw
import datetime as dt
import json
import asyncio

CLIENT_SECRET = ""
CLIENT_ID = ""
import logging

logger = logging.getLogger("asyncpraw")

logger = logging.getLogger("praw")
logger.setLevel(logging.DEBUG)

class Post:
    def __init__(self, title, date, likes_count, confidence):
        self.title = title
        self.date = date
        self.likes_count = likes_count
        self.confidence = confidence


def calculate_confidence(post_title):
    high_confidence_keywords = ["jihad", "hamas", "idf"]
    moderate_confidence_keywords = ["war", "casualti", "bomb", "killed", "murder", "famine", "starvation", "boycott",
                                    "resistance", "aid", "terror", "attack", "october 7th", "invaded"]
    if any(keyword in post_title for keyword in high_confidence_keywords):
        return 1.0
    elif "israel" in post_title and "palestine" in post_title:
        return 1.0
    elif ("israel" in post_title or "palestine" in post_title) and any(
            keyword in post_title for keyword in moderate_confidence_keywords):
        return 0.9
    elif "israel" in post_title or "palestine" in post_title:
        return 0.5
    return 0



counter = 0

async def main(subreddit_name: str):
    print("Starting")

    reddit = asyncpraw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="Python",
        ratelimit_seconds=5
    )

    subreddit = await reddit.subreddit(subreddit_name)

    start_date = dt.datetime(2023, 10, 5)
    end_date = dt.datetime.now()
    all_posts = []
    global counter
    async for submission in subreddit.all(limit=1000000):
        counter += 1
        print(counter)

        submission_date = dt.datetime.fromtimestamp(submission.created_utc)
        if submission_date < start_date:
            break
        post_title = submission.title.lower()
        confidence = calculate_confidence(post_title)
        if confidence > 0:
            post = Post(submission.title, submission_date, submission.score, confidence)
            all_posts.append(post)

    # Dump the data_old to a file
    with open(f'{subreddit_name}_israel_palestine.jsonl', 'w') as file:
        for post in all_posts:
            json_record = json.dumps(vars(post), default=str)
            file.write(json_record + '\n')

    print("Data dumped successfully.")


if __name__ == '__main__':
    asyncio.run(main("worldnews"))
