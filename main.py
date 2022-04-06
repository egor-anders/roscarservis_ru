import requests
from datetime import datetime
import json
import time

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36',
    'X-Is-Ajax-Request': 'X-Is-Ajax-Request',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_data(url):
    res = requests.get(url=url, headers=headers).json()
    return res

def get_pages_count(url):
    res = requests.get(url=url, headers=headers).json()
    return int(res['pageCount'])


def main():
    start_time = datetime.now()
    pages_count = get_pages_count('https://roscarservis.ru/catalog/legkovye/?isAjax=true&PAGEN_1=1')
    json_data = []
    for i in range(1, pages_count + 1):
        data = get_data(f'https://roscarservis.ru/catalog/legkovye/?isAjax=true&PAGEN_1={i}')
        items = data['items']        
        try:
            for item in items:
                name = item['name']
                price = item['price']
                img = 'https://roscarservis.ru' + item['imgSrc']
                url = 'https://roscarservis.ru' + item['url']
                total_amount = 0
                stores_data = []
                stores = item['commonStores']
                if stores is None:
                    continue
                else:
                    for store in stores:
                        store_info = {
                            'store_name': store['STORE_NAME'],
                            'store_price': store['PRICE'],
                            'store_amount': int(store['AMOUNT'])
                        }
                        total_amount += int(store['AMOUNT'])
                        stores_data.append(store_info)

                product_data = {
                    'name': name,
                    'price': price,
                    'img': img,
                    'url': url,
                    'amount': total_amount,
                    'stores_data': stores_data
                }
                
                json_data.append(product_data)
        except:
            print('error')
        print(f'[PROGRESS] {i}/{pages_count} completed')
        time.sleep(1)
    
    current_date = datetime.now().strftime('%d_%m_%Y_%H_%M')
    with open(f'{current_date}.json', 'a', encoding='utf8') as t:
        json.dump(json_data, t, indent=4, ensure_ascii=False)


    print(f'Время выполнения: {datetime.now()-start_time}')

if __name__ == '__main__':
    main()