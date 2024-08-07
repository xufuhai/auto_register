import mysql.connector
from mysql.connector import Error
import random

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='xfh134XUFU!',
        database='cpl_registration_tasks'
    )
    return connection

def insert_registration_task(url, email, password, proxy_ip, user_agent, country, city, offer):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO registration_tasks (url, email, password, proxy_ip, user_agent, country, city, offer, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    values = (url, email, password, proxy_ip, user_agent, country, city, offer, '0')
    cursor.execute(query, values)
    conn.commit()

    # Update status in buy_email
    query_update = '''
        UPDATE buy_email
        SET status = %s
        WHERE email = %s
    '''
    values_update = ('1', email)
    cursor.execute(query_update, values_update)
    conn.commit()
    print("Record updated in buy_email successfully")

    cursor.close()
    conn.close()

def insert_buy_email(email, password, recoveryemail, type, status):
    """Insert data into the buy_email table."""
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        query = '''
            INSERT INTO buy_email (email, password, recoveryemail, type, status)
            VALUES (%s, %s, %s, %s, %s)
        '''
        values = (email, password, recoveryemail, type, status)
        cursor.execute(query, values)
        conn.commit()
        print("Data inserted successfully into buy_email")
    except Error as e:
        print(f"Error while inserting data into MySQL: {e}")
    finally:
        cursor.close()
        conn.close()


def get_random_email_with_status_zero():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT email FROM buy_email WHERE status = %s"
        cursor.execute(query, ('0',))
        emails = cursor.fetchall()

        if not emails:
            print("No emails with status 0 found.")
            return None

        random_email = random.choice(emails)[0]
        return random_email

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def get_email_passwd_with_email(email):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT password FROM buy_email WHERE email = %s"
        cursor.execute(query, (email,))
        emails = cursor.fetchall()

        if not emails:
            print("No emails with status 0 found.")
            return None
        email_password = random.choice(emails)[0]
        return email_password

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def get_email_passwd_with_recoveryemail(email):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT recoveryemail FROM buy_email WHERE email = %s"
        cursor.execute(query, (email,))
        emails = cursor.fetchall()

        if not emails:
            print("No emails with status 0 found.")
            return None
        email_recoveryemail = random.choice(emails)[0]
        return email_recoveryemail

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
