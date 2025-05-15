from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore

class SchedulerManager:
    def __init__(self):
        self.scheduler = BlockingScheduler(
            jobstores={'default': MemoryJobStore()},
            job_defaults={
                'misfire_grace_time': 60,
                'coalesce': True,
                'max_instances': 3
            },
            timezone='UTC'
        )

    def add_job(self, func, interval: int, url: str):
        trigger = IntervalTrigger(seconds=interval)
        self.scheduler.add_job(
            func,
            trigger=trigger,
            id=url,
            replace_existing=True,
            name=f"Check job for {url}"
        )

    def start(self):
        self.scheduler.start()
