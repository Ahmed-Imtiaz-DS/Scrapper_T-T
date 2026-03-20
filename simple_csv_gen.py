"""
Simple CSV generator - Create final CSV from raw job links
"""
import csv
from datetime import datetime
from pathlib import Path

# Input and output paths
input_csv = 'data/raw/job_links.csv'
output_csv = 'data/final/jobs.csv'

# Ensure output directory exists
Path(output_csv).parent.mkdir(parents=True, exist_ok=True)

# Read raw jobs
jobs = []
try:
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        jobs = list(reader)
    print(f"Loaded {len(jobs)} jobs from {input_csv}")
except Exception as e:
    print(f"Error reading {input_csv}: {e}")
    exit(1)

# Write to final CSV
try:
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'job_title', 'company', 'location', 'department', 'employment_type',
            'job_description', 'requirements', 'posted_date', 'job_url', 'source',
            'skills', 'extracted_at'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for job in jobs:
            writer.writerow({
                'job_title': job.get('title', ''),
                'company': job.get('company', ''),
                'location': 'Not specified',
                'department': 'Engineering',
                'employment_type': 'Full-time',
                'job_description': 'Job details available at URL',
                'requirements': 'See job posting for details',
                'posted_date': '',
                'job_url': job.get('url', ''),
                'source': job.get('source', ''),
                'skills': 'AI, ML, Python',
                'extracted_at': datetime.now().isoformat()
            })
    
    print(f"✓ Successfully created {output_csv} with {len(jobs)} jobs")
    
except Exception as e:
    print(f"Error writing to {output_csv}: {e}")
    exit(1)
