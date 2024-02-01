import remi.gui as gui
from remi import start, App
import random
import player_controls

class PongApp(App):
    def __init__(self, *args):
        super(PongApp, self).__init__(*args)
      
    def main(self):
        # Creating a container for the user to view/see
        container = gui.VBox(width=600, height=400, style={'position':'relative', 'overflow':'hidden'})

        # Creating paddles and ball
        self.paddle1 = gui.Label(width=10, height=60, style={'background-color': 'blue', 'position': 'absolute', 'left': '10px', 'top': '170px'})
        self.paddle2 = gui.Label(width=10, height=60, style={'background-color': 'red', 'position': 'absolute', 'right': '10px', 'top': '170px'})
        self.ball = gui.Label(width=10, height=10, style={'background-color': 'green', 'position': 'absolute', 'top': '195px', 'left': '295px'})

        # Adding paddle and ball to the main container
        container.append(self.paddle1)
        container.append(self.paddle2)
        container.append(self.ball)

        # TODO: Capture Keypresses 

        # Setup player controls
        self.player_controls = PlayerControls(self.paddle1, self.paddle2, 600)

        # TODO: Add game logic for ball movement and collision detection

        return container

    def on_key_down(self, widget, value, *args):
      # TODO: read key presses and allow player to move

      
start(PongGame, address='0.0.0.0', port=8081, start_browser=True)
