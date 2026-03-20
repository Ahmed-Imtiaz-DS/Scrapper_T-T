"""
Test fetching and parsing a single job page
"""
import requests
from bs4 import BeautifulSoup
import csv

# Get first job URL from CSV
with open('data/raw/job_links.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    first_job = next(reader)

url = first_job['url']
print(f"Testing URL: {url}")
print(f"Title: {first_job['title']}")
print(f"Company: {first_job['company']}\n")

try:
    # Fetch the page
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0'}
    response = requests.get(url, timeout=10, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)} chars\n")
    
    if response.status_code == 200:
        # Check what HTML we got
        print("First 500 chars of response:")
        print(response.text[:500])
        print("\n...")
        
        # Try parsing with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for <h1> tags
        h1s = soup.find_all('h1')
        print(f"\nFound {len(h1s)} <h1> tags")
        if h1s:
            for h1 in h1s[:3]:
                print(f"  {h1.get_text()[:100]}")
        
        # Look for job description patterns        
        description_ele = soup.find(class_=lambda x: x and 'description' in x.lower())
        if description_ele:
            print(f"\nFound description element: {description_ele.name}")
            print(f"Text: {description_ele.get_text()[:200]}...")
        else:
            print("\nNo description element found")
            
        # Count paragraphs
        ps = soup.find_all('p')
        print(f"\nFound {len(ps)} <p> tags")
        if ps:
            print(f"First p: {ps[0].get_text()[:150]}...")
            
except Exception as e:
    print(f"Error: {str(e)}")
