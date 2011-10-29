from eventlet import patcher
from eventlet.green import socket
from eventlet.green import ssl
from eventlet.green import time

smtplib = patcher.inject('smtplib',
    globals(),
    ('socket', socket),
    ('ssl', ssl),
    ('time', time))

del patcher


class MailSender(object):
    """
        Smtp server wrapper
    """

    def __init__(self, host, port=25, user=None, password=None, enable_ssl=True):

        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.server = smtplib.SMTP(host, port)

        if enable_ssl:
            self.start_ssl()

    def start_ssl(self):
        """
            Starts the ssl session over the stmp protocol
        """

        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.user, self.password)

    def send(self, to_addresses, body, from_address=None, subject='Crawley Mailer'):
        """
            Sends an email to a list of to_addresses
        """

        if from_address is None and self.user is not None:
            from_address = self.user
        else:
            from_address = self.host

        msg = "\r\n".join(["From: %s" % from_address, "To: %s" % ",".join(to_addresses), "Subject: %s" % subject, "", body])

        self.server.sendmail(from_address, to_addresses, msg)

    def __del__(self):
        """
            Ends the server
        """

        self.server.quit()
