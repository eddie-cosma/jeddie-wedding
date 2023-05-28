import smtplib
from threading import Thread

from config import config


def threading(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@threading
def log_to_email(message: str):
    if config.EMAIL_HOSTNAME and config.EMAIL_USERNAME \
            and config.EMAIL_PASSWORD and config.EMAIL_RECIPIENT:
        smtp = smtplib.SMTP(config.EMAIL_HOSTNAME, 587)
        smtp.starttls()
        headers = (
            f'From: {config.EMAIL_USERNAME}\n'
            f'To: {config.EMAIL_RECIPIENT}\n'
            'Subject: jeddie.wedding notice\n\n'
        )
        smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
        smtp.sendmail(config.EMAIL_USERNAME, config.EMAIL_RECIPIENT, headers + message)
        smtp.quit()
