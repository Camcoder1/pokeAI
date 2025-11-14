"""
Pokemon TCG Market Analyst - Lambda Handler (Simplified for testing)
"""

import json
import os
from datetime import datetime

# CORS headers
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
}

def lambda_handler(event, context):
    """Main Lambda handler"""

    try:
        path = event.get('path', '')
        method = event.get('httpMethod', '')

        print(f"Request: {method} {path}")

        # Handle CORS preflight
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': ''
            }

        # Route requests
        if path == '/sets' or path == '/prod/sets':
            return get_sets(CORS_HEADERS)
        elif path == '/trending' or path == '/prod/trending':
            return get_trending(CORS_HEADERS)
        elif path.startswith('/analyze') and method == 'POST':
            return analyze_product(event, CORS_HEADERS)
        else:
            return {
                'statusCode': 404,
                'headers': CORS_HEADERS,
                'body': json.dumps({'error': 'Not found', 'path': path})
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e), 'type': type(e).__name__})
        }


def get_sets(headers):
    """Return sample Pokemon sets"""

    sets = [
        {
            'id': 'sv04',
            'name': '151',
            'series': 'Scarlet & Violet',
            'release_date': '2023-09-22',
            'total': 207,
            'logo': 'https://images.pokemontcg.io/sv04/logo.png'
        },
        {
            'id': 'sv05',
            'name': 'Obsidian Flames',
            'series': 'Scarlet & Violet',
            'release_date': '2023-08-11',
            'total': 230,
            'logo': 'https://images.pokemontcg.io/sv05/logo.png'
        },
        {
            'id': 'sv04pt5',
            'name': 'Paldean Fates',
            'series': 'Scarlet & Violet',
            'release_date': '2024-01-26',
            'total': 245,
            'logo': 'https://images.pokemontcg.io/sv04pt5/logo.png'
        },
        {
            'id': 'sv06',
            'name': 'Twilight Masquerade',
            'series': 'Scarlet & Violet',
            'release_date': '2024-05-24',
            'total': 226,
            'logo': 'https://images.pokemontcg.io/sv06/logo.png'
        },
        {
            'id': 'sv07',
            'name': 'Shrouded Fable',
            'series': 'Scarlet & Violet',
            'release_date': '2024-08-02',
            'total': 99,
            'logo': 'https://images.pokemontcg.io/sv07/logo.png'
        }
    ]

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'sets': sets})
    }


def get_trending(headers):
    """Return sample trending data"""

    trending = [
        {
            'set_name': '151',
            'product_name': '151 Booster Box',
            'ev_open': 145.50,
            'sealed_price': 120.00,
            'roi_percent': 21.3,
            'recommendation': 'OPEN - Expected value significantly exceeds sealed price',
            'timestamp': int(datetime.now().timestamp())
        }
    ]

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'trending': trending})
    }


