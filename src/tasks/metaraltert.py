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
from email.message import EmailMessage
import requests
from .. import celery, mail

@celery.task()
def metaralert():
    """Dispatches an email every time a metar with negative temperature or dew point is found.
    """
    airports = ['LPPT', 'LPPR', 'LPFR', 'LPMA']
    alerts = []

    def get_metar_with_negative_temp(airport):
        resp = requests.get('/'.join(['https://avwx.rest/api/metar', airport]))
        metar = resp.json()

        temp = metar['temperature']['value']
        dwpt = metar['dewpoint']['value']

        logging.info(metar['raw'])

        if (temp < 0 or dwpt < 0):
            return metar

        return None

    for airport in airports:
        metar = get_metar_with_negative_temp(airport)
        if metar:
            alerts.append(metar)

    if alerts:
        msg = EmailMessage()
        alert_airports = ', '.join([alert['station'] for alert in alerts])

        body = '\r\n'.join([alert['raw'] for alert in alerts])
        msg['Subject'] = f'{alert_airports} with negative temperature.'
        msg.set_content(body)
        msg['From'] = 'gecqo.lizard@gmail.com'
        msg['To'] = 'prodrigues1990@gmail.com'

        with mail:
            mail.send_message(msg)
