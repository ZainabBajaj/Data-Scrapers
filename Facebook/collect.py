import csv
import json
import re
import time
from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, TypedDict, Optional, Tuple

from facebook_scraper import get_posts
from facebook_scraper.exceptions import TemporarilyBanned

dataset_path: Path = Path('./data/facebook/{}_private_group_posts.csv'.format(datetime.now()))


class FacebookGroupPost(TypedDict):
    group_id: str  # a facebook group where post was found
    # fetched_at: datetime  # time when post was scrapped

    post_id: str
    post_url: str
    created_at: datetime
    post_text: str

    author_id: str
    author_username: str

    external_link: str  # if post contains external links, the link will be here

    images: str  # JSON string of image information

    video_id: str
    video: str
    video_duration_seconds: int
    video_thumbnail: str
    video_watches: int

    likes_count: int
    comments_count: int
    shares_count: int
    reaction_count: int
    reactions: str  # JSON string of serialized reactions with user information


def serialize_images(image_ids: List[str], image_urls: List[str], image_descriptions: List[str]) -> str:
    """
    Serialize all image information as JSON string
    """
    if not image_ids or len(image_ids) == 0:
        return ''

    images = []

    for image_id, image_url, image_description in zip(image_ids, image_urls, image_descriptions):
        images.append({
            'id': image_id,
            'url': image_url,
            'desc': image_description,
        })

    return json.dumps(images)


def get_username_from_url(user_url: str) -> str:
    """
    Parse username in a given user link.
    Links can be longs with a lots of marketing params in URL. We make our dataset smaller by removing all junk parts
    """
    user_id_regex: str = r'profile\.php\?id=(?P<user_id>\d+)&'
    username_regex: str = r'facebook\.com\/(?P<username>.*)\?'

    user_id_matches: re.Match = re.search(user_id_regex, user_url)

    if user_id_matches:
        return user_id_matches.group('user_id')

    username_matches: re.Match = re.search(username_regex, user_url)

    if username_matches:
        return username_matches.group('username').strip('/')

    raise RuntimeError('Facebook User URL was given in an unknown format: {}'.format(user_url))


def serialize_reactors(reactors: List[Dict]) -> str:
    """
    Group reactors by their reactions and then serialize them as JSON string
    """
    if not reactors or len(reactors) == 0:
        return ''

    reactions_map = defaultdict(list)

    for reactor in reactors:
        reaction = reactor['type']
        reactor_name = reactor['name']
        reactor_url = reactor['link']

        reactions_map[reaction].append({
            'name': reactor_name,
            'username': get_username_from_url(reactor_url)  # can be accesses by 'https://facebook.com/{username}'
        })

    return json.dumps(reactions_map)


"""
Facebook may temporarily ban client IP after certain amount of requests.
Storing search_page_url helps to proceed from where we left after ban is gone. 
"""


class SearchPagePersistor:
    search_page_url: Optional[str] = None

    def __init__(self, page_url: Optional[str] = None):
        self.search_page_url = page_url

    def get_current_search_page(self) -> Optional[str]:
        return self.search_page_url

    def set_search_page(self, page_url: str) -> None:
        print('Storing next search page {}..'.format(page_url))
        self.search_page_url = page_url


def get_arg_parser() -> ArgumentParser:
    """
    Create console API for the script
    :return: ArgumentParser
    """
    arg_parser: ArgumentParser = ArgumentParser(description='Collect information from private Facebook groups')

    arg_parser.add_argument(
        '--group_id',
        type=str,
        required=True,
        help='private group ID to scrap posts from. Could be found in group URL',
    )

    arg_parser.add_argument(
        '--cookie',
        type=str,
        required=True,
        help='serialized cookies of account that has access to the private group. More information: '
             'https://github.com/kevinzg/facebook-scraper#optional-parameters',
    )

    arg_parser.add_argument(
        '--save_every_n_posts',
        type=int,
        help='how many posts to store in RAM before writing to the dataset',
        default=10,
    )

    arg_parser.add_argument(
        '--ban_timeout',
        type=int,
        help='how many time (in seconds) should we wait on IP ban (600secs by default, e.g. 10mins)',
        default=600,
    )

    arg_parser.add_argument(
        '--ignore_post_ids',
        nargs='+',
        help='ignore posts by ID. For example, it may be helpful to ignore old announcement posts which '
             'may be outside of the time period of interest',
        default=(),
    )

    return arg_parser


