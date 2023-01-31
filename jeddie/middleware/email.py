import smtplib

from config import config
from database.model import Item


def log_to_email(item: Item, buyer: str, stripe_id: str):
    smtp = smtplib.SMTP(config.EMAIL_HOSTNAME, 587)
    smtp.starttls()
    smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
    message = f'Gift of ${item.price / 100} received from {buyer} via Stripe (transaction ID: {stripe_id}).'
    smtp.sendmail(config.EMAIL_USERNAME, config.EMAIL_RECIPIENT, message)
    smtp.quit()
