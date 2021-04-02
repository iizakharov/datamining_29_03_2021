import json
from pathlib import Path
from time import sleep
import requests


headers = {
    'User-agent': 'Alla Pugacheva',
}

params = {
    'store': None,
    'records_per_page': 12,
    'page': 1,
    'categories': None,
    'ordering': None,
    'price_promo__gte': None,
    'price_promo__lte': None,
    'search': None,
}

# Get all categories
url_category = 'https://5ka.ru/api/v2/categories/'
response_category: requests.Response = requests.get(url_category, headers=headers)
file_category = Path(__file__).parent.joinpath('category.json')
categories = []
req_text = json.loads(response_category.text)
for category in req_text:
    categories.append(category)


# parser
url = 'http://5ka.ru/api/v2/special_offers/'

for cat in categories:
    dock_view = {
        "name": None,
        "code": None,
        "products": list
    }
    params['categories'] = cat["parent_group_code"]
    response: requests.Response = requests.get(url, headers=headers, params=params)
    req_text = json.loads(response.text)
    if len(json.dumps(req_text["results"])) != 2:
        dock_view['name'], dock_view['code'] = cat["parent_group_name"], cat["parent_group_code"]
        dock_view['products'] = req_text["results"]
        file = Path(__file__).parent.joinpath(f'{cat["parent_group_name"]}.json')
        dock_view = json.dumps(dock_view, ensure_ascii=False)
        # print(dock_view)
        file.write_text(dock_view)
        # sleep(0.1)
        
print('END parse!')
