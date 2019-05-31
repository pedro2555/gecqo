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


Main project package.

"""
import os
from dotenv import load_dotenv
from celery import Celery
from .mail import SMTP

# loads a file name .env into environment
load_dotenv()

celery = Celery(
    __name__,
    broker=os.getenv('REDIS_URL', 'redis://'))
celery.config_from_object('celeryconfig')

mail = SMTP(
    hostname=os.getenv('MAIL_HOST'),
    port=    os.getenv('MAIL_PORT'),
    username=os.getenv('MAIL_USER'),
    password=os.getenv('MAIL_PASS'),
    ssl=     os.getenv('MAIL_SSL', False),
    tls=     os.getenv('MAIL_TLS', False))
