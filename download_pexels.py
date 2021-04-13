import argparse
from pathlib import Path

import requests


def download_pexels(root_dir="./", n_workers=1, compress=False):
    if n_workers > 1:
        raise NotImplementedError

    links = []
    with open("links.txt") as fin:
        line = fin.readline().replace("\n", "")
        while line:
            links += [line]
            line = fin.readline().replace("\n", "")

    links = [l_.split("?")[0] for l_ in links]
    fnames = [l_.split("/")[-1] for l_ in links]

    Path(root_dir).mkdir(exist_ok=True)

    params = ["auto=compress"] if compress else []
    downloaded = 0
    for link, fname in zip(links, fnames):
        fpath = Path(root_dir, fname)
        if fpath.exists():
            print("Exists: ", fpath)
            continue

        response = requests.get(link + ("?" + "&".join(params)))
        with open(str(fpath), "wb") as file:
            file.write(response.content)

        if fpath.exists():
            print("Downloaded: ", fpath)
            downloaded += 1

    print("Finished. Files downloaded: ", downloaded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compress", default=True, type=bool)
    parser.add_argument("--root_dir", default="./pexels_images/")
    args = parser.parse_args()
    download_pexels(**vars(args))
