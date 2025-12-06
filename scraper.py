"""
Web scraper for Khalti events site
Uses the official Khalti API endpoint to fetch event data in JSON format
"""

import requests
from typing import Dict, List, Optional
import logging
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)



class KhaltiScraper:
    def __init__(self, event_id: str, timeout: int = 15):
        self.event_id = event_id
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with proper headers and retry strategy"""
        session = requests.Session()
        
        # Retry strategy for resilience
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Browser-like headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
        })
        
        return session

    def fetch_events_api(self) -> Optional[Dict]:
        """Fetch event data from Khalti API"""
        if not self.event_id:
            logger.error("Event ID not found in URL")
            return None
        
        api_url = f"https://khalti.com/api/e5/events/{self.event_id}/children/"
        
        try:
            logger.info(f"Fetching from API: {api_url}")
            response = self.session.get(api_url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"API response received successfully")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching from API: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing API response: {e}")
            return None

    def parse_event_data(self, api_data: Dict) -> List[Dict]:
        """Parse event data from API response"""
        try:
            cards = []
            
            if not api_data or 'children' not in api_data:
                logger.warning("No children events found in API response")
                return cards
            
            children = api_data.get('children', [])
            logger.info(f"Found {len(children)} event(s) in API response")
            
            for event in children:
                try:
                    ticket_info = self._extract_api_ticket_info(event)
                    if ticket_info:
                        cards.append(ticket_info)
                        logger.debug(f"Extracted: {ticket_info.get('title')} - {ticket_info.get('status')}")
                except Exception as e:
                    logger.debug(f"Error parsing event: {e}")
                    continue
            
            logger.info(f"Parsed {len(cards)} event card(s)")
            return cards
            
        except Exception as e:
            logger.error(f"Error parsing event data: {e}")
            return []

    def _extract_api_ticket_info(self, event: Dict) -> Optional[Dict]:
        """Extract ticket information from API event object"""
        try:
            # Determine availability status
            is_sold_out = event.get('is_sold_out', False)
            status = event.get('status')  # e.g., "Filling Fast", "Sold Out"
            
            if is_sold_out:
                status = "Sold Out"
            elif not status:
                status = "Available"
            
            # Extract price
            price = None
            price_data = event.get('price', {})
            if price_data:
                min_price = price_data.get('min_price')
                max_price = price_data.get('max_price')
                
                if min_price and max_price:
                    if min_price == max_price:
                        price = f"Rs. {min_price // 100}"  # Convert paisa to rupees
                    else:
                        price = f"Rs. {min_price // 100} - Rs. {max_price // 100}"
                elif min_price:
                    price = f"Rs. {min_price // 100}"
            
            ticket_info = {
                'title': event.get('title', 'N/A'),
                'date': event.get('date', 'N/A'),
                'location': event.get('location', 'N/A'),
                'status': status,
                'price': price,
                'image_url': event.get('web_image_url') or event.get('image_url'),
                'is_sold_out': is_sold_out,
                'start_date': event.get('start_date'),
                'event_id': event.get('idx')
            }
            
            return ticket_info
            
        except Exception as e:
            logger.debug(f"Error extracting ticket info from API: {e}")
            return None

    def get_available_tickets(self) -> Optional[List[Dict]]:
        """Get list of available tickets from API"""
        try:
            api_data = self.fetch_events_api()
            if not api_data:
                logger.error("Failed to fetch API data")
                return None
            
            cards = self.parse_event_data(api_data)
            
            if not cards:
                logger.info("No events found in API response")
                return None
            
            # Filter for non-sold-out tickets
            available = [card for card in cards if not card.get('is_sold_out', False)]
            
            if available:
                logger.info(f"Found {len(available)} available ticket(s) out of {len(cards)} total")
                for ticket in available:
                    logger.debug(f"  - {ticket.get('title')}: {ticket.get('status', 'Available')}")
                return available
            else:
                logger.info("All tickets are sold out")
                return None
                
        except Exception as e:
            logger.error(f"Error getting available tickets: {e}", exc_info=True)
            return None
        finally:
            # Clean up session
            if self.session:
                try:
                    self.session.close()
                except:
                    pass
