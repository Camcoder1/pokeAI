"""
Pokemon TCG Market Analyst - Lambda Handler
Analyzes sealed products for Open vs Hold vs Resell decisions
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import boto3
from pokemontcgsdk import Card, Set
from pokemontcgsdk import RestClient
import requests

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'pokemon-tcg-analytics')
table = dynamodb.Table(table_name)

# Configure Pokemon TCG SDK
RestClient.configure(os.environ.get('POKEMON_TCG_API_KEY', ''))

# Pull rate estimations (community averages)
PULL_RATES = {
    'Common': 1.0,  # Not counted in EV
    'Uncommon': 1.0,  # Not counted in EV
    'Rare': 0.25,  # 1 per 4 packs
    'Rare Holo': 0.166,  # 1 per 6 packs
    'Ultra Rare': 0.166,  # 1 per 6 packs
    'Full Art': 0.083,  # 1 per 12 packs
    'Secret Rare': 0.028,  # 1 per 36 packs
    'Illustration Rare': 0.055,  # 1 per 18 packs
    'Special Illustration Rare': 0.055,
    'Hyper Rare': 0.020,  # 1 per 50 packs
    'Gold Rare': 0.020,  # 1 per 50 packs
}

# Minimum card value to include in EV calculation
MIN_CARD_VALUE = 0.40

# Standard booster box configuration
PACKS_PER_BOX = 36
CARDS_PER_PACK = 10


def lambda_handler(event, context):
    """Main Lambda handler"""

    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }

    try:
        path = event.get('path', '')
        method = event.get('httpMethod', '')

        # Handle CORS preflight
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }

        # Route requests
        if path == '/analyze' and method == 'POST':
            return analyze_product(event, headers)
        elif path.startswith('/analyze/') and method == 'GET':
            product_id = path.split('/')[-1]
            return get_analysis(product_id, headers)
        elif path == '/sets' and method == 'GET':
            return list_sets(headers)
        elif path == '/trending' and method == 'GET':
            return get_trending(headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def analyze_product(event, headers):
    """Analyze a sealed product for Open/Hold/Resell decision"""

    try:
        body = json.loads(event.get('body', '{}'))
        product_name = body.get('product_name')
        set_name = body.get('set_name')
        sealed_price = body.get('sealed_price')  # Optional - will fetch if not provided

        if not product_name and not set_name:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'product_name or set_name required'})
            }

        # Step 1: Get set data from Pokemon TCG API
        pokemon_set = find_set(set_name or product_name)
        if not pokemon_set:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Set not found'})
            }

        # Step 2: Get all cards in the set
        cards = get_cards_for_set(pokemon_set.id)

        # Step 3: Get card prices and calculate EV
        ev_data = calculate_expected_value(cards, pokemon_set.id)

        # Step 4: Get sealed product price
        if not sealed_price:
            sealed_price = estimate_sealed_price(pokemon_set.name, product_name)

        # Step 5: Calculate ROI metrics
        analysis = generate_recommendation(
            ev_data=ev_data,
            sealed_price=sealed_price,
            set_name=pokemon_set.name,
            set_id=pokemon_set.id,
            product_name=product_name or f"{pokemon_set.name} Booster Box"
        )

        # Step 6: Store in DynamoDB for analytics
        store_analysis(analysis)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(analysis, default=str)
        }

    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def find_set(search_term: str) -> Optional[Set]:
    """Find a Pokemon TCG set by name"""
    try:
        # Search for sets matching the term
        sets = Set.where(q=f'name:"{search_term}"')
        if sets:
            return sets[0]

        # Try partial match
        all_sets = Set.all()
        for s in all_sets:
            if search_term.lower() in s.name.lower():
                return s

        return None
    except Exception as e:
        print(f"Set search error: {str(e)}")
        return None


def get_cards_for_set(set_id: str) -> List[Card]:
    """Get all cards for a specific set"""
    try:
        cards = Card.where(q=f'set.id:{set_id}')
        return cards
    except Exception as e:
        print(f"Card fetch error: {str(e)}")
        return []


def calculate_expected_value(cards: List[Card], set_id: str) -> Dict:
    """Calculate expected value of opening packs"""

    ev_total = 0.0
    card_breakdown = []
    rarity_stats = {}

    for card in cards:
        try:
            # Get card price
            price = get_card_price(card)

            if price < MIN_CARD_VALUE:
                continue

            # Get rarity
            rarity = card.rarity
            pull_rate = get_pull_rate(rarity)

            # Calculate contribution to EV
            ev_contribution = price * pull_rate * PACKS_PER_BOX
            ev_total += ev_contribution

            # Track stats
            if rarity not in rarity_stats:
                rarity_stats[rarity] = {'count': 0, 'total_value': 0}
            rarity_stats[rarity]['count'] += 1
            rarity_stats[rarity]['total_value'] += price

            # Store card data if significant contributor (>=5% of EV)
            if ev_contribution >= (ev_total * 0.05) or price >= 10:
                card_breakdown.append({
                    'name': card.name,
                    'rarity': rarity,
                    'price': round(price, 2),
                    'pull_rate': pull_rate,
                    'ev_contribution': round(ev_contribution, 2),
                    'set_number': card.number,
                    'image': card.images.small if hasattr(card, 'images') else None
                })

        except Exception as e:
            print(f"Error processing card {card.name}: {str(e)}")
            continue

    # Sort by EV contribution
    card_breakdown.sort(key=lambda x: x['ev_contribution'], reverse=True)

    return {
        'ev_total': round(ev_total, 2),
        'top_cards': card_breakdown[:20],  # Top 20 contributors
        'rarity_breakdown': rarity_stats,
        'total_cards_analyzed': len(cards),
        'valuable_cards_count': len(card_breakdown),
        'api_source': 'pokemontcg.io'
    }


def get_card_price(card: Card) -> float:
    """Get card market price from TCGPlayer or CardMarket"""
    try:
        # Try to get TCGPlayer market price
        if hasattr(card, 'tcgplayer') and card.tcgplayer:
            prices = card.tcgplayer.prices

            # Try different price types
            if hasattr(prices, 'holofoil') and prices.holofoil:
                return prices.holofoil.market or 0.0
            elif hasattr(prices, 'normal') and prices.normal:
                return prices.normal.market or 0.0
            elif hasattr(prices, 'reverseHolofoil') and prices.reverseHolofoil:
                return prices.reverseHolofoil.market or 0.0

        # Fallback to CardMarket
        if hasattr(card, 'cardmarket') and card.cardmarket:
            prices = card.cardmarket.prices
            if hasattr(prices, 'averageSellPrice'):
                return prices.averageSellPrice or 0.0

        return 0.0

    except Exception as e:
        print(f"Price fetch error for {card.name}: {str(e)}")
        return 0.0


def get_pull_rate(rarity: str) -> float:
    """Get pull rate for a rarity type"""
    # Try exact match
    if rarity in PULL_RATES:
        return PULL_RATES[rarity]

    # Try partial matches
    rarity_lower = rarity.lower()
    if 'secret' in rarity_lower or 'sr' in rarity_lower:
        return PULL_RATES['Secret Rare']
    elif 'hyper' in rarity_lower:
        return PULL_RATES['Hyper Rare']
    elif 'gold' in rarity_lower:
        return PULL_RATES['Gold Rare']
    elif 'illustration rare' in rarity_lower:
        return PULL_RATES['Illustration Rare']
    elif 'full art' in rarity_lower or 'ultra rare' in rarity_lower:
        return PULL_RATES['Full Art']
    elif 'holo' in rarity_lower:
        return PULL_RATES['Rare Holo']
    elif 'rare' in rarity_lower:
        return PULL_RATES['Rare']

    # Default
    return 0.05


def estimate_sealed_price(set_name: str, product_name: str) -> float:
    """Estimate sealed product price (simplified - would use TCGPlayer API in production)"""

    # Check cache first
    cached = get_cached_price(product_name)
    if cached:
        return cached

    # Default estimates by product type
    if 'booster box' in product_name.lower():
        return 100.0  # Default booster box price
    elif 'etb' in product_name.lower() or 'elite trainer' in product_name.lower():
        return 50.0
    elif 'booster bundle' in product_name.lower():
        return 25.0
    else:
        return 100.0  # Default


def generate_recommendation(ev_data: Dict, sealed_price: float, set_name: str,
                            set_id: str, product_name: str) -> Dict:
    """Generate Open vs Hold vs Resell recommendation"""

    ev_open = ev_data['ev_total']

    # Calculate ROI metrics
    roi_open = ev_open - sealed_price
    roi_open_percent = (roi_open / sealed_price * 100) if sealed_price > 0 else 0

    # Estimate hold value (simplified - would use historical data in production)
    projected_6mo_price = sealed_price * 1.15  # Assume 15% appreciation
    roi_hold = projected_6mo_price - sealed_price
    roi_hold_percent = (roi_hold / sealed_price * 100) if sealed_price > 0 else 0

    # Resell now (assuming no markup for simplicity)
    roi_resell = 0
    roi_resell_percent = 0

    # Determine recommendation
    recommendation = determine_recommendation(
        roi_open_percent, roi_hold_percent, roi_resell_percent, ev_open, sealed_price
    )

    # Calculate confidence score
    confidence = calculate_confidence(ev_data, sealed_price)

    return {
        'product_name': product_name,
        'set_name': set_name,
        'set_id': set_id,
        'timestamp': datetime.now().isoformat(),
        'pricing': {
            'sealed_box_cost': round(sealed_price, 2),
            'market_value_sealed': round(sealed_price, 2),
            'expected_value_open': round(ev_open, 2),
            'projected_6mo_sealed': round(projected_6mo_price, 2)
        },
        'roi': {
            'open': {
                'amount': round(roi_open, 2),
                'percent': round(roi_open_percent, 2)
            },
            'hold_6mo': {
                'amount': round(roi_hold, 2),
                'percent': round(roi_hold_percent, 2)
            },
            'resell_now': {
                'amount': round(roi_resell, 2),
                'percent': round(roi_resell_percent, 2)
            }
        },
        'recommendation': recommendation,
        'confidence_score': confidence,
        'ev_breakdown': ev_data,
        'assumptions': {
            'packs_per_box': PACKS_PER_BOX,
            'pull_rates': 'Community averages (see documentation)',
            'min_card_value': MIN_CARD_VALUE,
            'hold_period': '6 months',
            'appreciation_estimate': '15% for sealed'
        },
        'api_sources': [
            'pokemontcg.io for card data',
            'TCGPlayer market prices from Pokemon TCG SDK'
        ]
    }


def determine_recommendation(roi_open_pct: float, roi_hold_pct: float,
                             roi_resell_pct: float, ev_open: float,
                             sealed_price: float) -> str:
    """Determine the best action: OPEN, HOLD, or RESELL"""

    # OPEN if EV significantly exceeds sealed price
    if roi_open_pct > 20 and ev_open > sealed_price * 1.2:
        return "OPEN - Expected value significantly exceeds sealed price"

    # HOLD if sealed is appreciating and EV is lower
    elif roi_hold_pct > roi_open_pct and ev_open < sealed_price:
        return "HOLD SEALED - Sealed product likely to appreciate, EV below cost"

    # RESELL if sealed is inflated above EV
    elif sealed_price > ev_open * 1.3:
        return "RESELL SEALED NOW - Sealed price inflated above expected value"

    # Default to HOLD for marginal cases
    else:
        return "HOLD SEALED - Marginal expected value, sealed preservation recommended"


def calculate_confidence(ev_data: Dict, sealed_price: float) -> int:
    """Calculate confidence score 1-100"""

    confidence = 50  # Base confidence

    # More cards analyzed = higher confidence
    if ev_data['total_cards_analyzed'] > 200:
        confidence += 20
    elif ev_data['total_cards_analyzed'] > 100:
        confidence += 10

    # More valuable cards = higher confidence
    if ev_data['valuable_cards_count'] > 50:
        confidence += 15
    elif ev_data['valuable_cards_count'] > 20:
        confidence += 10

    # API data available
    if ev_data.get('api_source'):
        confidence += 15

    return min(confidence, 100)


def store_analysis(analysis: Dict):
    """Store analysis in DynamoDB for analytics"""
    try:
        # Generate unique ID
        analysis_id = f"{analysis['set_id']}_{int(time.time())}"

        # Store in DynamoDB
        table.put_item(
            Item={
                'pk': f"ANALYSIS#{analysis['set_id']}",
                'sk': f"TIMESTAMP#{analysis['timestamp']}",
                'analysis_id': analysis_id,
                'timestamp': int(datetime.now().timestamp()),
                'product_name': analysis['product_name'],
                'set_name': analysis['set_name'],
                'recommendation': analysis['recommendation'],
                'ev_open': analysis['pricing']['expected_value_open'],
                'sealed_price': analysis['pricing']['sealed_box_cost'],
                'confidence': analysis['confidence_score'],
                'data': json.dumps(analysis)
            }
        )

        # Also store in trending cache
        update_trending_cache(analysis)

    except Exception as e:
        print(f"DynamoDB store error: {str(e)}")


def update_trending_cache(analysis: Dict):
    """Update trending products cache"""
    try:
        table.put_item(
            Item={
                'pk': 'TRENDING',
                'sk': f"SET#{analysis['set_id']}",
                'timestamp': int(datetime.now().timestamp()),
                'set_name': analysis['set_name'],
                'product_name': analysis['product_name'],
                'ev_open': analysis['pricing']['expected_value_open'],
                'sealed_price': analysis['pricing']['sealed_box_cost'],
                'roi_percent': analysis['roi']['open']['percent'],
                'recommendation': analysis['recommendation'],
                'ttl': int((datetime.now() + timedelta(days=7)).timestamp())
            }
        )
    except Exception as e:
        print(f"Trending cache error: {str(e)}")


def get_analysis(product_id: str, headers: Dict) -> Dict:
    """Retrieve stored analysis by ID"""
    try:
        # Query DynamoDB
        response = table.query(
            KeyConditionExpression='pk = :pk',
            ExpressionAttributeValues={
                ':pk': f"ANALYSIS#{product_id}"
            },
            Limit=1,
            ScanIndexForward=False  # Most recent first
        )

        if response['Items']:
            item = response['Items'][0]
            return {
                'statusCode': 200,
                'headers': headers,
                'body': item.get('data', '{}')
            }
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Analysis not found'})
            }

    except Exception as e:
        print(f"Get analysis error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def list_sets(headers: Dict) -> Dict:
    """List available Pokemon TCG sets"""
    try:
        sets = Set.all()
        set_list = [
            {
                'id': s.id,
                'name': s.name,
                'series': s.series,
                'release_date': s.releaseDate,
                'total_cards': s.total,
                'logo': s.images.logo if hasattr(s, 'images') else None
            }
            for s in sets[:50]  # Limit to recent 50 sets
        ]

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'sets': set_list}, default=str)
        }

    except Exception as e:
        print(f"List sets error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def get_trending(headers: Dict) -> Dict:
    """Get trending analyses"""
    try:
        response = table.query(
            KeyConditionExpression='pk = :pk',
            ExpressionAttributeValues={
                ':pk': 'TRENDING'
            },
            Limit=20,
            ScanIndexForward=False
        )

        trending = []
        for item in response.get('Items', []):
            trending.append({
                'set_name': item.get('set_name'),
                'product_name': item.get('product_name'),
                'ev_open': item.get('ev_open'),
                'sealed_price': item.get('sealed_price'),
                'roi_percent': item.get('roi_percent'),
                'recommendation': item.get('recommendation'),
                'timestamp': item.get('timestamp')
            })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'trending': trending})
        }

    except Exception as e:
        print(f"Get trending error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def get_cached_price(product_name: str) -> Optional[float]:
    """Get cached sealed price from DynamoDB"""
    try:
        response = table.get_item(
            Key={
                'pk': 'PRICE_CACHE',
                'sk': f"PRODUCT#{product_name}"
            }
        )

        if 'Item' in response:
            item = response['Item']
            # Check if cache is still valid (1 hour TTL)
            cached_time = item.get('timestamp', 0)
            if time.time() - cached_time < 3600:
                return item.get('price')

        return None

    except Exception as e:
        print(f"Cache fetch error: {str(e)}")
        return None
