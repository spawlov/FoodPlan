# import logging
from datetime import timedelta

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from loguru import logger

from food_app.models import Subscription, Plan


def checking_active_subscription():
    subscriptions = Subscription.objects.filter(is_active=True)
    for subscription in subscriptions:
        if subscription.end <= timezone.now():
            subscription.is_active = False
            subscription.save()
            logger.info(f'Subscription: {subscription.pk} marked is not active!')


def checking_payed_subscription():
    subscriptions = Subscription.objects.filter(is_active=False, paid=False)
    for subscription in subscriptions:
        paid_period = subscription.start + timedelta(minutes=30)
        if paid_period < timezone.now():
            plan = Plan.objects.get(pk=subscription.plan_id)
            subscription_pk = subscription.pk
            plan_pk = plan.pk
            subscription.delete()
            print(f'Subscription #{subscription_pk} deleted!')
            plan.delete()
            logger.info(f'Plan #{plan_pk} deleted!')


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
    logger.info('Old jobs deleted!')


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(
            timezone=pytz.timezone(settings.TIME_ZONE)
        )
        scheduler.add_jobstore(
            DjangoJobStore(),
            'default',
            replace_existing=True,
        )
        scheduler.add_job(
            checking_payed_subscription,
            trigger=CronTrigger(second='00'),
            id="checking_payed_subscription",
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job "checking_payed_description".')

        scheduler.add_job(
            checking_active_subscription,
            trigger=CronTrigger(hour='00', minute='00'),
            id="checking_active_subscription",
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job "checking_active_description".')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added weekly job: "delete_old_job_executions".')

        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')
