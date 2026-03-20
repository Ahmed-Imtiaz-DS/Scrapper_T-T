"""
Scrapy Settings Configuration
"""

BOT_NAME = 'job_market_analyzer'

SPIDER_MODULES = ['scrapy_project.spiders']
NEWSPIDER_MODULE = 'scrapy_project.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests per domain
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies
COOKIES_ENABLED = False

# Configure user agent
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Configure download delay
DOWNLOAD_DELAY = 2

# Disable default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'scrapy_project/httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [404, 410]

# Configure pipelines
ITEM_PIPELINES = {
    'scrapy_project.pipelines.DataValidationPipeline': 100,
    'scrapy_project.pipelines.SkillsExtractionPipeline': 200,
    'scrapy_project.pipelines.DuplicateCheckPipeline': 300,
    'scrapy_project.pipelines.CSVExportPipeline': 400,
}

# Enable and configure logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'scrapy_project/logs/scrapy.log'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# Disable SSL verification for development (be careful in production)
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Configure timeouts
DOWNLOAD_TIMEOUT = 30
