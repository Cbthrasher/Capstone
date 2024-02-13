import PySimpleGUIWeb as sg
import datetime
import keyboard
from pong_classes import BACKGROUND_COLOR, Bat, Ball, Scores, GAMEPLAY_SIZE, BAT_SIZE
from pong_functions import check_ball_exit, goto_menu, update_leaderboard

def pong():
    sleep_time = 10

    leaderboard_layout = [
        [sg.Text("Leaderboard", font="Courier 20", justification="center")],
        [sg.Listbox(values=[], size=(20, 20), key="-LEADERBOARD-", enable_events=True)]
    ]
    
    inner_layout = [[sg.Graph(GAMEPLAY_SIZE,
                        (0, GAMEPLAY_SIZE[1]),
                        (GAMEPLAY_SIZE[0], 0),
                        background_color=BACKGROUND_COLOR,
                        key='-GRAPH-')],
              [sg.Button('Back to Menu', key="-MENU-")]]

    main_menu_layout = [[sg.Text("Pong", font="Courier 40", justification="center", size=(10, 1))],
                        [sg.Text("", font="Courier 8")],
                        [sg.Text("-- Instructions --", font="Courier 16")],
                        [sg.Text("Left player controls: W and S", font="Courier 12")],
                        [sg.Text("Right player controls: I and K", font="Courier 12")],
                        [sg.Text("Quit to leave the game", font="Courier 12")],
                        [sg.Text("", font="Courier 8")],
                        [sg.Text("Winner is first to 10 points", font="Courier 12")],
                        [sg.Text("", font="Courier 8")],
                        [sg.Button("Start", key='-START-', font="Courier 24"),
                        sg.Button("Quit", key='-QUIT-', font="Courier 24")]]
    
    layout = [[sg.Column(main_menu_layout, key='-MAIN_MENU-', size=GAMEPLAY_SIZE),
           sg.Column(inner_layout, key='-GAME-'), sg.Column(leaderboard_layout, key='-LEADERBORD-')]]
    
    window = sg.Window('Pong', layout, finalize=True, use_default_focus=False, web_port=8080, web_debug=True, web_start_browser=True, return_key_down_events=True)
    
    graph_elem = window['-GRAPH-']  
    
    scores = Scores(graph_elem)
    bat_1 = Bat(graph_elem, 'green', 30, GAMEPLAY_SIZE[1])
    bat_2 = Bat(graph_elem, 'yellow', GAMEPLAY_SIZE[0] - 30 - BAT_SIZE[0], GAMEPLAY_SIZE[1])
    ball_1 = Ball(graph_elem, bat_1, bat_2, 'green1')

    start = datetime.datetime.now()
    last_post_read_time = start

    game_playing = False
    
    while True:
        pre_read_time = datetime.datetime.now()
        processing_time = (pre_read_time - last_post_read_time).total_seconds()
        time_to_sleep = sleep_time - int(processing_time*1000)
        time_to_sleep = max(time_to_sleep, 0)

        event, values = window.read(time_to_sleep)
        now = datetime.datetime.now()
        delta = (now-last_post_read_time).total_seconds()
        last_post_read_time = now
        if event in (sg.WIN_CLOSED, "-QUIT-"):
            break
        elif event == "-START-":
            scores.reset()
            ball_1.restart()
            window['-MAIN_MENU-'].Visible=False
            window['-GAME-'].Visible=True
            last_post_read_time = datetime.datetime.now()
            game_playing = True
        elif event == "-MENU-":
            game_playing = False
            goto_menu(window)
        elif game_playing:
            
            if keyboard.is_pressed("W"):
                bat_1.up()
                
            elif keyboard.is_pressed("S"):    
                bat_1.down()
                    
            elif keyboard.is_pressed("I"):    
                bat_2.up()
                
            elif keyboard.is_pressed("K"):    
                bat_2.down()
                
        if game_playing:
            ball_1.update(delta)
            bat_1.update(delta)
            bat_2.update(delta)

            check_ball_exit(ball_1, scores)

            winner = scores.win_loss_check()
            if winner is not None:
                winner_name = sg.popup_get_text('Game Over', f'{winner} won! Enter your name: ', no_titlebar=True)
                if winner_name:
                    leaderboard = update_leaderboard(winner_name)
                    window['-LEADERBOARD-'].update(values=leaderboard)
                game_playing = False
                goto_menu(window)

    window.close()


if __name__ == '__main__':
    pong()
