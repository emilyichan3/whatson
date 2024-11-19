import os

# For a production app, you should use a secret key set in the environment
# The recommended way to generate a 64char secret key is to run:
# python -c 'import secrets; print(secrets.token_hex())'
SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')

# When deploying, set in the environment to the PostgreSQL URL
SQLALCHEMY_DATABASE_URI = os.getenv('LOCAL_DATABASE_URL', 'sqlite:///db.sqlite3')
# SQLALCHEMY_DATABASE_   URI = "post   gresql://ucdtestdatabase_user:LILVLDIhZcSObq1Yd5ZK8sBKUl2pqRYN@dpg-cs8mj088fa8c73cf2cp0-a.oregon-postgres.render.com/ucdtestdatabase"
