import os

# For a production app, you should use a secret key set in the environment
# The recommended way to generate a 64char secret key is to run:
# python -c 'import secrets; print(secrets.token_hex())'
SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')

# When deploying, set in the environment to the PostgreSQL URL
# SQLALCHEMY_DATABASE_URI = os.getenv('LOCAL_DATABASE_URL', 'sqlite:///db.sqlite3')
SQLALCHEMY_DATABASE_URI = "postgresql://whatson_database_user:MvygQ3Xniwu9Cd7UDLJnIH7I4B0grIr8@dpg-ct2ehp56l47c73ban60g-a.oregon-postgres.render.com/whatson_database"
