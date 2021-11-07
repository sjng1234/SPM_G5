import os 
from flask_sqlalchemy import sqlalchemy
# for macbook (Adrian)
import pymysql as MySQLdb


SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 100, 'pool_recycle': 280}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# For Localhost Testing -Macbook
# SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/SPM"

# # for windows
# SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3306/SPM"

# To Test on Cloud SQL
# CLOUD_DB_USERNAME = os.environ.get('CLOUD_DB_USERNAME')
# CLOUD_DB_PASSWORD = os.environ.get('CLOUD_DB_PASSWORD')
# CLOUD_DB_HOST = os.environ.get('CLOUD_DB_HOST')
# CLOUD_DB_NAME = os.environ.get('CLOUD_DB_NAME')

# SQLALCHEMY_DATABASE_URI = sqlalchemy.engine.url.URL.create(
#     drivername = "mysql+pymysql",
#     username = CLOUD_DB_USERNAME,  
#     password = CLOUD_DB_PASSWORD,  # e.g. "my-database-password"
#     host = CLOUD_DB_HOST,  # e.g. "127.0.0.1"
#     database = CLOUD_DB_NAME,  # e.g. "my-database-name"
# )

# To Test on Cloud SQL
CLOUD_DB_USERNAME = os.environ.get('CLOUD_DB_USERNAME')
CLOUD_DB_PASSWORD = os.environ.get('CLOUD_DB_PASSWORD')
CLOUD_DB_HOST = os.environ.get('CLOUD_DB_HOST')
CLOUD_DB_NAME = os.environ.get('CLOUD_DB_NAME')

SQLALCHEMY_DATABASE_URI = sqlalchemy.engine.url.URL.create(
    drivername = "mysql+pymysql",
    username = CLOUD_DB_USERNAME,  
    password = CLOUD_DB_PASSWORD,  # e.g. "my-database-password"
    host = CLOUD_DB_HOST,  # e.g. "127.0.0.1"
    database = CLOUD_DB_NAME,  # e.g. "my-database-name"
)

