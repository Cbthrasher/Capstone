from pong_classes import Ball, Scores, GAMEPLAY_SIZE
import mysql.connector
from mysql.connector import Error
import boto3

def check_ball_exit(ball: Ball, scores: Scores):
    if ball.current_x <= 0:
        scores.increment_player_2()
        ball.restart()
    if ball.current_x >= GAMEPLAY_SIZE[0]:
        scores.increment_player_1()
        ball.restart()

def get_db_endpoint(stack_name):
    client = boto3.client('cloudformation')
    response = client.describe_stacks(StackName=stack_name)
    outputs = response['Stacks'][0]['Outputs']
    for output in outputs:
        if output['OutputKey'] == 'DBEndpoint':
            return output['OutputValue']
    raise ValueError("DBEndpoint not found in stack outputs")

stack_name = 'pongcapstack'

try:
    db_endpoint = get_db_endpoint(stack_name)
    print("Database Endpoint:", db_endpoint)
except Exception as e:
    print(f"Error: {e}")


def goto_menu(window):
    window['-MAIN_MENU-'].Visible=True
    window['-GAME-'].Visible=False
    
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=db_endpoint,  
            database='stackdb',
            user='adminadmin',
            password='passpass'
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        
def create_leaderboard_table():
    connectiond = create_db_connection()
    
    if connectiond and connectiond.is_connected():
            cursor = connectiond.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                score INT NOT NULL
            );
            """
            cursor.execute(create_table_query)
            connectiond.commit()
            print("Leaderboard table is created successfully")

def update_leaderboard(winner_name):
    
    create_leaderboard_table()
    
    connection = create_db_connection()
    if connection and connection.is_connected():
        cursor = connection.cursor()
        
        # Check if the winner is already in the leaderboard
        cursor.execute("SELECT score FROM leaderboard WHERE name = %s", (winner_name,))
        record = cursor.fetchone()

        if record:
            # Increment score if winner exists
            new_score = record[0] + 1
            cursor.execute("UPDATE leaderboard SET score = %s WHERE name = %s", (new_score, winner_name))
        else:
            # Add new winner to the leaderboard
            cursor.execute("INSERT INTO leaderboard (name, score) VALUES (%s, 1)", (winner_name,))
        
        connection.commit()

        # Fetch updated leaderboard
        cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC")
        leaderboard_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return [f"{name}: {score}" for name, name, score in leaderboard_data]
    else:
        return []
