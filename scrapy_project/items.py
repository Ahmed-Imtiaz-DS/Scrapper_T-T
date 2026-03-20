"""
Scrapy Item Definitions for Job Data
"""

import scrapy


class JobItem(scrapy.Item):
    """Job listing item with all extracted fields."""
    
    # Core job information
    job_title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    department = scrapy.Field()
    
    # Employment details
    employment_type = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_currency = scrapy.Field()
    
    # Content
    job_description = scrapy.Field()
    requirements = scrapy.Field()
    
    # Metadata
    posted_date = scrapy.Field()
    job_url = scrapy.Field()
    source = scrapy.Field()
    
    # Extracted skills
    skills = scrapy.Field()
    
    # Processing metadata
    extracted_at = scrapy.Field()
    last_updated = scrapy.Field()
