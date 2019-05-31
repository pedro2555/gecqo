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


Module containing a wrapper around the smtplib.

"""
import smtplib
from email.message import EmailMessage as Message

class SMTP(object):
    """Wrapper context manager class for the smtplib SMTP mailer.

    """
    def __init__(self, *, hostname, port, username, password, ssl=False, tls=False):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._ssl = ssl
        self._tls = tls

    def connect(self):
        """Opens a connection to the server.
        """
        if self._ssl:
            self._conn = smtplib.SMTP_SSL(self._hostname, self._port)
        else:
            self._conn = smtplib.SMTP(self._hostname, self._port)
        if self._tls:
            self._conn.starttls()
        self._conn.login(self._username, self._password)

    def close(self):
        """Closes a connection to the server.
        """
        self._conn.close()

    def send_message(self, message):
        """Send a given EmailMessage

        Args:
            message (EmailMessage): the message to be sent.
        """
        self._conn.send_message(message)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.close()
