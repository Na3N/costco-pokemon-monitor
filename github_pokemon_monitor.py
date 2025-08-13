#!/usr/bin/env python3
"""
Costco Australia Pokemon Set Monitor - GitHub Actions Version
Runs once per execution (GitHub Actions will schedule it)
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import urllib.parse

class GitHubCostcoPokemonMonitor:
    def __init__(self):
        self.base_url = "https://www.costco.com.au"
        self.search_url = f"{self.base_url}/search?text=pokemon"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.known_products = set()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Load existing products from previous runs
        self.load_known_products_from_github()
    
    def load_known_products_from_github(self):
        """Load previously found products from JSON file"""
        try:
            if os.path.exists('known_products.json'):
                with open('known_products.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.known_products = set(data.get('products', []))
                    logging.info(f"Loaded {len(self.known_products)} known products from file")
            else:
                logging.info("No previous products file found, starting fresh")
        except Exception as e:
            logging.error(f"Error loading products from file: {e}")
            self.known_products = set()
    
    def save_known_products_to_github(self):
        """Save known products to JSON file for next run"""
        try:
            data = {
                'products': list(self.known_products),
                'last_updated': datetime.now().isoformat()
            }
            with open('known_products.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved {len(self.known_products)} known products to file")
        except Exception as e:
            logging.error(f"Error saving products to file: {e}")
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options for GitHub Actions"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            return driver
        except Exception as e:
            logging.error(f"Error setting up WebDriver: {e}")
            return None
    
    def fetch_pokemon_products(self):
        """Fetch Pokemon products from Costco Australia using Selenium"""
        driver = None
        try:
            logging.info("Starting browser to fetch Pokemon products from Costco Australia...")
            driver = self.setup_driver()
            if not driver:
                return []
            
            # Navigate to search page
            driver.get(self.search_url)
            
            # Wait for page to load and check for content
            wait = WebDriverWait(driver, 20)
            
            products = []
            
            try:
                # Wait for the page to load
                wait.until(lambda d: 
                    d.find_elements(By.CSS_SELECTOR, '[data-testid*="product"], .product, [class*="product"], .no-results, .search-results') or 
                    "no results" in d.page_source.lower() or
                    len(d.find_elements(By.TAG_NAME, "a")) > 10
                )
                
                # Give extra time for dynamic content to load
                time.sleep(5)
                
                # Get page source and parse with BeautifulSoup
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Try multiple strategies to find products
                product_selectors = [
                    '[data-testid*="product"]',
                    '.product-item',
                    '.product-card', 
                    '.product-list-item',
                    '.product-tile',
                    '[class*="product"][class*="item"]',
                    'a[href*="/p/"]',  # Product page links
                    'article',
                    '.search-result',
                ]
                
                all_potential_products = []
                
                for selector in product_selectors:
                    elements = soup.select(selector)
                    if elements:
                        logging.info(f"Found {len(elements)} elements with selector: {selector}")
                        all_potential_products.extend(elements)
                
                # Also search in text content for Pokemon mentions
                text_content = soup.get_text().lower()
                if 'pokemon' in text_content:
                    logging.info("✅ Found 'pokemon' in page text content")
                    
                    # Look for any links that might be products
                    all_links = soup.find_all('a', href=True)
                    for link in all_links:
                        link_text = link.get_text().lower()
                        if 'pokemon' in link_text or 'tcg' in link_text or 'trading' in link_text:
                            all_potential_products.append(link)
                
                # Process potential products
                seen_urls = set()
                
                for element in all_potential_products:
                    try:
                        # Get URL first for deduplication
                        url = ""
                        if element.name == 'a' and element.get('href'):
                            url = element['href']
                        else:
                            link_elem = element.find('a')
                            if link_elem and link_elem.get('href'):
                                url = link_elem['href']
                        
                        if url and not url.startswith('http'):
                            url = self.base_url + url
                        
                        # Skip duplicates by URL
                        if url and url in seen_urls:
                            continue
                        if url:
                            seen_urls.add(url)
                        
                        # Extract title/product name
                        title = None
                        title_selectors = ['h1', 'h2', 'h3', 'h4', '.product-title', '.product-name', '[data-testid*="title"]']
                        
                        for selector in title_selectors:
                            title_elem = element.select_one(selector)
                            if title_elem:
                                title = title_elem.get_text().strip()
                                break
                        
                        if not title:
                            title = element.get_text().strip()
                        
                        # Clean up title
                        if title:
                            import re
                            title = re.sub(r'\s+', ' ', title)
                            lines = title.split('\n')
                            for line in lines:
                                line = line.strip()
                                if line and ('pokemon' in line.lower() or 'tcg' in line.lower()):
                                    if len(line) > 10 and len(line) < 200:
                                        title = line
                                        break
                        
                        # Skip if no title or title doesn't contain Pokemon-related terms
                        if not title or not any(term in title.lower() for term in ['pokemon', 'pokémon', 'tcg', 'trading card']):
                            continue
                        
                        # Get price
                        price = "Price not found"
                        price_selectors = ['.price', '[class*="price"]', '[data-testid*="price"]', '.cost']
                        
                        for selector in price_selectors:
                            price_elem = element.select_one(selector)
                            if price_elem:
                                price_text = price_elem.get_text().strip()
                                if '$' in price_text or 'aud' in price_text.lower():
                                    price = price_text
                                    break
                        
                        # Get availability
                        availability = "Unknown"
                        availability_selectors = ['.stock', '.availability', '[class*="stock"]', '[class*="availability"]']
                        
                        for selector in availability_selectors:
                            avail_elem = element.select_one(selector)
                            if avail_elem:
                                availability = avail_elem.get_text().strip()
                                break
                        
                        product = {
                            'title': title,
                            'url': url,
                            'price': price,
                            'availability': availability,
                            'found_at': datetime.now().isoformat()
                        }
                        products.append(product)
                        
                        logging.info(f"Found Pokemon product: {title[:50]}...")
                        
                    except Exception as e:
                        logging.error(f"Error parsing product element: {e}")
                        continue
                
                if not products:
                    logging.info("No Pokemon products found")
                    logging.info(f"Page title: {soup.find('title').get_text() if soup.find('title') else 'No title'}")
                    logging.info(f"Page contains 'pokemon': {'pokemon' in text_content}")
                    logging.info(f"Total links on page: {len(soup.find_all('a'))}")
                
            except TimeoutException:
                logging.warning("Timeout waiting for page to load")
                return []
            
            logging.info(f"Found {len(products)} Pokemon products")
            return products
            
        except Exception as e:
            logging.error(f"Error fetching products with Selenium: {e}")
            return []
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def check_for_new_products(self, products):
        """Check if there are any new products"""
        new_products = []
        
        for product in products:
            product_key = f"{product['title']}|{product['price']}"
            if product_key not in self.known_products:
                new_products.append(product)
                self.known_products.add(product_key)
        
        return new_products
    
    def send_discord_notification(self, new_products, webhook_url):
        """Send Discord webhook notification to #new_products channel"""
        if not new_products or not webhook_url:
            return
            
        try:
            for product in new_products:
                embed = {
                    "title": "🎉 NEW POKEMON PRODUCT FOUND!",
                    "description": f"**{product['title']}**",
                    "color": 0x00ff00,
                    "fields": [
                        {"name": "💰 Price", "value": product['price'], "inline": True},
                        {"name": "📊 Availability", "value": product['availability'], "inline": True},
                        {"name": "🔗 URL", "value": f"[View Product]({product['url']})", "inline": False}
                    ],
                    "timestamp": product['found_at']
                }
                
                data = {
                    "content": "@everyone New Pokemon drop detected! 🚨",
                    "embeds": [embed]
                }
                
                response = requests.post(webhook_url, json=data)
                if response.status_code == 204:
                    logging.info("Discord notification sent successfully to #new_products")
                else:
                    logging.error(f"Discord notification failed: {response.status_code}")
                    
        except Exception as e:
            logging.error(f"Error sending Discord notification: {e}")
    
    def send_telegram_notification(self, new_products, bot_token, chat_id):
        """Send Telegram bot notification"""
        if not new_products or not bot_token or not chat_id:
            return
            
        try:
            for product in new_products:
                message = (
                    f"🎉 *NEW POKEMON PRODUCT FOUND!*\\n\\n"
                    f"📦 *Product:* {product['title']}\\n"
                    f"💰 *Price:* {product['price']}\\n"
                    f"📊 *Availability:* {product['availability']}\\n"
                    f"🔗 [View Product]({product['url']})\\n"
                    f"⏰ *Found at:* {product['found_at']}"
                )
                
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": False
                }
                
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    logging.info("Telegram notification sent successfully")
                else:
                    logging.error(f"Telegram notification failed: {response.status_code}")
                    
        except Exception as e:
            logging.error(f"Error sending Telegram notification: {e}")
    
    def send_ntfy_notification(self, new_products, topic_url):
        """Send ntfy.sh notification"""
        if not new_products or not topic_url:
            return
            
        try:
            for product in new_products:
                title = "🎉 New Pokemon Product Found!"
                message = (
                    f"📦 {product['title']}\\n"
                    f"💰 {product['price']}\\n"
                    f"📊 {product['availability']}\\n"
                    f"🔗 {product['url']}"
                )
                
                headers = {
                    "Title": title,
                    "Priority": "high",
                    "Tags": "shopping,pokemon,alert"
                }
                
                response = requests.post(topic_url, data=message.encode('utf-8'), headers=headers)
                if response.status_code == 200:
                    logging.info("ntfy notification sent successfully")
                else:
                    logging.error(f"ntfy notification failed: {response.status_code}")
                    
        except Exception as e:
            logging.error(f"Error sending ntfy notification: {e}")

