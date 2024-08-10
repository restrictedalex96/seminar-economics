import praw
import datetime as dt
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

CLIENT_SECRET = "qthSZUWu3DMt2rmgMIaJVkyPtsZWZA"
CLIENT_ID = "q7R0Pw5L74hSgFxbfFxM2A"

class Post:
    def __init__(self, title, date, likes_count):
        self.title = title
        self.date = date
        self.likes_count = likes_count

class CountryPosts:
    def __init__(self, name):
        self.name = name
        self.posts = []
        self.counter = 0

    def add_post(self, post):
        self.posts.append(post)
        self.counter += 1

def get_date(submission):
    return dt.datetime.fromtimestamp(submission.created)

def process_submission(submission, country_posts):
    submission_date = get_date(submission)
    if submission_date > dt.datetime.now() - dt.timedelta(days=180):
        post = Post(submission.title.lower(), submission_date, submission.ups)
        post_title = submission.title.lower()

        for country, posts_obj in country_posts.items():
            if country in post_title:
                
                posts_obj.add_post(post)
                print("Added post to", country)

async def main(subreddit_name: str):
    print("Starting")

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="Python",
        check_for_async=False
    )

    subreddit = reddit.subreddit(subreddit_name)
    countries = ["russia", "ukraine", "israel", "lebanon", "syria", "palestine", "china", "taiwan", "myanmar", "sudan"]
    country_posts = {country: CountryPosts(country) for country in countries}

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        futures = [
            loop.run_in_executor(executor, process_submission, submission, country_posts)
            for submission in subreddit.new(limit=20000)  # limiting to prevent large data_old load
        ]
        await asyncio.gather(*futures)

    # Dump the data_old to a file
    data_to_dump = {country: [vars(post) for post in posts_obj.posts] for country, posts_obj in country_posts.items()}
    with open(f'{subreddit_name}.json', 'w') as f:
        json.dump(data_to_dump, f, default=str)

    print("Data dumped successfully.")

if __name__ == '__main__':
    asyncio.run(main("worldnews"))
