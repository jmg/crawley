import smtplib

class MailSender(object):
    """
        Smtplib wrapper
    """
    
    def __init__(self, host, port=25, user=None, password=None):

        self.host = host
        self.port = port
        self.user = user        
        
        self.server = smtplib.SMTP(host, port)
        
        if user is not None and password is not None:
            self.start_ssl(user, password)
    
    def start_ssl(self, user, password):
        """
            Starts the ssl session over the stmp protocol
        """
        
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(user, password)
    
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
