Broken Link Checker Made by Bruen Smith This script is a Scrapy-based web crawler designed to find broken links on a given website.
It scans a website, follows internal links, checks external links, and logs broken ones in a CSV file.

Setup Instructions
1. Create a Virtual Environment and Install Dependencies
First, set up a virtual environment and install Scrapy and scraper_helper.
Windows (Command Prompt / PowerShell)
python -m venv .venv  
.venv\Scripts\activate  
pip install scrapy scraper_helper  
Mac/Linux (Terminal)
python3 -m venv .venv  
source .venv/bin/activate  
pip install scrapy scraper_helper  
2. Update multi_run.py for Your System
The script now executes find_broken.py with a specific Python executable.
	•	Open multi_run.py and update the PYTHON_EXECUTABLE variable (line 14) to match your system's Python environment.
	•	Update SCRIPT_PATH (line 16) if necessary to reflect the correct location of find_broken.py.
Example (Windows)
PYTHON_EXECUTABLE = "C:/Users/YourName/Projects/Scrapy/.venv/Scripts/python.exe"
SCRIPT_PATH = "src/find_broken.py"
Example (Mac/Linux)
PYTHON_EXECUTABLE = "/home/yourname/Projects/Scrapy/.venv/bin/python"
SCRIPT_PATH = "src/find_broken.py"
💡 If you don’t update these paths, the script may not execute properly.
3. Configure Websites to Scan
	•	Open multi_run.py
	•	Edit the WEBSITES list (starting at line 5) to update the list of websites to scan.
Example:
WEBSITES = [
    "https://www.bethel.k12.or.us",
    "https://cascade.bethel.k12.or.us",
    "https://clearlake.bethel.k12.or.us",
    "https://danebo.bethel.k12.or.us",
    "https://fairfield.bethel.k12.or.us",
    "https://irving.bethel.k12.or.us",
    "https://malabon.bethel.k12.or.us",
    "https://shasta.bethel.k12.or.us",
    "https://willamette.bethel.k12.or.us",
    "https://meadowview.bethel.k12.or.us",
    "https://kalapuya.bethel.k12.or.us",
    "https://prairiemountain.bethel.k12.or.us"
]
4. Run the Script
The script will check each website one by one, pausing between checks.
Windows (PowerShell/Command Prompt)
python multi_run.py
Mac/Linux (Terminal)
python3 multi_run.py
Output Files
Broken links are saved in broken_links_reports/ with a timestamped CSV file:
broken_links_reports/example_com_broken_links_YYYY-MM-DD_HH-MM-SS.csv
Notes
	•	The script ignores robots.txt (change ROBOTSTXT_OBEY=True in find_broken.py to respect it).
	•	Adjust RETRY_TIMES in find_broken.py to retry failed requests.
	•	The script now ensures all output files are saved in broken_links_reports/ automatically.
	•	If you run into permission issues, try running with admin privileges (Windows) or sudo (Mac/Linux). (Be careful if you do this!)
🚀 Now you're ready to find broken links! 🚀
