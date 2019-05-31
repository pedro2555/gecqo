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


Module to alert me on temps for metars.

"""
import logging
import requests
import smtplib
from email.message import EmailMessage
from .. import celery, mail

@celery.task()
def negative_temp_metar():
    airports = ['LPPT', 'LPPR', 'LPFR', 'LPMA']
    alert = []

    def get_metar_with_negative_temp(airport):
        resp = requests.get('/'.join(['https://avwx.rest/api/metar', airport]))
        metar = resp.json()

        temp = int(metar['Temperature'].replace('M', '-'))
        dwpt = int(metar['Dewpoint'].replace('M', '-'))

        if (temp < 0 or dwpt < 0):
            logging.info(metar['raw'])

    for airport in airports:
        metar = get_metar_with_negative_temp(airport)
        if metar:
            alert.append(metar)

    if alert:
        msg = EmailMessage()
        alert_airports = ', '.join(alert)

        msg['Subject'] = f'{alert_airports} with negative temperature.'
        msg['From'] = 'gecqo@gmail.com'
        msg['To'] = 'prodrigues1990@gmail.com'

    with mail:
        mail.send_message(msg)