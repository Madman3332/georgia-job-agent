import os
import time
from dotenv import load_dotenv

from scraper import scrape_jobs_ge
from ai_filter import filter_jobs
from telegram_bot import handle_updates, send_message
from database import init_db, init_settings, job_already_sent, mark_job_as_sent


# Load local .env (safe for Railway too)
load_dotenv()

CHAT_ID = os.getenv("CHAT_ID")

if not CHAT_ID:
    raise RuntimeError("CHAT_ID is missing. Set it in .env locally or Railway Variables.")


# -----------------------------
# JOB SCANNING LOGIC
# -----------------------------

def job_check():
    print("🔎 Checking for new jobs...")

    jobs = scrape_jobs_ge()
    relevant_jobs = filter_jobs(jobs)

    new_jobs_found = False

    for job in relevant_jobs:
        if not job_already_sent(job["link"]):
            message = (
                f"📌 {job['title']}\n\n"
                f"💰 Salary: {job['salary'] if job['salary'] else 'Not specified'}\n\n"
                f"🔗 {job['link']}"
            )

            send_message(CHAT_ID, message)
            mark_job_as_sent(job["link"])
            new_jobs_found = True

    if not new_jobs_found:
        print("No new relevant jobs found.")


# -----------------------------
# MAIN BOT LOOP
# -----------------------------

def run():
    init_db()
    init_settings()

    print("🤖 Bot is running...")

    last_job_check = 0
    JOB_CHECK_INTERVAL = 1800  # 30 minutes (in seconds)

    while True:
        try:
            # Always listen for Telegram commands
            handle_updates()

            # Run job scan every 30 minutes
            current_time = time.time()
            if current_time - last_job_check > JOB_CHECK_INTERVAL:
                job_check()
                last_job_check = current_time

            time.sleep(2)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    run()