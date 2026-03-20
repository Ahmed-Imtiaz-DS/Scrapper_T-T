# 📊 Job Market Monitoring System - UCP Assignment 1

A production-ready ETL pipeline that monitors AI/ML/Data Science job markets across Spotify, OpenAI (Ashby), and Airbnb (Greenhouse) using **Selenium** for extraction, **Scrapy** for processing, and **Pandas** for analysis.

## 🎯 Project Objectives

✅ **Selenium Quality (20%)**: WebDriverWait, robust link repair, absolute URL reconstruction  
✅ **Scrapy Extraction (25%)**: Multi-source job detail extraction with skills parsing  
✅ **Analysis (10%)**: Workforce insights and market trends  
✅ **GitHub Discipline**: Proper branch workflow (master → develop → feature/)  

---

## 🚀 Quick Start

### 1. Setup Environment
```powershell
# Clone/navigate to project
cd "c:\Users\AHMED IMTIAZ\Desktop\Scrapper_T&T"

# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Download ChromeDriver
- Download from: https://chromedriver.chromium.org/
- Choose version matching your Chrome browser
- Extract to: `selenium\chromedriver.exe`

### 3. Run Pipeline
```powershell
# Complete pipeline (extract → scrape → analyze)
python run_project.py all

# Or run individually
python run_project.py extract    # Selenium extraction
python run_project.py scrape     # Scrapy spider
python run_project.py analyze    # Analysis
```

### 4. View Results
- **Raw links**: `data/raw/job_links.csv`
- **Processed jobs**: `data/final/jobs.csv`
- **Analysis**: `analysis/workforce_analysis.txt`

---

## 📁 Project Structure

```
Scrapper_T&T/
├── selenium/
│   ├── extractor.py          # Selenium job board scraper
│   └── chromedriver.exe      # ⬅ Download & place here
├── scrapy_project/
│   ├── spiders/
│   │   └── job_market.py     # Spider for job details
│   ├── items.py              # Item definitions
│   ├── pipelines.py          # Data processing pipelines
│   ├── settings.py           # Scrapy configuration
│   └── __init__.py
├── analysis/
│   └── summary.py            # Workforce analysis script
├── data/
│   ├── raw/                  # ⬅ Selenium output (job_links.csv)
│   └── final/                # ⬅ Scrapy output (jobs.csv)
├── data_utils.py             # Data utilities & validation
├── run_project.py            # Main CLI orchestrator
├── requirements.txt          # Python dependencies
├── .gitignore               # Git exclusions
└── README.md                # This file
```

---

## 🔍 What Each Component Does

### Selenium Extractor (`selenium/extractor.py`)
- **Targets**: Spotify Jobs, OpenAI (Ashby), Airbnb (Greenhouse)
- **Filters**: Data Science, Machine Learning, AI roles only
- **Quality Features**:
  - `WebDriverWait` for robust element loading
  - Dynamic scrolling to load all listings
  - Absolute URL reconstruction (repairs relative links)
  - Comprehensive logging
- **Output**: `data/raw/job_links.csv` (URL, title, company, source)

### Scrapy Spider (`scrapy_project/spiders/job_market.py`)
- **Input**: Reads from `data/raw/job_links.csv`
- **Extraction**: 
  - Job title, company, location, department
  - Employment type, posted date
  - Full job description & requirements
  - **Skills extraction**: Python, SQL, PyTorch, TensorFlow, Spark, R
- **Processing Pipeline**:
  1. **DataValidationPipeline** - Validates required fields
  2. **SkillsExtractionPipeline** - Extracts tech skills
  3. **DuplicateCheckPipeline** - Removes duplicates
  4. **CSVExportPipeline** - Saves to CSV
- **Output**: `data/final/jobs.csv` (12 fields, processed data)

### Analysis Script (`analysis/summary.py`)
Answers 5 key workforce questions:
1. **Top 5 Skills** - Most demanded tech skills
2. **Top 5 Locations** - Cities with most openings
3. **Top 5 Companies** - Active employers
4. **Entry-Level Positions** - Junior/internship roles
5. **Top Job Titles** - Common role patterns

**Output**: `analysis/workforce_analysis.txt` + console logs

---

## 📊 Data Fields Extracted

| Field | Source | Example |
|-------|--------|---------|
| job_title | Selenium/Page | "Senior Data Scientist" |
| company | Selenium | "Spotify" |
| location | Page scraping | "San Francisco, CA" |
| department | Page scraping | "Analytics" |
| employment_type | Page scraping | "Full-time" |
| job_description | Page HTML | Long text... |
| requirements | Page HTML | "5+ years Python..." |
| posted_date | Page metadata | "2024-01-15" |
| job_url | Page link | "https://..." |
| source | Selenium | "spotify" |
| skills | Extracted | "Python; SQL; PyTorch" |
| extracted_at | System | ISO timestamp |

---

## 🔧 Configuration

### Target Job Boards
Configured in `selenium/extractor.py`:
```python
JOB_BOARDS = {
    'spotify': {
        'url': 'https://www.spotifyjobs.com/jobs',
        'base_url': 'https://www.spotifyjobs.com',
        ...
    },
    'openai': {...},
    'airbnb': {...}
}
```

### Role Keywords
```python
ROLE_KEYWORDS = ['Data Science', 'Machine Learning', 'AI', ...]
```

### Skills Keywords
Configured in `scrapy_project/pipelines.py`:
```python
SKILL_KEYWORDS = {
    'python': r'\bpython\b',
    'sql': r'\b(sql|...)\b',
    'pytorch': r'\bpytorch\b',
    ...
}
```

---

## 🌳 Git Workflow (GitHub Discipline)

### Branch Structure
```
master (production-ready)
├── develop (integration branch)
│   └── feature/complete-pipeline (feature branch)
```

### Workflow Steps

**1. Start Work on Feature**
```powershell
git checkout develop
git pull origin develop
git checkout -b feature/complete-pipeline
```

**2. Make Commits**
```powershell
# After editing files
git add .
git commit -m "Add Selenium extractor with WebDriverWait"
git add .
git commit -m "Implement Scrapy spider with skills extraction"
git add .
git commit -m "Add analysis script and data utilities"
```

**3. Push Feature Branch**
```powershell
git push origin feature/complete-pipeline
```

**4. Create Pull Request**
- Go to GitHub repository
- Create PR: `feature/complete-pipeline` → `develop`
- Review code, add description
- Merge when approved

**5. Update Develop**
```powershell
git checkout develop
git pull origin develop
```

**6. Merge to Master (Production)**
```powershell
git checkout master
git pull origin master
git merge develop
git push origin master
```

### Commit Best Practices
- ✅ Atomic commits (one feature per commit)
- ✅ Descriptive messages (type: description format)
- ✅ Reference issues: "Fix #123: Add Selenium scraper"
- ✅ Keep commits focused and testable

---

## 📝 Data Processing Pipeline

```
SELENIUM STAGE
  |
  └─→ Job Links CSV (raw URLs, titles)
       |
       v
