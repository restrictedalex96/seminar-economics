import praw
import datetime as dt
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

CLIENT_SECRET = "qthSZUWu3DMt2rmgMIaJVkyPtsZWZA"
CLIENT_ID = "q7R0Pw5L74hSgFxbfFxM2A"

class Post:
    def __init__(self, title, date, likes_count, confidence):
        self.title = title
        self.date = date
        self.likes_count = likes_count
        self.confidence = confidence

def get_date(submission):
    return dt.datetime.fromtimestamp(submission.created)

def calculate_confidence(post_title):
    high_confidence_keywords = ["jihad", "hamas", "idf"]
    moderate_confidence_keywords = ["war", "casualti", "bomb", "killed", "murder", "famine", "starvation", "boycott", "resistance", "aid", "terror", "attack", "october 7th", "invaded"]
    if any(keyword in post_title for keyword in high_confidence_keywords):
        return 1.0
    elif "israel" in post_title and "palestine" in post_title:
        return 1.0
    elif ("israel" in post_title or "palestine" in post_title) and any(keyword in post_title for keyword in moderate_confidence_keywords):
        return 0.9
    elif "israel" in post_title or "palestine" in post_title:
        return 0.5
    return 0

def process_submission(submission):
    print("here!")
    submission_date = get_date(submission)
    if submission_date >= dt.datetime(2023, 10, 5):
        post_title = submission.title.lower()
        confidence = calculate_confidence(post_title)

        if confidence > 0:
            return Post(submission.title, submission_date, submission.likes, confidence)

async def main(subreddit_name: str):
    print("Starting")

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="Python",
        check_for_async=False
    )

    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        futures = [
            loop.run_in_executor(executor, process_submission, submission)
            for submission in subreddit.new(limit=None)
        ]
        results = await asyncio.gather(*futures)
        # Filter out None values returned from process_submission
        posts = [result for result in results if result]

    # Dump the data_old to a file
    with open(f'{subreddit_name}_israel_palestine.jsonl', 'w') as file:
        for post in posts:
            json_record = json.dumps(vars(post), default=str)
            file.write(json_record + '\n')

    print("Data dumped successfully.")

if __name__ == '__main__':
    asyncio.run(main("worldnews"))
