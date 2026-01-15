import configparser
import os

config_file = os.path.join(os.path.dirname(__file__), "database.ini")

config = configparser.ConfigParser()
config.read(config_file)

if 'mysql' not in config:
    raise Exception(f"Arquivo de configuração não encontrado ou sem seção [mysql]: {config_file}")

DB_CONFIG = {
    "host": config['mysql']['host'],
    "user": config['mysql']['user'],
    "password": config['mysql']['password'],
    "database": config['mysql']['database'],
    "port": int(config['mysql']['port'])
}