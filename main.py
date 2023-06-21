from fake_useragent import UserAgent
import requests
import json




ua=UserAgent()




def collect_data(min_price=0,max_price=1000000,discount=20):

    offset=0
    size=60
    result = []
    count=1

    while True:
        try:
            for item in range(offset,offset+size,60):
                url=f'https://cs.money/1.0/market/sell-orders?limit=60&maxPrice={max_price}&minPrice={min_price}&offset={item}'
                response= requests.get(
                    url=url,
                    headers={'user-agent': f'{ua.random}'}
            )
                offset+=size


                data=response.json()
                items=data.get('items')







                for i in items:
                    pricing=i.get('pricing')
                    if pricing.get('discount')>discount/100:
                        item_full_name=i.get("asset").get('names').get('full')
                        item_3d=i.get('links').get('3d')
                        item_price=round(i.get('pricing').get('computed'),1)
                        item_discount=round(i.get('pricing').get('discount'),2)*100
                    #print(item_full_name)
                    #print(item_price)
                    #print(item_discount)
                        result.append({
                               'full_name': item_full_name,
                               '3d':item_3d,
                               'price':item_price,
                               'discount': item_discount
                                   }
                                  )


            print(f'Page {count} complete')
            count += 1

            if len(items)<60:
                break
        except:
            if items is None:
                break
    with open('result.json', 'w') as file:
        json.dump(result, file, indent=4, )
    print(len(result))










