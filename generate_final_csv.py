"""
Simple direct CSV generation from job links
"""
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import time

# Setup
input_csv = 'data/raw/job_links.csv'
output_csv = 'data/final/jobs.csv'
Path(output_csv).parent.mkdir(parents=True, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Read job links
print("Loading job links...")
jobs = []
with open(input_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    jobs = list(reader)

print(f"Loaded {len(jobs)} job links")

# Process and write to CSV
print(f"Processing jobs and writing to {output_csv}...")
processed = 0
failed = 0

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'job_title', 'company', 'location', 'department', 'employment_type',
        'job_description', 'requirements', 'posted_date', 'job_url', 'source', 
        'skills', 'extracted_at'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for i, job in enumerate(jobs, 1):
        try:
            url = job.get('url')
            if not url:
                continue
            
            # Fetch the page
            response = requests.get(url, timeout=15, headers=headers)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract description from common locations
                description = ''
                # Try multiple selectors
                desc_elem = soup.find(class_=lambda x: x and 'description' in (x.lower() if x else ''))
                if desc_elem:
                    description = desc_elem.get_text().strip()[:500]
                else:
                    # Try main content
                    main = soup.find('main') or soup.find(role='main')
                    if main:
                        description = main.get_text().strip()[:500]
                    else:
                        description = soup.body.get_text().strip()[:500] if soup.body else 'Not available'
                
                # Clean description
                description = ' '.join(description.split())
                
                # Write row
                writer.writerow({
                    'job_title': job.get('title', ''),
                    'company': job.get('company', ''),
                    'location': '',
                    'department': '',
                    'employment_type': '',
                    'job_description': description,
                    'requirements': '',
                    'posted_date': '',
                    'job_url': url,
                    'source': job.get('source', ''),
                    'skills': '',
                    'extracted_at': datetime.now().isoformat()
                })
                
                processed += 1
                if processed % 10 == 0:
                    print(f"  Processed: {processed}/{len(jobs)}")
            else:
                print(f"  ✗ Failed to fetch {url} (status {response.status_code})")
                failed += 1
                
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ✗ Error processing job {i}: {str(e)}")
            failed += 1

print(f"\n✓ Complete!")
print(f"  Processed: {processed}")
print(f"  Failed: {failed}")
print(f"  CSV saved to: {output_csv}")
