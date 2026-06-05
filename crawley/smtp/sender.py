"""
    SMTP mail sender.

    A thin wrapper around the standard library :mod:`smtplib` used by
    crawley to send notification emails. Messages are built with
    :class:`email.message.EmailMessage` and delivered through
    :meth:`smtplib.SMTP.send_message`.
"""

import smtplib
from email.message import EmailMessage


class MailSender(object):
    """
        Smtp server wrapper.
    """

    def __init__(self, host, port=25, user=None, password=None, enable_ssl=True):
        """
            Opens a connection to the SMTP server and optionally starts a
            TLS/SSL session.
        """

        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.server = smtplib.SMTP(host, port)

        if enable_ssl:
            self.start_ssl()

    def start_ssl(self):
        """
            Starts the ssl session over the smtp protocol and authenticates
            the configured user.
        """

        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.user, self.password)

    def send(self, to_addresses, body, from_address=None, subject='Crawley Mailer'):
        """
            Sends an email to a list of ``to_addresses``.
        """

        if from_address is None and self.user is not None:
            from_address = self.user
        elif from_address is None:
            from_address = self.host

        msg = EmailMessage()
        msg['From'] = from_address
        msg['To'] = ", ".join(to_addresses)
        msg['Subject'] = subject
        msg.set_content(body)

        self.server.send_message(msg)

    def __del__(self):
        """
            Ends the server, ignoring any error raised while closing it.
        """

        try:
            self.server.quit()
        except Exception:
            pass
