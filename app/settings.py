# import os

# SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CREDENTIALS')
SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3306/SPM_LMS"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 100, 'pool_recycle': 280}
