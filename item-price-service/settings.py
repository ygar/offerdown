HOST="offerupchallenge.cgtzqpsohu0g.us-east-1.rds.amazonaws.com"
PORT="5432"
USERNAME="offerupchallenge"
PASSWORD="ouchallenge"
DB_NAME="itemprices"

DB_CONNECTION_STRING="dbname="+DB_NAME+" host="+HOST+" user="+USERNAME+" port="+PORT+" password="+PASSWORD

LOCALHOST = '127.0.0.1'
CACHE_URL = LOCALHOST + ':6379'
CACHE_TIMEOUT_TIME = 3600