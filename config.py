import os, ast
from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID_LIST = ast.literal_eval(os.getenv('ADMIN_ID_LIST'))
DB_NAME = os.getenv('DB_NAME')