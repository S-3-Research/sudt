import json 
import requests
import os
from tqdm import tqdm
import brotli 

DATA_DIR = "data/addicted_org_050923"
PAGE_SIZE = 50
for page in tqdm(range(506)):
    if os.path.exists(f"{DATA_DIR}/addicted_org_{page}.json"):
        continue
    url = f"https://www.addicted.org/wp-admin/admin-ajax.php?id=direcoryindex&post_id=48815&slug=directory&canonical_url=https%3A%2F%2Fwww.addicted.org%2Fdirectory.html&posts_per_page=50&page=0&offset=0&post_type=wpbdp_listing&repeater=default&seo_start_page=1&filters=true&filters_startpage=0&filters_target=overallfilter&facets=false&paging=true&preloaded=true&preloaded_amount=0&meta_key=priority&order=DESC&orderby=meta_value_num&action=alm_get_posts&query_type=standard"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
    }
    response = requests.get(url, headers=headers)
    content = response.content.decode()
    if content.startswith("400 - Bad Request"):
        print("400 - Bad Request")
        break
    elif content.startswith("<html>"):
        print("Captured by captcha")
        break
    print(type(content))
    # print(json.loads(content))
    json.dump(content, open(f"{DATA_DIR}/addicted_org_{page}.json", "w"))
    break
