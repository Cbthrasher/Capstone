import PySimpleGUIWeb as sg
import random

GAMEPLAY_SIZE = (700, 400)
BAT_SIZE = (20, 110)
STARTING_BALL_POSITION = (327, 200)
BALL_RADIUS = 12
BACKGROUND_COLOR = 'black'
BALL_COLOR = 'green1'
BALL_SPEED = 300
BAT_SPEED = 400

num_rounds = 10
current_view = 'menu'  # Possible values: 'menu', 'game'


class Bat:
    def __init__(self, graph: sg.Graph, colour, x, field_height):
        self.graph = graph
        self.field_height = field_height
        self.width = BAT_SIZE[0]
        self.height = BAT_SIZE[1]
        self.current_x = x
        self.current_y = self.field_height / 2 - self.height / 2
        self.id = graph.draw_rectangle(
            (self.current_x, self.current_y),
            (self.current_x + self.width, self.current_y + self.height),
            fill_color=colour
        )
        self.vy = 0

    def stop(self):
        self.vy = 0

    def up(self):
        self.vy = -BAT_SPEED

    def down(self):
        self.vy = BAT_SPEED

    def is_hit_by(self, pos):
        bat_p0 = (self.current_x, self.current_y)
        bat_p1 = (bat_p0[0] + self.width, bat_p0[1] + self.height)
        return bat_p0[0] <= pos[0] <= bat_p1[0] and bat_p0[1] <= pos[1] <= bat_p1[1]

    def update(self, delta: float):
        new_y = self.current_y + self.vy * delta
        if new_y <= 0:
            new_y = 0
            self.stop()
        if new_y + self.height >= self.field_height:
            new_y = self.field_height - self.height
            self.stop()
        self.current_y = new_y

        self.graph.relocate_figure(self.id, self.current_x, self.current_y)


class Ball:
    def __init__(self, graph: sg.Graph, bat_1: Bat, bat_2: Bat, colour):
        self.graph = graph              # type: sg.Graph
        self.bat_1 = bat_1
        self.bat_2 = bat_2
        self.id = self.graph.draw_circle(
            STARTING_BALL_POSITION, BALL_RADIUS, line_color=colour, fill_color=colour)
        self.current_x, self.current_y = STARTING_BALL_POSITION
        self.vx = random.choice([-BALL_SPEED, BALL_SPEED])
        self.vy = -BALL_SPEED

    def hit_left_bat(self):
        return self.bat_1.is_hit_by((self.current_x - BALL_RADIUS, self.current_y))

    def hit_right_bat(self):
        return self.bat_2.is_hit_by((self.current_x + BALL_RADIUS, self.current_y))

    def update(self, delta: float):
        self.current_x += self.vx * delta
        self.current_y += self.vy * delta
        if self.current_y <= BALL_RADIUS:            # see if hit top or bottom of play area. If so, reverse y direction
            self.vy = -self.vy
            self.current_y = BALL_RADIUS
        if self.current_y >= GAMEPLAY_SIZE[1] - BALL_RADIUS:
            self.vy = -self.vy
            self.current_y = GAMEPLAY_SIZE[1] - BALL_RADIUS
        if self.hit_left_bat():
            self.vx = abs(self.vx)
        if self.hit_right_bat():
            self.vx = -abs(self.vx)

        self.position_to_current()

    def position_to_current(self):
        self.graph.relocate_figure(self.id, self.current_x - BALL_RADIUS, self.current_y - BALL_RADIUS)

    def restart(self):
        self.current_x, self.current_y = STARTING_BALL_POSITION
        self.position_to_current()


class Scores:
    def __init__(self, graph: sg.Graph):
        self.player_1_score = 0
        self.player_2_score = 0
        self.score_1_element = None
        self.score_2_element = None
        self.graph = graph

        self.draw_player1_score()
        self.draw_player2_score()

    def draw_player1_score(self):
        if self.score_1_element:
            self.graph.delete_figure(self.score_1_element)
        self.score_1_element = self.graph.draw_text(
            str(self.player_1_score), (170, 50), font='Courier 40', color='white')

    def draw_player2_score(self):
        if self.score_2_element:
            self.graph.delete_figure(self.score_2_element)
        self.score_2_element = self.graph.draw_text(
            str(self.player_2_score), (550, 50), font='Courier 40', color='white')

    def win_loss_check(self):
        if self.player_1_score >= num_rounds:
            return 'Left player'
        if self.player_2_score >= num_rounds:
            return 'Right player'
        return None

    def increment_player_1(self):
        self.player_1_score += 1
        self.draw_player1_score()

    def increment_player_2(self):
        self.player_2_score += 1
        self.draw_player2_score()

    def reset(self):
        self.player_1_score = 0
        self.player_2_score = 0
        self.draw_player1_score()
        self.draw_player2_score()
