import poplib,email,os,datetime,time,pymysql
from email.header import decode_header,Header,make_header 
from email import parser
from ExcelDB import LoadDocument
user = '**********'
password = '**********'
server = '**********'
attachment_dir = "**********"
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
resp, lines, octets = server_.retr(numberOfMails)
msg_content = email.message_from_string( b'\r\n'.join(lines).decode('utf-8'))
conn = pymysql.connect('**********',port=**********,user='**********',passwd = '**********',db='**********')
Name = get_attachments(msg_content)
print(Name[0] + str(' ') + str(datetime.datetime.now()))
LoadDocument(Name[1],conn)
prevNumberOfMails = numberOfMails
if(Name[1]!='Empty mail'):
    os.remove(Name[1])

while True:
	print('C')
	server_ = poplib.POP3_SSL(server)
	server_.user(user)
	server_.pass_(password)
	resp, mails, octets = server_.list()
	numberOfMails = len(mails)
	for i in range((prevNumberOfMails) - (numberOfMails)):
		print('New mail')
		resp, lines, octets = server_.retr(numberOfMails-i)
		msg_content = email.message_from_string( b'\r\n'.join(lines).decode('utf-8'))
		conn = pymysql.connect('**********',port=**********,user='**********',passwd = '**********',db='**********')
		Name = get_attachments(msg_content)
		print(Name[0] + str(' ') + str(datetime.datetime.now()))
		LoadDocument(Name[1],conn)	
		if(Name[1]!='Empty mail'):
			os.remove(Name[1])
	time.sleep(300)
	prevNumberOfMails = numberOfMails
