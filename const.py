#constant
# ln -s /Applications/MAMP/tmp/mysql/mysql.sock /tmp/mysql.sock
HOSTNAME = 'localhost'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'otcmarket'
PORT = '27017'
# USERNAME = 'user_mojo'
# PASSWORD = '46%Q4nmb'
# DATABASE = 'admin_mojo'
# PORT = 3306
#collection names
DB_COLLECTION_CONTACT = 'Contact'

# 1 10 * * * python /Users/sangdt/Documents/Source/Python/otcmarket_python/sync_contact.py
# 1 16 * * * python /Users/sangdt/Documents/Source/Python/otcmarket_python/sync_contact.py

# echo "Hello World" | mail -s "Test email" dtsang012@yahoo.com

SUBJECT_FREFIX = '"OTC Market app: A new message from "'
RECEIVER_MAIL = 'dtsang012@yahoo.com'