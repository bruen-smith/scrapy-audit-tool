import subprocess
from multiprocessing import Pool

# List of websites to check
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
    "https://prairiemountain.bethel.k12.or.us",
]

PYTHON_EXECUTABLE = ".venv/bin/python"  # Path to Python executable
SCRIPT_PATH = "src/find_broken.py"  # Path to the broken link checker script


def check_site(site):
    print(f"Checking broken images for: {site}")
    subprocess.run([PYTHON_EXECUTABLE, SCRIPT_PATH, site])
    print(f"Finished checking {site}.")


if __name__ == "__main__":
    with Pool(
        processes=12
    ) as pool:  # You can adjust the number of processes based on cores
        pool.map(check_site, WEBSITES)

    print("All sites checked.")
