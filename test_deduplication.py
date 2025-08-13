#!/usr/bin/env python3
"""
Test script to verify the deduplication system works correctly
"""

import os
import json
import sys
sys.path.append('.')

from github_pokemon_monitor import GitHubCostcoPokemonMonitor

def test_deduplication():
    print("🧪 Testing Product Deduplication System")
    print("=" * 50)
    
    # Clean slate for testing
    if os.path.exists('known_products.json'):
        os.remove('known_products.json')
        print("🗑️  Removed existing known_products.json for clean test")
    
    # Create monitor instance
    monitor = GitHubCostcoPokemonMonitor()
    
    # Simulate some products
    test_products = [
        {
            'title': 'Pokemon Charizard ex Super-Premium Collection',
            'price': '$119.99',
            'availability': 'In Stock',
            'url': 'https://www.costco.com.au/test1'
        },
        {
            'title': 'Pokemon Pikachu Trading Card Set',
            'price': '$59.99', 
            'availability': 'In Stock',
            'url': 'https://www.costco.com.au/test2'
        }
    ]
    
    print(f"📦 Testing with {len(test_products)} sample products")
    
    # First run - should detect all as new
    print("\n🔍 First run (should find all products as new):")
    new_products_1 = monitor.check_for_new_products(test_products)
    print(f"   Found {len(new_products_1)} new products")
    for product in new_products_1:
        print(f"   ✅ NEW: {product['title']}")
    
    # Save the products
    monitor.save_known_products_to_github()
    print(f"💾 Saved {len(monitor.known_products)} products to file")
    
    # Second run - should detect none as new (same products)
    print("\n🔍 Second run (should find no new products):")
    monitor_2 = GitHubCostcoPokemonMonitor()  # Fresh instance to test loading
    new_products_2 = monitor_2.check_for_new_products(test_products)
    print(f"   Found {len(new_products_2)} new products")
    if new_products_2:
        print("   ❌ ERROR: Should have found 0 new products!")
        for product in new_products_2:
            print(f"   ❌ DUPLICATE: {product['title']}")
    else:
        print("   ✅ SUCCESS: No duplicates detected!")
    
    # Third run - add one new product
    print("\n🔍 Third run (adding one new product):")
    test_products.append({
        'title': 'Pokemon Mew ex Collection Box',
        'price': '$79.99',
        'availability': 'In Stock', 
        'url': 'https://www.costco.com.au/test3'
    })
    
    new_products_3 = monitor_2.check_for_new_products(test_products)
    print(f"   Found {len(new_products_3)} new products")
    if len(new_products_3) == 1:
        print(f"   ✅ SUCCESS: Found only the new product: {new_products_3[0]['title']}")
    else:
        print(f"   ❌ ERROR: Expected 1 new product, found {len(new_products_3)}")
    
    # Check the saved file
    print("\n📄 Checking saved file contents:")
    if os.path.exists('known_products.json'):
        with open('known_products.json', 'r') as f:
            data = json.load(f)
            print(f"   File contains {len(data['products'])} products")
            print(f"   Last updated: {data['last_updated']}")
    
    print("\n✅ Deduplication test complete!")
    print("💡 If you saw 'SUCCESS' messages above, the system is working correctly")
    
if __name__ == "__main__":
    test_deduplication()
