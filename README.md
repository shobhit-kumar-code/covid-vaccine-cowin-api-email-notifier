# COWIN Vaccine Slot Availability Email Notifier

This is a script to get email notifications with available slot details for Covid-19 Vaccination Centers from CoWIN API in India and shows a Windows notification for the same.  This will NOT book slots.

## Usage

Set the required district ids and run the script using ``python script.py``
**To find you district id:**
 1. Open the link in your browser to get your state id. https://cdn-api.co-vin.in/api/v2/admin/location/states
 2. Using the state id obtained, open this link in your browser. https://cdn-api.co-vin.in/api/v2/admin/location/districts/STATE_ID
 
 Set the environment variables with the required values. ``FROM_EMAIL SENDGRID_API_KEY TO_EMAIL1``. This can be done in Windows by entering the following in cmd: ``setx ENV_VARIABLE_NAME value_of_env_variable``

## Requirements

- The required libraries can be installed using, ``pip install -r requirements.txt`` 
- For email notifications, a send grid free trial account can be set up. It gives 100 email calls a day
