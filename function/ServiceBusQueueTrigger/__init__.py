import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    POSTGRES_URL = os.environ.get('POSTGRES_URL')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PW = os.environ.get('POSTGRES_PW')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    connection = psycopg2.connect(host=POSTGRES_URL, user = POSTGRES_USER, password=POSTGRES_PW, database = POSTGRES_DB)
    cursor = connection.cursor()
    
    try:
        # TODO: Get notification message and subject from database using the notification_id
        #  executes the given database operation (query or command). 
        cursor.execute('SELECT message, subject FROM notification where id = %s',str(notification_id))
        (massage, subject) = cursor.fetchone()

        # TODO: Get attendees email and name
        cursor.execute("SELECT first_name, last_name, email FROM attendee")
        attendees = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            email = attendee[2]
            first_name = attendee[0]
            body = "Hi {}, {}".format(first_name,massage)
            # send_email(email, subject, body)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        notification_completed_date = datetime.utcnow()
        notification_status = 'Notified {} attendees'.format(len(attendees))
        cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notification_status, notification_completed_date, notification_id))
        connection.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        connection.rollback()
    finally:
        # TODO: Close connection
        cursor.close()
        connection.close()

def send_email(email, subject, body):
    if os.environ.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email=os.environ.get('ADMIN_EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(os.environget('SENDGRID_API_KEY'))
        sg.send(message)