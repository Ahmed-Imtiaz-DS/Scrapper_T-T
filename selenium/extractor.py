"""
Selenium Job Board Extractor - UCP Assignment 1
Extracts Data Science, ML, and AI roles from Spotify, OpenAI, and Airbnb job boards.
Implements WebDriverWait, dynamic scrolling, and absolute URL reconstruction.
"""

import csv
import time
import logging
from datetime import datetime
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('selenium/extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Role keywords to filter
ROLE_KEYWORDS = ['Data Science', 'Machine Learning', 'AI', 'Artificial Intelligence', 'ML']
TARGET_KEYWORDS_LOWERCASE = [kw.lower() for kw in ROLE_KEYWORDS]

# Job board configurations
JOB_BOARDS = {
    'spotify': {
        'name': 'Spotify',
        'url': 'https://www.spotifyjobs.com/jobs',
        'base_url': 'https://www.spotifyjobs.com',
        'job_card_selector': 'div[data-job-id], a[data-job-id]',
        'link_selector': 'a',
        'title_selector': 'h2, h3, span[class*="title"]',
        'wait_time': 10
    },
    'openai': {
        'name': 'OpenAI',
        'url': 'https://jobs.ashbyhq.com/openai',
        'base_url': 'https://jobs.ashbyhq.com',
        'job_card_selector': 'a[href*="/openai/"]',
        'link_selector': 'a',
        'title_selector': 'h2, h3, div[class*="title"]',
        'wait_time': 10
    },
    'airbnb': {
        'name': 'Airbnb',
        'url': 'https://boards.greenhouse.io/airbnb',
        'base_url': 'https://boards.greenhouse.io',
        'job_card_selector': 'div[class*="opening"], a[class*="job"]',
        'link_selector': 'a',
        'title_selector': 'h2, h3, span[class*="title"]',
        'wait_time': 10
    }
}


class JobBoardScraper:
    """Scrapes job listings from multiple boards with role filtering."""
    
    def __init__(self, headless=True, chromedriver_path='selenium/chromedriver'):
        """Initialize Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
        
        self.wait = WebDriverWait(self.driver, 10)
        self.job_links = []
    
    def is_target_role(self, text):
        """Check if job title contains target role keywords."""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in TARGET_KEYWORDS_LOWERCASE)
    
    def scroll_and_load(self, max_scrolls=10):
        """Scroll page to load all dynamic job listings."""
        previous_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0
        
        while scrolls < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == previous_height:
                logger.info(f"Reached end of page after {scrolls + 1} scrolls")
                break
            previous_height = new_height
            scrolls += 1
        
        logger.info(f"Completed scrolling: {scrolls} scroll(s)")
    
    def repair_url(self, href, base_url):
        """Convert relative URLs to absolute URLs."""
        if not href:
            return None
        if href.startswith('http://') or href.startswith('https://'):
            return href
        # Remove query params/fragments if just a path
        if href.startswith('#'):
            return None
        # Handle relative URLs
        return urljoin(base_url, href)
    
    def scrape_board(self, board_key):
        """Scrape a specific job board."""
        board = JOB_BOARDS[board_key]
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting: {board['name']} ({board['url']})")
        logger.info(f"{'='*60}")
        
        try:
            self.driver.get(board['url'])
            time.sleep(3)  # Initial page load
            
            # Wait for job cards to load
            try:
                self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, board['job_card_selector'])))
                logger.info("Job cards loaded")
            except TimeoutException:
                logger.warning(f"Timeout waiting for job cards on {board['name']}")
                return []
            
            # Scroll to load all listings
            self.scroll_and_load(max_scrolls=15)
            
            # Extract all job links
            board_links = []
            try:
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, board['job_card_selector'])
                logger.info(f"Found {len(job_elements)} job elements")
                
                for idx, element in enumerate(job_elements):
                    try:
                        # Extract title
                        title_text = ""
                        try:
                            title_elem = element.find_element(By.CSS_SELECTOR, board['title_selector'])
                            title_text = title_elem.text.strip()
                        except NoSuchElementException:
                            pass
                        
                        # Check if it's a target role
                        if not self.is_target_role(title_text):
                            continue
                        
                        # Extract link
                        try:
                            link_elem = element.find_element(By.CSS_SELECTOR, board['link_selector'])
                            href = link_elem.get_attribute('href')
                        except NoSuchElementException:
                            href = element.get_attribute('href')
                        
                        # Repair URL to make absolute
                        absolute_url = self.repair_url(href, board['base_url'])
                        
                        if absolute_url:
                            board_links.append({
                                'url': absolute_url,
                                'title': title_text,
                                'company': board['name'],
                                'source': board_key
                            })
                            logger.debug(f"  ✓ {idx+1}. {title_text[:50]}... → {absolute_url}")
                    
                    except Exception as e:
                        logger.debug(f"  Error processing element {idx}: {str(e)}")
                        continue
            
            except Exception as e:
                logger.error(f"Error extracting links from {board['name']}: {str(e)}")
                return []
            
            logger.info(f"{board['name']}: Extracted {len(board_links)} valid links")
            return board_links
        
        except Exception as e:
            logger.error(f"Error scraping {board['name']}: {str(e)}")
            return []
    
    def save_to_csv(self, links, output_file='data/raw/job_links.csv'):
        """Save extracted links to CSV."""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['url', 'title', 'company', 'source', 'extracted_at'])
                writer.writeheader()
                for link in links:
                    link['extracted_at'] = datetime.now().isoformat()
                    writer.writerow(link)
            logger.info(f"\n✓ Saved {len(links)} links to {output_file}")
        except Exception as e:
            logger.error(f"Error saving CSV: {str(e)}")
            raise
    
    def run_all(self):
        """Run extraction for all job boards."""
        try:
            all_links = []
            for board_key in JOB_BOARDS.keys():
                links = self.scrape_board(board_key)
                all_links.extend(links)
                time.sleep(2)  # Pause between boards
            
            logger.info(f"\n{'='*60}")
            logger.info(f"TOTAL EXTRACTED: {len(all_links)} job links")
            logger.info(f"{'='*60}")
            
            if all_links:
                self.save_to_csv(all_links)
                return all_links
            else:
                logger.warning("No jobs extracted. Check selectors and wait times.")
                return []
        
        finally:
            self.driver.quit()
            logger.info("WebDriver closed")


def main():
    """Main execution."""
    logger.info("Starting Job Board Extraction")
    logger.info(f"Looking for roles: {', '.join(ROLE_KEYWORDS)}")
    
    scraper = JobBoardScraper(headless=False)  # Set headless=True for production
    links = scraper.run_all()
    
    if links:
        logger.info(f"\n✅ Successfully extracted {len(links)} job links")
        logger.info("Next step: Run Scrapy spider with 'python run_project.py scrape'")
    else:
        logger.warning("⚠️  No jobs extracted. Update selector configurations if needed.")
    
    return len(links)


if __name__ == '__main__':
    try:
        count = main()
        sys.exit(0 if count > 0 else 1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
