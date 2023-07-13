import requests

BASE_API_KEY = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'

def search_card(card):
    try: 
        response = requests.get(f'{BASE_API_KEY}?fname={card}')
        response.raise_for_status()
        obj = response.json()
        if 'data' in obj:
            return obj['data']
        else:
            return []
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f'Error: {e}')
        return []


def find_card_id(id):
    try: 
        response = requests.get(f'{BASE_API_KEY}?id={id}')
        response.raise_for_status()
        obj = response.json()
        if 'data' in obj:
            return obj['data']
        else:
            return []
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f'Error: {e}')
        return []

def find_card_desc(card):
    desc_list = card[0]['desc'].split('. ')
    result_list = []
    cond_obj = {}
    cost_obj = {}
    act_obj = {}
    # if ('toss a coin:' in desc_list):
    #     desc_list = [' '.join(desc_list)]
    for desc in desc_list:

        if ":" in desc:
            cond = desc.index(":")
            substring = desc[0:cond+1]
            cond_obj = {'condition' : substring}
            desc = desc.replace(substring, '')
        else:
            cond_obj = {}

        if ";" in desc:
            cost = desc.index(";")
            substring = desc[0:cost+1]
        
            cost_obj = {'cost' : substring}
            desc = desc.replace(substring, '')
        else:
            cost_obj = {}

        
        
        act_obj = {'act': desc}

        # ISSUES: dot '●', Fix it later.
        result_list.append({**cond_obj, **cost_obj, **act_obj})

    return result_list
