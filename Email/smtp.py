import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.mime import *
from email.utils import parseaddr, formataddr


def _send_text(sender_addr, sender_passwd, smtp_server, content, rec_list, title):
    msg = MIMEText(content, 'html', 'utf-8')
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(sender_addr, sender_passwd)
    for i in range(len(rec_list)):
        msg = _msg_format(msg, sender_addr, rec_list[i], title)
        server.sendmail(sender_addr, rec_list, msg.as_string())
    server.quit()
    return


def _format_addr(str):
    name, addr = parseaddr(str)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def _msg_format(msg, sender_addr, rec_addr, title):
    msg['From'] = _format_addr('<%s>' % sender_addr)
    msg['To'] = _format_addr('<%s>' % rec_addr)
    msg['Subject'] = Header(title, 'utf-8').encode()
    return msg


if __name__ == "__main__":
    from_addr = input('From: ')
    password = input('Passwd: ')
    smtp_server = input('SMTP server: ')
    to_addr = input('To: ')
    title = input('Title: ')

    content = 'hello email' + '\n' + '<html><body><h1>Hello</h1>' + '<p>send by <a href="http://www.python.org">Python</a>...</p>' + '</body></html>'
    rec_list = []
    rec_list.append(to_addr)
    _send_text(from_addr, password, smtp_server, content, rec_list, title)
