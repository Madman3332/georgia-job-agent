import time
from scraper import scrape_jobs_ge
from ai_filter import filter_jobs
from telegram_bot import handle_updates, send_message
from database import init_db, init_settings, job_already_sent, mark_job_as_sent

CHAT_ID = "YOUR_CHAT_ID_HERE"  # replace this

def job_check():
    jobs = scrape_jobs_ge()
    relevant_jobs = filter_jobs(jobs)

    for job in relevant_jobs:
        if not job_already_sent(job["link"]):
            message = f"""
📌 {job['title']}
💰 Salary: {job['salary'] if job['salary'] else "Not specified"}
🔗 {job['link']}
"""
            send_message(CHAT_ID, message)
            mark_job_as_sent(job["link"])


def run():
    init_db()
    init_settings()

    print("🤖 Bot is running...")

    while True:
        handle_updates()  # listen for commands
        time.sleep(2)


if __name__ == "__main__":
    run()