SCRAPY STAGE
  |
  ├─ ValidationPipeline ✓
  ├─ SkillsExtractionPipeline ✓
  ├─ DuplicateCheckPipeline ✓
  └─ CSVExportPipeline
       |
       └─→ Jobs CSV (full details)
            |
            v
ANALYSIS STAGE
  |
  ├─ Load jobs.csv
  ├─ Analyze skills, locations, companies
  ├─ Count entry-level positions
  ├─ Identify job title patterns
  └─ Generate workforce_analysis.txt
```

---

## 🐛 Troubleshooting

### "ChromeDriver not found"
```
✗ Solution: Download from https://chromedriver.chromium.org/
           Extract to selenium/chromedriver.exe
```

### "404 Not Found" errors
✓ **Fixed by**: 
- Proper WebDriverWait in Selenium
- Absolute URL repair with `urljoin()`
- Robust CSS selectors

### "No jobs extracted"
✓ **Check**:
1. Verify URLs are accessible
2. Check CSS selectors in `selenium/extractor.py`
3. Review `selenium/extraction.log`

### "CSV file not found"
✓ **Fix**: Run steps in order
```
python run_project.py extract  # First
python run_project.py scrape   # Second
python run_project.py analyze  # Third
```

---

## 📚 Key Technologies

| Tool | Purpose | Version |
|------|---------|---------|
| **Selenium** | Browser automation, job board scraping | 4.15.2 |
| **Scrapy** | Web scraping framework, job details | 2.11.0 |
| **Pandas** | Data analysis & manipulation | 2.1.3 |
| **NumPy** | Numerical operations | 1.26.2 |
| **lxml** | HTML/XML parsing | 4.9.3 |

---

## 📋 Rubric Compliance

### ✅ Selenium Quality (20%)
- [x] WebDriverWait for element loading
- [x] Dynamic scrolling to load all jobs
- [x] Absolute URL reconstruction
- [x] Comprehensive error handling
- [x] Logging and debugging

### ✅ Scrapy Extraction (25%)
- [x] Multi-stage processing pipelines
- [x] Skills extraction from descriptions
- [x] Data validation & deduplication
- [x] CSV export with 12+ fields
- [x] Robust HTML parsing

### ✅ Analysis (10%)
- [x] Top 5 skills analysis
- [x] Top 5 locations by openings
- [x] Top 5 companies hiring
- [x] Entry-level position count
- [x] Job title pattern analysis

### ✅ GitHub Discipline
- [x] master, develop, feature branches
- [x] Atomic, descriptive commits
- [x] Pull request workflow
- [x] Proper .gitignore

---

## 📧 Support

For issues or questions:
1. Check logs: `selenium/extraction.log`, `scrapy_project/logs/scrapy.log`
2. Review `data/raw/job_links.csv` for extracted links
3. Verify CSS selectors match current job board structure

---

## 📄 License

University of Central Punjab - Assignment 1
