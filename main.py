import argparse
import json
import os
import time

import requests
import tqdm
from pexels_api import API

PEXELS_API_KEY = os.environ['PEXELS_KEY']
MAX_IMAGES_PER_QUERY = 100
RESULTS_PER_PAGE = 10
PAGE_LIMIT = MAX_IMAGES_PER_QUERY / RESULTS_PER_PAGE


def get_sleep(t):
    def sleep():
        time.sleep(t)
    return sleep


def main(args):
    sleep = get_sleep(args.sleep)

    api = API(PEXELS_API_KEY)
    query = args.query

    page = 1
    counter = 0

    photos_dict = {}

    # Step 1: Getting urls and meta information
    while True or page < PAGE_LIMIT:
        api.search(query, page=page, results_per_page=10)
        photos = api.get_entries()

        for photo in tqdm.tqdm(photos):
            photos_dict[photo.id] = vars(photo)['_Photo__photo']
            counter += 1

        if not api.has_next_page:
            print(f"Finishing at page: {page}")
            print(f"Images were processed: {counter}")
            break

        page += 1
        sleep()

    # Step 2: Downloading
    if photos_dict:
        os.makedirs(args.path, exist_ok=True)

        # Saving dict
        with open(os.path.join(args.path, f'{query}.json'), 'w') as fout:
            json.dump(photos_dict, fout)

        for val in tqdm.tqdm(photos_dict.values()):
            url = val['src'][args.resolution]
            fname = os.path.basename(val['src']['original'])
            image_path = os.path.join(args.path, fname)

            if not os.path.isfile(image_path):  # ignore if already downloaded
                response = requests.get(url, stream=True)

                with open(image_path, 'wb') as outfile:
                    outfile.write(response.content)
            else:
                print(f"File exists: {image_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, required=True)
    parser.add_argument('--path', type=str, default='./results_pexels')
    parser.add_argument('--resolution', choices=['original', 'large2x', 'large',
                                                 'medium', 'small', 'portrait',
                                                 'landscape', 'tiny'], default='original')
    parser.add_argument('--sleep', type=float, default=0.1)
    args = parser.parse_args()
    main(args)
