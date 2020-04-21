from mlgame.communication import ml as comm
import pickle
from sklearn.ensemble import RandomForestRegressor
import os.path

def ml_loop():
    filename = 'ian.sav'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    model = pickle.load(open(filepath, 'rb'))
    comm.ml_ready()
    scene_info = comm.recv_from_game()
    comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})

    ballspeedx = 0
    ballspeedy = 0
    ballx = 102.5
    bally = 102.5
    predictx = 100

    while True:
        scene_info = comm.recv_from_game()

        if scene_info["status"] == "GAME_OVER":
            scene_info = comm.recv_from_game()
            break
        elif scene_info["status"] == "GAME_PASS":
            scene_info = comm.recv_from_game()

        ballspeedx = scene_info["ball"][0] + 2.5 - ballx
        ballspeedy = scene_info["ball"][1] + 2.5 - bally
        ballx = scene_info["ball"][0] + 2.5
        bally = scene_info["ball"][1] + 2.5
        platformx = scene_info["platform"][0] + 20
        predictx = model.predict([[ballspeedx, ballspeedy, ballx, bally]])[0]

        if predictx - 3 > platformx:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
        elif predictx + 3 < platformx:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
