import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed for this script
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL of the job listings page
url = "https://berlinstartupjobs.com/engineering/"

# Send a GET request to the specified URL with custom headers
response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    verify=False,  # Bypass SSL verification (not recommended for production)
)

# List of skills to search for in job listings
skills = ["python", "typescript", "javascript", "rust"]

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all job listings
job_listings = soup.find_all("li", class_="bjs-jlid")

# Iterate over each job listing
for job in job_listings:
    # Find the a tag within the h4 tag in one step
    a_element = job.find("h4").find("a") if job.find("h4") else None
    if a_element:
        title = a_element.text.strip()
        print("Job Title:", title)

    # Find the skills element
    skills_elements = (
        job.find("div", class_="links-box").find_all("a")
        if job.find("div", class_="links-box")
        else None
    )

    if skills_elements:
        # Extract text from each a tag and join them with commas
        skills_text = ", ".join([element.text.strip() for element in skills_elements])

        # Find matching skills
        skills_found = [
            skill.strip()
            for skill in skills_text.split(",")
            if skill.strip().lower() in skills
        ]

        # Print matching skills if any are found
        if skills_found:
            print("Skills:", skills_found)
            print("----")
