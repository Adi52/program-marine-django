from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from .models import EntryData

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", seconds=3600)
def delete_book_after_day_if_no_email_confirm():
    for record in EntryData.objects.all():
        time_elapsed = datetime.now(timezone.utc) - record.date_created
        if time_elapsed > timedelta(days=1) and not record.email_confirm:
            record.delete()


register_events(scheduler)
