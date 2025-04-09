import requests
from bs4 import BeautifulSoup
import json
import time
from telegram import Bot
from telegram.error import TelegramError

# Telegram bot credentials
BOT_TOKEN = '7734445379:AAG_X2lDP1eq8f-cu1cfCGELXX-lDyNhsbE'
CHAT_ID = '7819261629'

# List of URLs to monitor
urls = [
    'https://www.vesteda.com/nl/woning-zoeken?placeType=1&sortType=1&radius=20&s=Utrecht,%20Nederland&sc=woning&latitude=52.091927&longitude=5.122957&filters=6873,6883,6889&priceFrom=500&priceTo=9999',
    'https://www.funda.nl/zoeken/huur/?selected_area=[%22utrecht%22]&price=%220-3000%22&bedrooms=%220-2%22&sort=%22date_down%22',
    'https://www.pararius.com/apartments/utrecht/0-2250/2-bedrooms',
    'https://www.beumer.nl/huurwoningen/?filters%5B0%5D=utrecht'
]

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)

# Function to check for new listings
def check_listings():
    # Store seen listings (could be moved to a file or database in the future)
    seen_listings = set()

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse listings (This part depends on the website structure)
        # Example: Adjust this to match each website's HTML structure
        listings = soup.find_all('a', class_='listing-class')  # Example, change as needed

        for listing in listings:
            title = listing.get_text(strip=True)
            link = listing['href']

            # If listing is new, send a notification
            if link not in seen_listings:
                seen_listings.add(link)
                message = f"New listing found: {title}\n{link}"

                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                except TelegramError as e:
                    print(f"Error sending message: {e}")
    print("Checked listings.")

# Run the scraper every 10 minutes
while True:
    check_listings()
    time.sleep(600)  # Wait for 10 minutes