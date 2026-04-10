
from flask import current_app
import time



def send_due_date_notification(task_title):
    with current_app.app_context():
        time.sleep(5)
        print(f"Reminder: Task '{task_title}' is due soon!")