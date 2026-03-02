import subprocess
import os
from multiprocessing import Pool

# List of websites to check
WEBSITES = [
    "https://www.website.com",
    "https://www.website2.com"
]

PYTHON_EXECUTABLE = ".venv/bin/python"  # Path to Python executable
SCRIPT_PATH = "src/find_broken.py"  # Path to the broken link checker script


def check_site(site):
    print(f"Checking broken links for: {site}")
    subprocess.run([PYTHON_EXECUTABLE, SCRIPT_PATH, site])
    print(f"Finished checking {site}.")


if __name__ == "__main__":
    with Pool(
        cpu = os.cpu_count()
        processes = min(32, cpu * 5)
    ) as pool:  # You can adjust the number of processes based on cores
        pool.map(check_site, WEBSITES)

    print("All sites checked.")

