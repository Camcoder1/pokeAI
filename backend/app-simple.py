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

        # Mock analysis
        analysis = {
            'product_name': product_name,
            'set_name': set_name,
            'set_id': 'sv04',
            'timestamp': datetime.now().isoformat(),
            'pricing': {
                'sealed_box_cost': sealed_price,
                'market_value_sealed': sealed_price,
                'expected_value_open': 145.50,
                'projected_6mo_sealed': sealed_price * 1.15
            },
            'roi': {
                'open': {
                    'amount': 145.50 - sealed_price,
                    'percent': ((145.50 - sealed_price) / sealed_price * 100)
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
            'recommendation': 'OPEN - Expected value significantly exceeds sealed price',
            'confidence_score': 75,
            'ev_breakdown': {
                'ev_total': 145.50,
                'top_cards': [
                    {
                        'name': 'Charizard ex',
                        'rarity': 'Ultra Rare',
                        'price': 45.00,
                        'pull_rate': 0.028,
                        'ev_contribution': 1.26,
                        'set_number': '006',
                        'image': 'https://images.pokemontcg.io/sv04/6.png'
                    },
                    {
                        'name': 'Mew ex',
                        'rarity': 'Ultra Rare',
                        'price': 35.00,
                        'pull_rate': 0.028,
                        'ev_contribution': 0.98,
                        'set_number': '151',
                        'image': 'https://images.pokemontcg.io/sv04/151.png'
                    }
                ],
                'rarity_breakdown': {
                    'Ultra Rare': {'count': 15, 'total_value': 450.00},
                    'Full Art': {'count': 20, 'total_value': 320.00}
                },
                'total_cards_analyzed': 207,
                'valuable_cards_count': 45,
                'api_source': 'Mock data - Pokemon TCG API integration pending'
            },
            'assumptions': {
                'packs_per_box': 36,
                'pull_rates': 'Community averages',
                'min_card_value': 0.40,
                'hold_period': '6 months',
                'appreciation_estimate': '15% for sealed'
            },
            'api_sources': [
                'Mock data for testing',
                'Pokemon TCG API integration in progress'
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
