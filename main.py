from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
# replace with your own email and password
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service('/usr/bin/chromedriver')

with webdriver.Chrome(service=service, options=chrome_options) as d:
    d.get("https://github.com/Ouckah/Summer2025-Internships")
    d.maximize_window()
    cur_jobs = d.find_elements(By.CSS_SELECTOR, value="table")

    cur_jobs = cur_jobs[1].find_elements(By.CSS_SELECTOR, value="tbody tr")

    with open("jobs.txt", "r") as f:
        prev_jobs = f.read().strip()
        prev_jobs_count = int(float(prev_jobs))

    with open("jobs.txt", "w") as f:
        f.write(str(len(cur_jobs)))

    if len(cur_jobs) > prev_jobs_count:
        new_jobs_count = len(cur_jobs) - prev_jobs_count
        new_jobs = cur_jobs[0:new_jobs_count]

        content = ""
        for j in new_jobs:
            for t in j.text.split("\n"):
                content += t + "\n"

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = f"{new_jobs_count} new jobs posted!"
        msg.attach(MIMEText(content, 'plain', 'utf-8'))

        with SMTP("smtp.gmail.com") as c:
            c.starttls()
            c.login(user=email, password=password)
            c.sendmail(from_addr=email,
                       to_addrs=email, msg=msg.as_string())
        