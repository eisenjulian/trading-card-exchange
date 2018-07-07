import os
import unidecode
import requests
import sys
import json
from datetime import datetime

def clean(string):
    if not string:
        return ''
    return unidecode.unidecode(string).translate(None, '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~').lower().strip()

with open(os.path.join('data', 'cards.json')) as f:
    print 'Loading cards'
    cards = {
        player.split()[0] : {
            'id': player.split()[0],
            'clean': clean(' '.join(player.split()[1:])),
            'team': team,
            'name': ' '.join(player.split()[1:])
        }
        for team, players in json.load(f).iteritems()
        for player in players}

def log(msg):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()

def get_stickers_from_text(lines):
    clean_lines = [clean(line) for line in lines]
    best_match = []
    score = 0
    for id, player in cards.iteritems():
        for line in clean_lines:
            clean_player = player['clean']
            if len(line) > 4 and line in clean_player and len(line) > score:
                log('Found match ' + line + ' in  '+ player)
                score = len(line)
                best_match = [id]
                # best_match = team + ' ' + player
    return best_match


def get_stickers_from_image(url):
    image_data = requests.get(url)
    if image_data.status_code / 100 != 2:
        log('Problems getting image at URL ' + url + ' response: ' + image_data.text)
        return 'Nothing found'
    data = json.dumps({
        "requests": [{
            "image": {"content": image_data.content.encode('base64')},
            "features": [{"type": "TEXT_DETECTION"}]
        }]
    })
    response = requests.post('https://vision.googleapis.com/v1/images:annotate?fields=responses%2FfullTextAnnotation%2Ftext&key=' + os.environ['VISION_API_KEY'], data=data)
    log(response.text)
    if response.status_code / 100 != 2:
        log('Error calling Cloud Vision API: ' + response.text + ' for URL: ' + url)
        return 'Nothing found'
    lines = ('\n'.join(
        line['fullTextAnnotation']['text'] for line in response.json()['responses'] if 'fullTextAnnotation' in line
    )).split('\n')
    print lines
    return get_stickers_from_text(lines)
