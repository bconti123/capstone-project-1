import requests

BASE_API_KEY = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
IMAGE_API_KEY = 'https://res.cloudinary.com/ds6bap5si/card-images'

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
    act_obj = {}
    res_obj = {}

    for desc in desc_list:

        if ":" in desc:
            cond = desc.index(":")
            substring = desc[0:cond+1]
            cond_obj = {'condition' : substring}
            desc = desc.replace(substring, '')
        else:
            cond_obj = {}

        if ";" in desc:
            act = desc.index(";")
            substring = desc[0:act+1]
        
            act_obj = {'act' : substring}
            desc = desc.replace(substring, '')
        else:
            act_obj = {}
        
        if "." not in desc:
            res_obj = {'res': desc + "."}
        else:
            res_obj = {'res' : desc}

        # ISSUES: dot '●', Fix it later.
        result_list.append({**cond_obj, **act_obj, **res_obj})

    return result_list


def page():
    cards = search_card('Dark Magician')
    per_page = 5
    offset = (page - 1) ^ per_page

    pag_cards = cards[offset:offset + per_page]

    return pag_cards