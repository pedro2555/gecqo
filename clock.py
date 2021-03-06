"""
gecqo

Copyright (C) 2019  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of gecqo.

gecqo is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

gecqo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gecqo.  If not, see <http://www.gnu.org/licenses/>.


Module used to schedule tasks.

"""
from apscheduler.schedulers.blocking import BlockingScheduler

from src import tasks
from src import celery

sched = scheduler = BlockingScheduler()

@sched.scheduled_job('cron', minute='*/30')
def metaralert():
    task = celery.task(tasks.metaralert)
    task.apply_async()
