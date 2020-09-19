#constant
# ln -s /Applications/MAMP/tmp/mysql/mysql.sock /tmp/mysql.sock
HOSTNAME = 'localhost'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'vndating'
PORT = '27017'
# USERNAME = 'user_mojo'
# PASSWORD = '46%Q4nmb'
# DATABASE = 'admin_mojo'
# PORT = 3306
#collection names
DB_COLLECTION_USER = 'user'

# 1 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopViews 0
# 8 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopViews 1
# 15 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopViews 2
# 21 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopViews 3
# 28 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopRegister 0
# 35 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopRegister 1
# 42 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopRegister 2
# 50 * * * * python /Users/sangdt/Documents/Source/Python/vndating_python/scrape_top_users.py TopRegister 3

# echo "Hello World" | mail -s "Test email" dtsang012@yahoo.com
