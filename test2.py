import threading
import time
from datetime import datetime, timedelta

def run_at_midnight(task_func):
    def run():
        while True:
            now = datetime.now()
            # Calculate seconds until next midnight
            next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            wait_seconds = (next_midnight - now).total_seconds()
            time.sleep(wait_seconds)
            # Run your task
            task_func()
    threading.Thread(target=run, daemon=True).start()

def midnight_task():
    print("✅ It's 12:00 AM! Daily task is running...")

# Start the background midnight watcher
run_at_midnight(midnight_task)
