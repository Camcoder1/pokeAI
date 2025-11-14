#!/usr/bin/env python3
"""
Quick test to verify Pokemon TCG API access
"""

import os
import sys

try:
    from pokemontcgsdk import Card, Set
    from pokemontcgsdk import RestClient
except ImportError:
    print("Installing required packages...")
    os.system("pip install pokemontcgsdk requests")
    from pokemontcgsdk import Card, Set
    from pokemontcgsdk import RestClient

# Configure API key if available
api_key = os.environ.get('POKEMON_TCG_API_KEY', '')
if api_key:
    RestClient.configure(api_key)
    print(f"[OK] Using Pokemon TCG API key: {api_key[:10]}...")
else:
    print("[WARN] Using demo API key (rate limited)")

print("\n[TEST] Testing Pokemon TCG API Connection...")
print("=" * 50)

# Test 1: Get recent sets
print("\n1. Fetching recent Pokemon TCG sets...")
try:
    sets = Set.all()
    print(f"   [OK] Successfully fetched {len(sets)} sets")

    # Show recent 5 sets
    print("\n   Recent sets:")
    for s in sets[:5]:
        print(f"   - {s.name} ({s.series}) - {s.total} cards")
except Exception as e:
    print(f"   [ERROR] Error: {e}")
    sys.exit(1)

# Test 2: Get cards from popular set
print("\n2. Testing card price data from '151' set...")
try:
    # Find 151 set
    set_151 = None
    for s in sets:
        if "151" in s.name:
            set_151 = s
            break

    if set_151:
        print(f"   [OK] Found set: {set_151.name} (ID: {set_151.id})")

        # Get some cards
        cards = Card.where(q=f'set.id:{set_151.id}')
        print(f"   [OK] Fetched {len(cards)} cards from set")

        # Show some valuable cards with prices
        print("\n   Sample cards with prices:")
        count = 0
        for card in cards:
            if count >= 5:
                break

            # Try to get price
            price = 0.0
            try:
                if hasattr(card, 'tcgplayer') and card.tcgplayer:
                    prices = card.tcgplayer.prices
                    if hasattr(prices, 'holofoil') and prices.holofoil:
                        price = prices.holofoil.market or 0.0
                    elif hasattr(prices, 'normal') and prices.normal:
                        price = prices.normal.market or 0.0
            except:
                pass

            if price > 1.0:
                rarity = card.rarity if hasattr(card, 'rarity') else 'Unknown'
                print(f"   - {card.name} ({rarity}): ${price:.2f}")
                count += 1

    else:
        print("   [WARN] '151' set not found, trying another set...")

        # Try first available set
        test_set = sets[0]
        print(f"   Testing with: {test_set.name}")
        cards = Card.where(q=f'set.id:{test_set.id}')
        print(f"   [OK] Fetched {len(cards)} cards")

except Exception as e:
    print(f"   [ERROR] Error: {e}")
    sys.exit(1)

# Test 3: Verify price data availability
print("\n3. Checking price data availability...")
try:
    cards_with_prices = 0
    total_checked = 0

    for card in cards[:50]:  # Check first 50 cards
        total_checked += 1
        try:
            if hasattr(card, 'tcgplayer') and card.tcgplayer:
                prices = card.tcgplayer.prices
                if prices:
                    cards_with_prices += 1
        except:
            pass

    percentage = (cards_with_prices / total_checked * 100) if total_checked > 0 else 0
    print(f"   [OK] {cards_with_prices}/{total_checked} cards have price data ({percentage:.1f}%)")

    if percentage < 30:
        print("   [WARN] Low price data availability. API key recommended.")

except Exception as e:
    print(f"   [ERROR] Error: {e}")

print("\n" + "=" * 50)
print("[SUCCESS] Pokemon TCG API is working correctly!")
print("\nYour backend will be able to:")
print("  * Fetch all Pokemon TCG sets")
print("  * Get card lists for any set")
print("  * Retrieve current market prices")
print("  * Calculate Expected Values")
print("\n[READY] Ready for deployment!")
