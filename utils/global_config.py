import os
from pathlib import Path

from environs import Env

ROOT_DIR = Path(os.getenv("ROOT_DIR", '')) or Path(__file__).parent.parent


CONFIG_PATH = Path(ROOT_DIR) / 'build/.env'
if CONFIG_PATH.exists():
    env = Env()
    env.read_env(str(CONFIG_PATH))


class GlobalConfig:
    mysql_database = os.getenv('MYSQL_DATABASE')
    mysql_db_address = os.getenv("MYSQL_DATABASE_ADDRESS")
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_root_password = os.getenv("MYSQL_ROOT_PASSWORD")
    django_secret_key = os.getenv("DJANGO_SECRET_KEY")
    debug = os.getenv("DEBUG")

    sqlalchemy_database_uri = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_db_address}/{mysql_database}'
    root_dir = ROOT_DIR
