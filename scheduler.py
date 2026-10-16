import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import time
import argparse
import schedule
import pandas as pd
from database import get_connection, save_execution, create_tables
from automator import run_test

def run_daily_campaigns():
    """Executes all active campaigns scheduled for daily execution."""
    print("[SCHEDULER] Starting daily campaigns cycle...")
    create_tables()
    conn = get_connection()
    campaigns = pd.read_sql("SELECT * FROM campaigns WHERE daily=1 AND status='active'", conn)
    conn.close()

    if campaigns.empty:
        print("[SCHEDULER] No active daily campaigns found.")
        return

    print(f"[SCHEDULER] Found {len(campaigns)} campaign(s) to execute.")
    for _, camp in campaigns.iterrows():
        camp_dict = camp.to_dict()
        print(f"\n[*] Running campaign: {camp_dict.get('name')} (ID: {camp_dict.get('id')})")
        
        if not camp_dict.get("newsletter_url"):
            print(f"[WARN] Skipped campaign ID {camp_dict.get('id')}: No newsletter URL configured.")
            continue

        try:
            results = run_test(camp_dict)
            save_execution(camp_dict["id"], results)
            print(f"[OK] Campaign ID {camp_dict.get('id')} completed and saved to history.")
        except Exception as e:
            print(f"[ERROR] Failed to run campaign ID {camp_dict.get('id')}: {e}")

def start_scheduler(run_at="09:00"):
    """Starts the continuous daily scheduler loop."""
    print(f"[SCHEDULER] Scheduled daily at {run_at}.")
    schedule.every().day.at(run_at).do(run_daily_campaigns)
    
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Newsletter Tester Scheduler")
    parser.add_argument("--once", action="store_true", help="Execute daily campaigns once and exit immediately (ideal for Windows Task Scheduler / Cron)")
    parser.add_argument("--time", type=str, default="09:00", help="Time of day to run when in continuous mode (HH:MM format)")
    args = parser.parse_args()

    if args.once:
        print("[SCHEDULER] Running in single-pass mode (--once)...")
        run_daily_campaigns()
        print("[SCHEDULER] Single-pass finished. Exiting.")
        sys.exit(0)
    else:
        run_daily_campaigns()
        start_scheduler(run_at=args.time)