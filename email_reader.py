import imaplib
import email
import MySQLdb

mydb = MySQLdb.connect(host='localhost', user='root', passwd='db_password', db='db_name')
cursor = mydb.cursor()
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('your gmail_id', 'password')
mail.list()

# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.
result, data = mail.uid('search', None, "ALL")
i = len(data[0].split()) # data[0] is a space separate string
for x in range(i):
	latest_email_uid = data[0].split()[x] # unique ids wrt label selected
	result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
	 
	# fetch the email body (RFC822) for the given ID
	raw_email = email_data[0][1]
	raw_email_string = raw_email.decode('utf-8')

	# converts byte literal to string removing b''
	email_message = email.message_from_string(raw_email_string)
	x = email_message['From']
	y = x.partition('<')[-1].rpartition('>')[0]
	z = email_message['Subject']
	# print z
	for part in email_message.walk():
	    if part.get_content_type() == "text/plain":
	    	body = part.get_payload(decode=True)
	    	cursor.execute("INSERT IGNORE INTO table_name(email_id,subject, description) VALUES(%s,%s,%s)", (y,z,body))
	    	print '*****'
	    	mydb.commit()
cursor.close()
print "Your email has been saved to database"
    
