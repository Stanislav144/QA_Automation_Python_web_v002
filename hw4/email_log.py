import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_log_via_email(email_from, email_to, password, file_name, report_file):
    msg = MIMEMultipart('alternative')
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = 'Результаты автотестов для тестового стенда gb'

    with open(file_name, 'rb') as f:
        part = MIMEApplication(f.read(), Name=basename(file_name))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file_name)
        msg.attach(part)

    body = f'Результат автотестирования тестового стенда GB https://test-stand.gb.ru'

    with open(report_file, 'r', encoding='utf-8') as f:
        report_text = f.read()

    body += report_text

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)  # 25
    server.login(email_from, password)
    text = msg.as_string()
    server.sendmail(email_from, email_to, text)
    server.quit()