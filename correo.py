from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from email.mime.application import MIMEApplication
import smtplib
from parameters.credentials import CREDENTIALS

from_address = CREDENTIALS['from_address']
to_address = CREDENTIALS['to_address']

def test_conn_open(conn):
    try:
        status = conn.noop()[0]
    except:  # smtplib.SMTPServerDisconnected
        status = -1
    return True if status == 250 else False


def send_correo(path):
    message = MIMEMultipart()
    message['Subject'] = "Reporte"
    text = MIMEText("Este es un reporte del Invernadero")
    message.attach(text)
    directory = path
    with open(directory, 'rb') as opened: openedfile = opened.read()
    attachedfile = MIMEApplication(openedfile, _subtype = "pdf")
    attachedfile.add_header('content-disposition', 'attachment', filename = path)
    message.attach(attachedfile)
    print('Conectando...')
    smtp = smtplib.SMTP("smtp.live.com", 587)
    i = 0
    while not test_conn_open(smtp):
        print('Conectando')
        smtp = smtplib.SMTP("smtp.live.com", 587)
        i+=1
        if i>5:
            raise SystemExit('Imposible conectarse')      
    smtp.starttls()
    smtp.login(CREDENTIALS['from_address'],CREDENTIALS['password'])
    print('Enviando ...')
    smtp.sendmail(from_address, to_address, message.as_string())
    smtp.quit()