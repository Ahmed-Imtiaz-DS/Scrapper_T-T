# ⚡ QUICKSTART - Run in 5 Minutes

## Step 1: Activate Virtual Environment
```powershell
cd "c:\Users\AHMED IMTIAZ\Desktop\Scrapper_T&T"
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Step 2: Get ChromeDriver
1. Go to https://chromedriver.chromium.org/
2. Download version matching your Chrome browser
3. Extract `chromedriver.exe` to `selenium\` folder

## Step 3: Run Everything
```powershell
python run_project.py all
```

## ✅ Done!
- **Job links**: `data/raw/job_links.csv`
- **Full data**: `data/final/jobs.csv`
- **Analysis**: `analysis/workforce_analysis.txt`

## 🔧 Run Individual Steps
```powershell
python run_project.py extract    # Only Selenium
python run_project.py scrape     # Only Scrapy
python run_project.py analyze    # Only Analysis
```

## 📊 View Results
Open `data/final/jobs.csv` in Excel or text editor to see:
- Job titles
- Companies
- Locations
- Extracted skills
- Job descriptions
- And more...

## 🌳 Git Commands
```powershell
# Check status
git status

# Make commits
git add .
git commit -m "Your message"

# Push to GitHub
git branch  # See current branch
git push origin develop
```

---

💡 **Tip**: First run takes 5-10 minutes. Subsequent runs are faster due to caching.
