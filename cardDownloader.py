# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

import requests
import time
ygo_image_url = "https://images.ygoprodeck.com/images/cards/"
ygo_api_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
cloud_url = "https://res.cloudinary.com/ds6bap5si/image/upload/card-images/"

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")

def Upload(card_id, image_url):
    public_id = card_id
    # card_jpg = str(card_id) + '.jpg'
    # if not card_exists(card_jpg):   
    response = cloudinary.uploader.upload(image_url, 
    public_id = public_id,
    overwrite=True,
    folder='card-images'
    )
    print("Uploaded:", response['secure_url'])
    # else: 
        # print('Skipping', card_id, '- Already exists')

# def card_exists(card_id):
#     response = cloudinary.api.resource(card_id)
#     return 'error' not in response

def Upload_all_card():
    response = requests.get(ygo_api_url)
    data = response.json()
    cards = data['data']
    for card in cards:
        card_id = card['id']
        image_url = card['card_images'][0]['image_url']
        Upload(card_id, image_url)
        time.sleep(1)


def main():
    Upload_all_card()
main()