def analyze_product(event, headers):
    """Analyze a product (simplified version)"""

    try:
        body = json.loads(event.get('body', '{}'))
        set_name = body.get('set_name', '151')
        product_name = body.get('product_name', '151 Booster Box')
        sealed_price = body.get('sealed_price', 120.0)

        # Comprehensive card list for 151 set with images and values
        top_cards = [
            {'name': 'Charizard ex (Special Illustration)', 'rarity': 'Special Illustration Rare', 'price': 285.00, 'pull_rate': 0.028, 'ev_contribution': 7.98, 'set_number': '199', 'image': 'https://images.pokemontcg.io/sv3pt5/199_hires.png'},
            {'name': 'Mew ex (Special Illustration)', 'rarity': 'Special Illustration Rare', 'price': 175.00, 'pull_rate': 0.028, 'ev_contribution': 4.90, 'set_number': '205', 'image': 'https://images.pokemontcg.io/sv3pt5/205_hires.png'},
            {'name': 'Mewtwo ex (Special Illustration)', 'rarity': 'Special Illustration Rare', 'price': 140.00, 'pull_rate': 0.028, 'ev_contribution': 3.92, 'set_number': '206', 'image': 'https://images.pokemontcg.io/sv3pt5/206_hires.png'},
            {'name': 'Zapdos ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 18.50, 'pull_rate': 0.083, 'ev_contribution': 1.54, 'set_number': '182', 'image': 'https://images.pokemontcg.io/sv3pt5/182_hires.png'},
            {'name': 'Moltres ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 15.00, 'pull_rate': 0.083, 'ev_contribution': 1.25, 'set_number': '184', 'image': 'https://images.pokemontcg.io/sv3pt5/184_hires.png'},
            {'name': 'Alakazam ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 12.50, 'pull_rate': 0.083, 'ev_contribution': 1.04, 'set_number': '180', 'image': 'https://images.pokemontcg.io/sv3pt5/180_hires.png'},
            {'name': 'Venusaur ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 11.00, 'pull_rate': 0.083, 'ev_contribution': 0.91, 'set_number': '189', 'image': 'https://images.pokemontcg.io/sv3pt5/189_hires.png'},
            {'name': 'Blastoise ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 10.50, 'pull_rate': 0.083, 'ev_contribution': 0.87, 'set_number': '174', 'image': 'https://images.pokemontcg.io/sv3pt5/174_hires.png'},
            {'name': 'Charizard ex', 'rarity': 'Double Rare', 'price': 45.00, 'pull_rate': 0.166, 'ev_contribution': 7.47, 'set_number': '6', 'image': 'https://images.pokemontcg.io/sv3pt5/6_hires.png'},
            {'name': 'Mew ex', 'rarity': 'Double Rare', 'price': 35.00, 'pull_rate': 0.166, 'ev_contribution': 5.81, 'set_number': '151', 'image': 'https://images.pokemontcg.io/sv3pt5/151_hires.png'},
            {'name': 'Mewtwo ex', 'rarity': 'Double Rare', 'price': 28.00, 'pull_rate': 0.166, 'ev_contribution': 4.65, 'set_number': '150', 'image': 'https://images.pokemontcg.io/sv3pt5/150_hires.png'},
            {'name': 'Zapdos ex', 'rarity': 'Double Rare', 'price': 8.50, 'pull_rate': 0.166, 'ev_contribution': 1.41, 'set_number': '145', 'image': 'https://images.pokemontcg.io/sv3pt5/145_hires.png'},
            {'name': 'Moltres ex', 'rarity': 'Double Rare', 'price': 7.00, 'pull_rate': 0.166, 'ev_contribution': 1.16, 'set_number': '146', 'image': 'https://images.pokemontcg.io/sv3pt5/146_hires.png'},
            {'name': 'Erika\'s Invitation (Full Art)', 'rarity': 'Ultra Rare', 'price': 32.00, 'pull_rate': 0.083, 'ev_contribution': 2.66, 'set_number': '196', 'image': 'https://images.pokemontcg.io/sv3pt5/196_hires.png'},
            {'name': 'Pidgeot ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 9.50, 'pull_rate': 0.083, 'ev_contribution': 0.79, 'set_number': '186', 'image': 'https://images.pokemontcg.io/sv3pt5/186_hires.png'},
            {'name': 'Gengar ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 8.00, 'pull_rate': 0.083, 'ev_contribution': 0.66, 'set_number': '178', 'image': 'https://images.pokemontcg.io/sv3pt5/178_hires.png'},
            {'name': 'Dragonite ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 7.50, 'pull_rate': 0.083, 'ev_contribution': 0.62, 'set_number': '175', 'image': 'https://images.pokemontcg.io/sv3pt5/175_hires.png'},
            {'name': 'Bulbasaur (Illustration Rare)', 'rarity': 'Illustration Rare', 'price': 6.50, 'pull_rate': 0.055, 'ev_contribution': 0.36, 'set_number': '1', 'image': 'https://images.pokemontcg.io/sv3pt5/1_hires.png'},
            {'name': 'Squirtle (Illustration Rare)', 'rarity': 'Illustration Rare', 'price': 5.50, 'pull_rate': 0.055, 'ev_contribution': 0.30, 'set_number': '7', 'image': 'https://images.pokemontcg.io/sv3pt5/7_hires.png'},
            {'name': 'Charmander (Illustration Rare)', 'rarity': 'Illustration Rare', 'price': 5.00, 'pull_rate': 0.055, 'ev_contribution': 0.28, 'set_number': '4', 'image': 'https://images.pokemontcg.io/sv3pt5/4_hires.png'},
            {'name': 'Pikachu (Illustration Rare)', 'rarity': 'Illustration Rare', 'price': 12.00, 'pull_rate': 0.055, 'ev_contribution': 0.66, 'set_number': '25', 'image': 'https://images.pokemontcg.io/sv3pt5/25_hires.png'},
            {'name': 'Articuno ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 6.00, 'pull_rate': 0.083, 'ev_contribution': 0.50, 'set_number': '172', 'image': 'https://images.pokemontcg.io/sv3pt5/172_hires.png'},
            {'name': 'Snorlax (Illustration Rare)', 'rarity': 'Illustration Rare', 'price': 4.50, 'pull_rate': 0.055, 'ev_contribution': 0.25, 'set_number': '143', 'image': 'https://images.pokemontcg.io/sv3pt5/143_hires.png'},
            {'name': 'Eevee (Illustration Rare)', 'rarity': 'Illustration Rare', 'price': 8.00, 'pull_rate': 0.055, 'ev_contribution': 0.44, 'set_number': '133', 'image': 'https://images.pokemontcg.io/sv3pt5/133_hires.png'},
            {'name': 'Arcanine ex (Full Art)', 'rarity': 'Ultra Rare', 'price': 5.50, 'pull_rate': 0.083, 'ev_contribution': 0.46, 'set_number': '171', 'image': 'https://images.pokemontcg.io/sv3pt5/171_hires.png'},
        ]

        # Calculate total EV
        ev_total = sum(card['ev_contribution'] for card in top_cards)

        # Mock analysis with full card list
        analysis = {
            'product_name': product_name,
            'set_name': set_name,
            'set_id': 'sv3pt5',
            'timestamp': datetime.now().isoformat(),
            'pricing': {
                'sealed_box_cost': sealed_price,
                'market_value_sealed': sealed_price,
                'expected_value_open': ev_total,
                'projected_6mo_sealed': sealed_price * 1.15
            },
            'roi': {
                'open': {
                    'amount': ev_total - sealed_price,
                    'percent': ((ev_total - sealed_price) / sealed_price * 100)
                },
                'hold_6mo': {
                    'amount': (sealed_price * 1.15) - sealed_price,
                    'percent': 15.0
                },
                'resell_now': {
                    'amount': 0,
                    'percent': 0
                }
            },
            'recommendation': 'OPEN - Expected value significantly exceeds sealed price' if ev_total > sealed_price else 'HOLD SEALED - EV below sealed price',
            'confidence_score': 85,
            'ev_breakdown': {
                'ev_total': round(ev_total, 2),
                'top_cards': top_cards,
                'rarity_breakdown': {
                    'Special Illustration Rare': {'count': 3, 'total_value': 600.00},
                    'Ultra Rare': {'count': 12, 'total_value': 245.00},
                    'Double Rare': {'count': 5, 'total_value': 123.50},
                    'Illustration Rare': {'count': 7, 'total_value': 47.50}
                },
                'total_cards_analyzed': 207,
                'valuable_cards_count': len(top_cards),
                'api_source': 'Sample data based on 151 set market prices'
            },
            'assumptions': {
                'packs_per_box': 36,
                'pull_rates': 'Community averages',
                'min_card_value': 0.40,
                'hold_period': '6 months',
                'appreciation_estimate': '15% for sealed'
            },
            'api_sources': [
                'TCGPlayer market prices (sample data)',
                'Pokemon TCG 151 set cards with images'
            ]
        }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(analysis)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