"""
- full docs on FB scrapping tool: https://github.com/kevinzg/facebook-scraper
"""

if __name__ == "__main__":
    args = get_arg_parser().parse_args()

    group_id: str = args.group_id
    ignore_post_ids: Tuple[str] = args.ignore_post_ids
    cookie_path: str = args.cookie
    num_posts_to_store_in_ram: int = args.save_every_n_posts
    search_page_persistor: SearchPagePersistor = SearchPagePersistor()

    period_end_date: datetime = datetime(2019, 1, 1)  # from 2019 until now - COVID period

    dataset_path.parent.mkdir(parents=True, exist_ok=True)

    print("Open dataset file ({})..".format(dataset_path))

    with open(dataset_path, mode='w') as dataset_file:
        dataset_writer = csv.DictWriter(dataset_file, fieldnames=FacebookGroupPost.__annotations__.keys())
        dataset_writer.writeheader()

        posts: List[FacebookGroupPost] = []

        while True:
            try:
                print('Next Search Page: {}'.format(search_page_persistor.get_current_search_page()))

                for post_idx, post in enumerate(get_posts(
                        group=group_id,
                        cookies=cookie_path,
                        page_limit=None,  # try to get all pages and then decide where to stop
                        start_url=search_page_persistor.get_current_search_page(),
                        request_url_callback=search_page_persistor.set_search_page,
                        options={
                            'reactors': True,
                            'posts_per_page': 200,
                        }
                )):
                    print(
                        "[{}] ({}) Collecting information about post {}..".format(
                            post['post_id'],
                            post['time'],
                            post['post_url']
                        )
                    )

                    if post['post_id'] in ignore_post_ids:
                        print('Ignore post {} created at {}'.format(post['post_id'], post['time']))
                        continue

                    if group_id not in post['post_url']:
                        print('Ignore post {} (promo)'.format(post['post_id']))
                        continue

                    if period_end_date > post['time']:
                        break

                    if 'image_ids' not in post:
                        post['image_ids'] = None

                    posts.append({
                        'group_id': group_id,

                        'post_id': post['post_id'],
                        'created_at': post['time'],
                        'post_url': post['post_url'],
                        'post_text': post['post_text'],

                        'author_id': post['user_id'],
                        'author_username': post['username'],

                        'external_link': post['link'],

                        'likes_count': post['link'],
                        'comments_count': post['comments'],
                        'shares_count': post['shares'],
                        'reaction_count': post['reaction_count'],
                        'reactions': serialize_reactors(post['reactors']),

                        'images': serialize_images(
                            post['image_ids'],
                            post['images'],
                            post['images_description']
                        ),

                        'video': post['video'],
                        'video_id': post['video_id'],
                        'video_duration_seconds': post['video_duration_seconds'],
                        'video_watches': post['video_watches'],
                        'video_thumbnail': post['video_thumbnail'],
                    })

                    if post_idx % num_posts_to_store_in_ram == 0:
                        # time to flush post data stored in RAM
                        print("Flushing {} posts to the dataset file..".format(num_posts_to_store_in_ram))

                        dataset_writer.writerows(posts)
                        posts = []

                break
            except TemporarilyBanned:
                print("Facebook temporarily banned IP, sleeping for 10m..")
                time.sleep(600)

        if len(posts) > 0:
            print("Flushing {} posts to the dataset file..".format(len(posts)))

            dataset_writer.writerows(posts)

        print("Scrapping posts from group {} has been complete".format(group_id))
        print("Check out results in {}".format(dataset_path))
