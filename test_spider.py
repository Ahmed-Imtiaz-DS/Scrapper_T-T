"""
Quick test to debug the spider
"""
import csv
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Check if CSV exists and load it
try:
    with open('data/raw/job_links.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        jobs = list(reader)
    logger.info(f"Loaded {len(jobs)} job links")
    
    # Show first few jobs
    for i, job in enumerate(jobs[:3]):
        logger.info(f"Job {i+1}: {job['title']} - {job['url']}")
        # Try to fetch the page
        import requests
        try:
            response = requests.get(job['url'], timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            logger.info(f"  Status: {response.status_code}")
            if response.status_code == 200:
                logger.info(f"  Content length: {len(response.text)} chars")
        except Exception as e:
            logger.error(f"  Error fetching: {str(e)}")
            
except Exception as e:
    logger.error(f"Error: {str(e)}")
    sys.exit(1)
