import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="techconfdb-singleserver.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="admin01@techconfdb-singleserver" #TODO: Update value
    POSTGRES_PW="P@ssword1234"   #TODO: Update value
    POSTGRES_DB="postgres"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://my-notification-queue.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qEcgwoNG9H9xQs49lx7lC/YBXF+X9byg6ITJ3V4qQ+I=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notification-queue'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False