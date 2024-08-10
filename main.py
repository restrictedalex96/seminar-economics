# import json
# import pathlib
# import dataclasses
#
#
# @dataclasses.dataclass
# class Record:
#     post_title: str
#     post_body: str
#     date: str
#     comments: list[str]
#
#
#
# records_parent_path = pathlib.Path(r'/scrap_reddit')
# devops_records_file_name = 'devops.json'
#
#
# def read_data(file_name: str):
#     with open(records_parent_path / file_name, 'r') as file:
#         data_old = json.loads(file.read())
#
#     return [Record(**record) for record in data_old]
#
#
# devops_records = read_data(devops_records_file_name)


import praw
import datetime as dt
import json
import time
from collections import defaultdict
from collections import Counter


CLIENT_SECRET = "qthSZUWu3DMt2rmgMIaJVkyPtsZWZA"
CLIENT_ID = "q7R0Pw5L74hSgFxbfFxM2A"



def get_date(submission):
    time = submission.created
    return dt.datetime.fromtimestamp(time)

class Post:
    def __init__(self, title, date, likes_count):
        self.title = title
        self.date = date
        self.likes_count = likes_count



class Israel:
    posts = list()
    counter = 0


class Lebanon:
    posts = list()
    counter = 0


class Syria:
    posts = list()
    counter = 0


class Palestine:
    posts = list()
    counter = 0


class Russia:
    posts = list()
    counter = 0


class Ukraine:
    posts = list()
    counter = 0


class China:
    posts = list()
    counter = 0


class Taiwan:
    posts = list()
    counter = 0


class Myanmar:
    posts = list()
    counter = 0


class Sudan:
    posts = list()
    counter = 0


# def get_comments(submission):
#     submission.comments.replace_more(limit=0)
#     comments = [comment.body for comment in submission.comments.list()]
#     return comments


def main(subreddit_name: str):
    print("Starting")

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="Python",
        check_for_async=False
    )

    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    russia = Russia()
    ukraine = Ukraine()
    israel = Israel()
    lebanon = Lebanon()
    syria = Syria()
    palestine = Palestine()
    china = China()
    taiwan = Taiwan()
    sudan = Sudan()
    myanmar = Myanmar()



    try:
        number_of_submissions = 0
        for submission in subreddit.new(limit=None):
            print(f"Submission {submission.title}")
            submission_date = get_date(submission)
            time.sleep(2)

            if submission_date > dt.datetime.now() - dt.timedelta(days=180):
                number_of_submissions += 1

                post = Post(submission.title.lower(), submission_date, submission.likes)

                post_title = submission.title.lower()

                if "russia" in post_title:
                    russia.posts.append(post)
                    russia.counter += 1

                if "ukraine" in post_title:
                    ukraine.posts.append(post)
                    ukraine.counter += 1

                # fill in the rest of the countries
                if "israel" in post_title:
                    israel.posts.append(post)
                    israel.counter += 1

                if "lebanon" in post_title:
                    lebanon.posts.append(post)
                    lebanon.counter += 1

                if "syria" in post_title:
                    syria.posts.append(post)
                    syria.counter += 1

                if "sudan" in post_title:
                    sudan.posts.append(post)
                    sudan.counter += 1

                if "myanmar" in post_title:
                    myanmar.posts.append(post)
                    myanmar.counter += 1

                if "palestine" in post_title:
                    palestine.posts.append(post)
                    palestine.counter += 1

                if "china" in post_title:
                    china.posts.append(post)
                    china.counter += 1

                if "taiwan" in post_title:
                    taiwan.posts.append(post)
                    taiwan.counter += 1


                print(post)

                if number_of_submissions % 100 == 0:
                    print(f"Done {number_of_submissions} submissions.")

                if number_of_submissions > 20000:
                    break
    except Exception as e:
        print(e)
    finally:
        with open(f'{subreddit_name}.json', 'w') as f:
            json.dump(posts, f)


if __name__ == '__main__':
    for subreddit in ["worldnews"]:
        main(subreddit)
        time.sleep(60)