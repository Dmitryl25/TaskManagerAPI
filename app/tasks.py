from .celery_app import celery_app

@celery_app.task
def send_welcome_email(email: str):
    print(f"Sending welcome email to {email}")
