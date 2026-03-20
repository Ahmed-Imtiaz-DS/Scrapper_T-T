"""
Debug script to test spider functionality
"""
import csv
import os
from pathlib import Path

# Check if CSV file exists
csv_file = 'data/raw/job_links.csv'

if not os.path.exists(csv_file):
    print(f"ERROR: {csv_file} not found!")
else:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        jobs = list(reader)
    
    print(f"✓ Loaded {len(jobs)} job links from {csv_file}")
    
    # Show first few jobs
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job['title']}")
        print(f"   URL: {job['url']}")
        print(f"   Company: {job['company']}")
        print(f"   Source: {job['source']}")

# Check if final CSV exists
final_csv = 'data/final/jobs.csv'
if os.path.exists(final_csv):
    with open(final_csv, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"\n\nFinal CSV Status:")
    print(f"✓ File exists: {final_csv}")
    print(f"  Lines: {len(lines)}")
    if len(lines) > 1:
        print(f"  Data rows: {len(lines) - 1}")
        # Show first data row
        print(f"  First row: {lines[1][:100]}...")
    else:
        print(f"  ✗ Only header present, no data rows")
else:
    print(f"\n✗ Final CSV not found: {final_csv}")

# Check cache directory
cache_dir = 'scrapy_project/job_cache_fresh2/requests.queue'
if os.path.exists(cache_dir):
    import os
    files = os.listdir(cache_dir)
    print(f"\n\nCache queue files: {len(files)}")
else:
    print(f"\n✗ Cache directory not found: {cache_dir}")
