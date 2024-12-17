import dataclasses
import json
import os

import requests
from bs4 import BeautifulSoup

from tarot_cmoney.card import CardRaw

OUTPUT_DIRECTORY = '/cards'
LOG_OUTPUT = True

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def scrape_card_data():
    url_base = 'https://labyrinthos.co'
    url = url_base + '/blogs/tarot-card-meanings-list'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find('div', attrs={'class': 'tarot-list'})
    suitDivs = results.find_all('div', attrs={'class': 'grid cards'})

    suits = [
        'MajorArcana',
        'Wands',
        'Cups',
        'Swords',
        'Pentacles'
    ]

    suit_idx = 0
    for suitDiv in suitDivs:
        cards = suitDiv.find_all('div', attrs={'class': 'grid__item'})
        for card in cards:
            name = card.find('h3').text.replace('Meaning', '').strip()
            meaning_link = url_base + card.find('a').get('href')
            text_lines = card.find('p').text

            # First level summary meanings
            upright_meanings_1 = list()
            reverse_meanings_1 = list()

            for line in text_lines.split('\n'):
                if 'Upright' in line or 'Reverse' in line:
                    words_to_append = line.strip().split(':')[1].strip().split(', ')

                    if 'Upright' in line:
                        upright_meanings_1.extend(words_to_append)
                    elif 'Reversed' in line:
                        reverse_meanings_1.extend(words_to_append)

            # Details page
            detail_page = requests.get(meaning_link)
            detail_soup = BeautifulSoup(detail_page.content, 'html.parser')
            tables = detail_soup.find_all('table')

            upright_meanings_2 = list()
            reverse_meanings_2 = list()
            upright_love_meaning = list()
            upright_career_meaning = list()
            upright_finances_meaning = list()
            reverse_love_meaning = list()
            reverse_career_meaning = list()
            reverse_finances_meaning = list()

            for i in range(3):
                # Six of Cups has four tables where the 2nd table in the odd one out. Shifting is required for this card.
                adj = (name == 'Six of Cups' and i > 0) + 0
                check = i + adj

                dat = tables[check].find_all('tr')[1].find_all('td')

                # Second level summary meanings
                if i == 0:
                    upright_meanings_2 = dat[0].text.split(', ')
                    reverse_meanings_2 = dat[1].text.split(', ')

                # Upright love/career/finances meanings
                elif i == 1:
                    upright_love_meaning = dat[0].text.split(', ')
                    upright_career_meaning = dat[1].text.split(', ')
                    upright_finances_meaning = dat[2].text.split(', ')

                # Reverse love/career/finances meanings
                elif i == 2:
                    reverse_love_meaning = dat[0].text.split(', ')
                    reverse_career_meaning = dat[1].text.split(', ')
                    reverse_finances_meaning = dat[2].text.split(', ')

            # Output to json
            card = CardRaw(
                suit=suits[suit_idx],
                name=name,
                upright_meanings_1=upright_meanings_1,
                upright_meanings_2=upright_meanings_2,
                upright_love_meaning=upright_love_meaning,
                upright_career_meaning=upright_career_meaning,
                upright_finances_meaning=upright_finances_meaning,
                reverse_meanings_1=reverse_meanings_1,
                reverse_meanings_2=reverse_meanings_2,
                reverse_love_meaning=reverse_love_meaning,
                reverse_career_meaning=reverse_career_meaning,
                reverse_finances_meaning=reverse_finances_meaning,
            )

            if suits[suit_idx] == 'MajorArcana':
                filename = name.title().replace(' ', '') + '.json'
            else:
                help_dict = {
                    'ace': 'Ace',
                    'two': '2',
                    'three': '3',
                    'four': '4',
                    'five': '5',
                    'six': '6',
                    'seven': '7',
                    'eight': '8',
                    'nine': '9',
                    'ten': '10',
                    'page': 'Page',
                    'knight': 'Knight',
                    'queen': 'Queen',
                    'king': 'King',
                }
                filename = suits[suit_idx] + help_dict[name.lower().split(' ')[0]] + '.json'

            output_path = os.path.join(OUTPUT_DIRECTORY, filename)

            with open(output_path, 'w') as f:
                if LOG_OUTPUT:
                    print('Writing to file: ', output_path)
                f.write(json.dumps(card, cls=EnhancedJSONEncoder, indent=2))

        suit_idx += 1
