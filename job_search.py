import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO   = os.environ.get("EMAIL_TO")

URLS = [
    "https://www.indeed.com/jobs?q=playwright+automation",
    "https://www.indeed.com/jobs?q=manual+tester+entry+level",
    "https://www.indeed.com/jobs?q=qa+tester+startup"
]

KEYWORDS = ["playwright", "manual", "qa", "tester", "automation"]

def get_jobs():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in URLS:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        for job in soup.select(".job_seen_beacon"):
            title = job.find("h2")
            if title:
                title_text = title.text.strip()
                if any(k in title_text.lower() for k in KEYWORDS):
                    jobs.append(title_text)

    return jobs


def send_email(job_list):
    if not job_list:
        body = "No new matching jobs today."
    else:
        body = "\n".join(job_list)

    msg = MIMEText(body)
    msg["Subject"] = "Daily Playwright & Manual Testing Jobs"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASS)
    server.send_message(msg)
    server.quit()


if __name__ == "__main__":
    jobs = get_jobs()
    send_email(jobs)
