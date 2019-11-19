import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    comm.ml_ready()

    while True:
        scene_info = comm.get_scene_info()
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            comm.ml_ready()
            continue

        if scene_info.platform[0] - scene_info.ball[0] > -15:
            command = PlatformAction.MOVE_LEFT
        elif scene_info.platform[0] - scene_info.ball[0] < -35:
            command = PlatformAction.MOVE_RIGHT
        else:
            command = PlatformAction.NONE

        comm.send_instruction(scene_info.frame, command)
