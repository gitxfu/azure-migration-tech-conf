# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* |  Basic, 1 vCore(s), 5 GB   |    $25.8    |
| *Azure Service Bus*   |      Basic   |      $0.05        |
| *Azure App Service*  |     F1     |      $0.00        |
| *Azure Function App*  |     consumption     |      < $0.01        |
| *Storage Account*  |     general purpose v2    |       $0.00        |
| *Total*  |        |       ~$26.00        |

## Architecture Explanation
Tech Conf was a monilithic conference registration application running locally with a Postgres SQL database. For the migration project, I used Azure Postgres Database single server for the database migration. At the early phase, a basic plan would be enough. 

The front-end web app has been migrated to Azure App Service, which gets and sends data to the Azure Postgres Database. The Azure App Service is a good option because we can autoscale our resources depending on the demand from users. It is also easier to manage App Service than VM.

The notification module of the app has been refactored and migrated to Azure Service Bus and Function App. When admin users creates a notification, the app sends messages to the Azure Service Bus Queues. The message queue can help level the load by providing a place to buffer communications when the app experiences bursts of communications, such as sending notifications to thousands of conference attendees. Then the Azure Function App gets the message from the queue and sends e-mail notifications to all attendees via SendGrid and update the notification status in the Postgres SQL database. We can also easily move up to a higher tier of Azure Service Bus for high throughput and autoscaling senarios.

## Live url
https://tech-conf-app.azurewebsites.net/

## Screenshots
![](screenshots/2021-05-23-20-38-36.png)