import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='xfh134XUFU!',
            database='cpl_registration_tasks'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def determine_type(email):
    """Determine the email type based on the domain."""
    if 'gmail.com' in email:
        return 'gmail'
    elif 'outlook.com' in email:
        return 'outlook'
    elif 'hotmail.com' in email:
        return 'hotmail'
    else:
        return 'other'

def insert_buy_email(email, password, recoveryemail, type, status='0'):
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

def process_txt_file(filename):
    """Process the TXT file and insert data into the database."""
    with open(filename, 'r') as file:
        for line in file:
            # Strip newline and extra spaces
            line = line.strip()
            # Split the line by '----'
            parts = line.split('----')
            
            if len(parts) == 2:
                # Format: email,password
                email, password = parts
                recoveryemail = ''  # Default value for missing recovery email
                type = determine_type(email)
                insert_buy_email(email, password, recoveryemail, type)
            elif len(parts) == 3:
                # Format: email,password,recoveryemail
                email, password, recoveryemail = parts
                type = determine_type(email)
                insert_buy_email(email, password, recoveryemail, type)
            else:
                print(f"Invalid line format: {line}")

# Example usage
process_txt_file('emails.txt')