def main():
    monitor = GitHubCostcoPokemonMonitor()
    
    # Get notification config from environment variables
    discord_webhook = os.environ.get('DISCORD_WEBHOOK')
    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    ntfy_topic = os.environ.get('NTFY_TOPIC')
    
    logging.info("🔍 Starting Costco Australia Pokemon Monitor (GitHub Actions)")
    
    # Fetch current products
    products = monitor.fetch_pokemon_products()
    
    if products:
        # Check for new products
        new_products = monitor.check_for_new_products(products)
        
        if new_products:
            logging.info(f"🎉 Found {len(new_products)} new Pokemon product(s)!")
            
            for product in new_products:
                logging.info(f"NEW PRODUCT: {product['title']} - {product['price']} - {product['url']}")
            
            # Send notifications
            if discord_webhook:
                monitor.send_discord_notification(new_products, discord_webhook)
            
            if telegram_bot_token and telegram_chat_id:
                monitor.send_telegram_notification(new_products, telegram_bot_token, telegram_chat_id)
            
            if ntfy_topic:
                monitor.send_ntfy_notification(new_products, ntfy_topic)
        else:
            logging.info("No new products found")
        
        # Save known products for next run
        monitor.save_known_products_to_github()
        
    else:
        logging.warning("No products found - website might be down or structure changed")

if __name__ == "__main__":
    main()
