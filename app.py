import gradio as gr
import sqlite3
from datetime import datetime

database_path = "database.db"

## Database functions
def open_connection():
    ''' Connect to database '''
    connection = None
    try:
        connection = sqlite3.connect(database_path)
        print("Connection to DB successful.")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred.")
    return connection


def close_connection(conn):
    ''' Close database connection '''
    try:
        conn.close()
        print("Connection to DB closed.")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred.")


def setup_database():
    ''' Setup database, if not already '''
    connection = open_connection()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS diary (date DATE, entry TEXT)")
    connection.commit()
    close_connection(connection)


def update_database(new_entry, date_to_update, connection=None):
    ''' Update entry in database '''
    if connection is None:
        connection = open_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE diary SET entry = ? WHERE date = ?", (new_entry, date_to_update,))
    connection.commit()
    close_connection(connection)


def insert_into_database(new_entry, date_to_add, connection=None):
    ''' Insert entry in database '''
    if connection is None:
        connection = open_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO diary (date, entry) VALUES (?, ?)", (date_to_add, new_entry,))
    connection.commit()
    close_connection(connection)


def get_entry(date_to_check, connection=None, close_conn=False):
    ''' Get an entry on a date '''
    if connection is None:
        connection = open_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT entry FROM diary WHERE date = ?", (date_to_check,))
    data = cursor.fetchall()
    if close_conn:
        close_connection(connection)
    return data


def does_entry_exist(date_to_check, connection=None):
    ''' Checks if entry for date already exists '''
    data = get_entry(date_to_check, connection)
    if data == []: return False
    else: return True


## Helpers
def todays_date():
    ''' Returns todays date in YYYY-MM-DD format '''
    return str(datetime.today().strftime('%Y-%m-%d'))

def yesterdays_date():
    ''' Returns yesterdays date in YYYY-MM-DD format'''
    pass


## Functionality
def submit_today(input_text):
    connection = open_connection()
    today = todays_date()
    entry_exists = does_entry_exist(today, connection)

    if entry_exists:
        update_database(new_entry=input_text, date_to_update=today, connection=connection)
        print("Entry updated.")
        return "Entry updated.", input_text
    else: 
        insert_into_database(new_entry=input_text, date_to_add=today, connection=connection)
        print("Entry saved.")
        return "Entry saved.", input_text


## UI Layout
with gr.Blocks() as home:
    # Yesterday tab layout
    with gr.Tab("Yesterday"):
        gr.Markdown("Yesterday")

    # Today tab layout
    with gr.Tab("Today"):
        gr.Markdown("What did you do today?")
        todays_entry = get_entry(date_to_check=todays_date(), close_conn=True)[0][0]

        input_text = gr.Textbox(todays_entry, label="Today I...")
        updatebtn = gr.Button("Save")
        display_output = gr.Markdown()

        # Submit/Update entry
        updatebtn.click(submit_today, inputs=input_text, outputs=[display_output, input_text])

    # Select date tab layout
    with gr.Tab("Select Date"):
        gr.Markdown("Select Date")

    # Buttons along bottom
    with gr.Row(equal_height=True):
        exportbtn = gr.Button("Export current entry")
        multiplebtn = gr.Button("Export multiple dates") # TODO: perhaps own tab/advanced section?
        searchbtn = gr.Button("AI search") # TODO: perhaps own tab/advanced section?

if __name__ == "__main__":
    setup_database()
    # Launch app
    home.launch()
