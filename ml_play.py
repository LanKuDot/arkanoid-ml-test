import pickle
from sklearn.ensemble import RandomForestRegressor
import os.path

class MLPlay:
    def __init__(self):
        filename = 'ian.sav'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.ballx = 102.5
        self.bally = 102.5
        self.ball_served = False

    def update(self, scene_info):
        """
        Decide the command according to the received scene information
        """
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        ballspeedx = scene_info["ball"][0] + 2.5 - self.ballx
        ballspeedy = scene_info["ball"][1] + 2.5 - self.bally
        self.ballx = scene_info["ball"][0] + 2.5
        self.bally = scene_info["ball"][1] + 2.5
        platformx = scene_info["platform"][0] + 20
        predictx = self.model.predict(
            [[ballspeedx, ballspeedy, self.ballx, self.bally]])[0]

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        if predictx - 3 > platformx:
            return "MOVE_RIGHT"
        if predictx + 3 < platformx:
            return "MOVE_LEFT"

    def reset(self):
        self.ball_served = False
