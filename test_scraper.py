"""
Test script to verify the setup works
"""

from scraper import KhaltiScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_scraper():
    """Test the scraper functionality"""
    event_id = "ET25AMY4AUYM"
    scraper = KhaltiScraper(event_id)

    logger.info("Testing scraper with Khalti API...")
    
    # Fetch data from API
    api_data = scraper.fetch_events_api()
    
    if api_data:
        logger.info("✓ Successfully fetched API data")
        logger.info(f"  Event: {api_data.get('title')}")
        
        # Parse the event data
        cards = scraper.parse_event_data(api_data)
        logger.info(f"✓ Found {len(cards)} event card(s)")

        if cards:
            logger.info("\nEvent Details:")
            for i, card in enumerate(cards, 1):
                logger.info(f"\n  Card {i}:")
                logger.info(f"    Title: {card.get('title')}")
                logger.info(f"    Date: {card.get('date')}")
                logger.info(f"    Location: {card.get('location')}")
                logger.info(f"    Status: {card.get('status')}")
                logger.info(f"    Price: {card.get('price')}")
                logger.info(f"    Sold Out: {card.get('is_sold_out')}")
    else:
        logger.error("✗ Failed to fetch API data")

if __name__ == "__main__":
    test_scraper()
