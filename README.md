# pexels-downloader
Script to download free-to-use images from pexels.com


Requirements
---
```bash
pip install pypexels requests tqdm 
```

How to use
---
```bash
PEXELS_KEY=%API_KEY% python3 main.py --query dogs --resolution large
```
To get `%APIKEY%` go to [https://www.pexels.com/api/new/](https://www.pexels.com/api/key/)


Original Post:
---
[Collecting free-to-use photos from Pexels using Python and Pexels API](https://medium.com/@olegkhomenko/collecting-free-to-use-photos-from-pexels-using-python-and-pexels-api-81845aee67ef)
