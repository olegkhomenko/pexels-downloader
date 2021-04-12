"""Scrap Pexels using selenium (without any API calls)"""

import argparse
import time

from selenium.webdriver import Chrome


def scrap_pexels(
    chromedriver_path="/usr/local/bin/chromedriver",
    links_file="links.txt",
    query="portrait",
    max_posts=100,
    scroll_coef=0.4,
):
    """Scrap Pexels website with a specific query. The function saves result links to links_file"""
    browser = Chrome(executable_path=chromedriver_path)
    browser.get(f"https://www.pexels.com/search/{query}/")
    body_scroll_height = (
        browser.execute_script("return document.body.scrollHeight") * scroll_coef
    )
    scroll_height_from = 0
    scroll_height_to = body_scroll_height

    browser.execute_script(
        f"window.scrollTo({scroll_height_from}, {scroll_height_to});"
    )
    scroll_height_from = scroll_height_to
    scroll_height_to += body_scroll_height

    links = set()
    while len(links) < max_posts:
        new_links = set(
            [
                el.find_element_by_tag_name("img").get_attribute("src")
                for el in browser.find_elements_by_class_name("photo-item__link")
            ]
        )
        links = {*links, *new_links}
        print("Len links: ", len(links))

        browser.execute_script(
            f"window.scrollTo({scroll_height_from}, {scroll_height_to});"
        )
        scroll_height_from = scroll_height_to
        scroll_height_to += body_scroll_height

        time.sleep(0.2)

    print("Saving links: ", links_file)
    with open(links_file, "w") as fout:
        for link in links:
            fout.write(link + "\n")
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--links_file", default="links.txt", help="File used to store links to posts"
    )
    parser.add_argument(
        "-q", "--query", default="corgi", type=str, help="Query (Hashtag)"
    )
    parser.add_argument(
        "--max_posts",
        default=1000,
        type=int,
        help="Maximum number of posts to be scraped",
    )
    args = parser.parse_args()
    scrap_pexels(**vars(args))
