"""
Pokemon TCG API Integration - Real pricing data
API Documentation: https://docs.pokemontcg.io/
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

# Pokemon TCG API base URL
API_BASE = "https://api.pokemontcg.io/v2"

# API Key (optional but recommended for higher rate limits)
# Free tier: 1000 requests/hour
# With key: 20000 requests/hour
API_KEY = None  # Will be set from environment variable

def set_api_key(key):
    """Set the Pokemon TCG API key"""
    global API_KEY
    API_KEY = key

def make_request(url):
    """Make HTTP request using urllib"""
    headers = {'Content-Type': 'application/json'}
    if API_KEY:
        headers['X-Api-Key'] = API_KEY

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"URL Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def fetch_set_cards(set_id='sv3pt5', page=1, page_size=250):
    """
    Fetch all cards from a specific set with real pricing
    set_id: sv3pt5 for Pokemon 151
    """
    try:
        params = urllib.parse.urlencode({
            'q': f'set.id:{set_id}',
            'page': page,
            'pageSize': page_size,
            'orderBy': 'number'
        })

        url = f"{API_BASE}/cards?{params}"
        data = make_request(url)

        if not data:
            return {'cards': [], 'total': 0, 'error': 'API request failed'}
        cards = data.get('data', [])

        # Extract relevant card info with real pricing
        processed_cards = []
        for card in cards:
            # Only include English cards
            if card.get('set', {}).get('id') != set_id:
                continue

            # Get TCGPlayer pricing
            tcg_prices = card.get('tcgplayer', {}).get('prices', {})

            # Determine price based on rarity/type
            price = 0.0
            price_type = None

            # Priority order: holofoil > normal > reverseHolofoil > unlimitedHolofoil
            if 'holofoil' in tcg_prices and tcg_prices['holofoil']:
                price = tcg_prices['holofoil'].get('market', 0.0) or tcg_prices['holofoil'].get('mid', 0.0)
                price_type = 'holofoil'
            elif 'normal' in tcg_prices and tcg_prices['normal']:
                price = tcg_prices['normal'].get('market', 0.0) or tcg_prices['normal'].get('mid', 0.0)
                price_type = 'normal'
            elif 'reverseHolofoil' in tcg_prices and tcg_prices['reverseHolofoil']:
                price = tcg_prices['reverseHolofoil'].get('market', 0.0) or tcg_prices['reverseHolofoil'].get('mid', 0.0)
                price_type = 'reverse'
            elif 'unlimitedHolofoil' in tcg_prices and tcg_prices['unlimitedHolofoil']:
                price = tcg_prices['unlimitedHolofoil'].get('market', 0.0) or tcg_prices['unlimitedHolofoil'].get('mid', 0.0)
                price_type = 'unlimited'

            # Skip cards without pricing
            if not price or price <= 0:
                continue

            processed_card = {
                'id': card.get('id'),
                'name': card.get('name'),
                'set': card.get('set', {}).get('name', '151'),
                'set_id': set_id,
                'number': card.get('number'),
                'rarity': card.get('rarity', 'Common'),
                'price': round(float(price), 2),
                'price_type': price_type,
                'type': card.get('types', ['Colorless'])[0] if card.get('types') else 'Colorless',
                'supertype': card.get('supertype', 'Pokémon'),
                'language': 'EN',
                'image': card.get('images', {}).get('large') or card.get('images', {}).get('small', ''),
                'tcgplayer_url': card.get('tcgplayer', {}).get('url', ''),
                'price_source': 'Pokemon TCG API (TCGPlayer)',
                'last_updated': datetime.now().isoformat()
            }

            processed_cards.append(processed_card)

        return {
            'cards': processed_cards,
            'total': data.get('totalCount', len(processed_cards)),
            'page': data.get('page', page),
            'page_size': data.get('pageSize', page_size)
        }

    except Exception as e:
        print(f"Error fetching cards from Pokemon TCG API: {str(e)}")
        return {
            'cards': [],
            'total': 0,
            'error': str(e)
        }

def fetch_all_set_cards(set_id='sv3pt5'):
    """Fetch ALL cards from a set (handles pagination)"""
    all_cards = []
    page = 1

    while True:
        result = fetch_set_cards(set_id, page=page, page_size=250)

        if 'error' in result:
            break

        cards = result.get('cards', [])
        if not cards:
            break

        all_cards.extend(cards)

        # Check if we have all cards
        if len(all_cards) >= result.get('total', 0):
            break

        page += 1

        # Safety limit
        if page > 10:
            break

    return all_cards

def get_card_by_id(card_id):
    """Get a specific card by ID"""
    try:
        url = f"{API_BASE}/cards/{card_id}"
        data = make_request(url)
        return data.get('data') if data else None

    except Exception as e:
        print(f"Error fetching card {card_id}: {str(e)}")
        return None

def search_cards(query, page=1, page_size=20):
    """Search for cards by name or other criteria"""
    try:
        params = urllib.parse.urlencode({
            'q': f'name:{query}*',
            'page': page,
            'pageSize': page_size
        })

        url = f"{API_BASE}/cards?{params}"
        data = make_request(url)
        return data.get('data', []) if data else []

    except Exception as e:
        print(f"Error searching cards: {str(e)}")
        return []

# For testing
if __name__ == "__main__":
    print("Fetching Pokemon 151 cards...")
    result = fetch_set_cards('sv3pt5')
    print(f"Found {len(result['cards'])} cards with pricing")

    if result['cards']:
        # Show a sample card
        card = result['cards'][0]
        print(f"\nSample: {card['name']} - ${card['price']} ({card['rarity']})")
