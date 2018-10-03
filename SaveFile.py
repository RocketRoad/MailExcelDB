import poplib,email,os,datetime,time,pymysql
from email.header import decode_header,Header,make_header 
from email import parser
from ExcelDB import LoadDocument
user = '********'
password = '********'
server = '********'
attachment_dir = "********"
def get_attachments(msg):
    fileName = 'Empty mail'
    filePath = 'Empty mail'
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        fileName =  str(make_header(decode_header(fileName)))
        if bool(fileName):
            filePath = os.path.join(attachment_dir, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))
    return [fileName,filePath]
server_ = poplib.POP3(server)
server_.user(user)
server_.pass_(password)
resp, mails, octets = server_.list()
numberOfMails = len(mails)
prevNumberOfMails = numberOfMails
print('New mail')
NumberOfFile = 0
resp, lines, octets = server_.retr(numberOfMails-NumberOfFile)
msg_content = email.message_from_string( b'\r\n'.join(lines).decode('utf-8'))
conn = pymysql.connect('********',port=46177,user='********',passwd = '********',db='********')
Name = get_attachments(msg_content)
