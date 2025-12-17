import viz
import vizact
import vizmat
import math
import os
import time

viz.go()
viz.clearcolor(viz.SKYBLUE)

PLAYER_HEIGHT = 12
MOVE_SPEED = 0.4
CAM_DISTANCE = 15
PLAYER_OFFSET = 5
TARGET_RADIUS = 2
LEVEL_TIME = 30
MOUSE_SENSITIVITY = 0.2

levels = [
    r'C:\Labirints\Labirints\level1.fbx',
    r'C:\Labirints\Labirints\level2.fbx'
]

cat_files = [
    r'C:\Labirints\Labirints\cat.fbx',
    r'C:\Labirints\Labirints\cat2.fbx'
]

info = viz.addText('', parent=viz.SCREEN)
info.setPosition([0.33,0.95,0])
info.fontSize(24)

timer_text = viz.addText('', parent=viz.SCREEN)
timer_text.setPosition([0.8,0.95,0])
timer_text.fontSize(24)

player_group = viz.addGroup()

player_model = viz.addChild(
    r'C:\Labirints\Labirints\cilvecins.fbx',
    parent=player_group
)
player_model.setScale([30,30,30])

viz.MainView.collision(viz.ON)

keys = {'w':False,'a':False,'s':False,'d':False}
yaw = 0
pitch = 0
last_mouse_pos = None

def onKeyDown(k):
    if k in keys: keys[k] = True

def onKeyUp(k):
    if k in keys: keys[k] = False

viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.KEYUP_EVENT, onKeyUp)
viz.mouse.setVisible(False)
viz.mouse.setOverride(True)

def onMouseMove(e):
    global yaw, pitch
    yaw += e.dx * MOUSE_SENSITIVITY
    pitch -= e.dy * MOUSE_SENSITIVITY
    pitch = max(-89, min(89, pitch))

viz.callback(viz.MOUSE_MOVE_EVENT, onMouseMove)

def move_player():
    global yaw, pitch

    forward = [math.sin(math.radians(yaw)), 0, math.cos(math.radians(yaw))]
    right   = [-forward[2], 0, forward[0]]

    pos = list(viz.MainView.getPosition())

    if keys['w']:
        pos[0] += forward[0] * MOVE_SPEED
        pos[2] += forward[2] * MOVE_SPEED
    if keys['s']:
        pos[0] -= forward[0] * MOVE_SPEED
        pos[2] -= forward[2] * MOVE_SPEED
    if keys['a']:
        pos[0] += right[0] * MOVE_SPEED
        pos[2] += right[2] * MOVE_SPEED
    if keys['d']:
        pos[0] -= right[0] * MOVE_SPEED
        pos[2] -= right[2] * MOVE_SPEED

    pos[1] = PLAYER_HEIGHT
    viz.MainView.setPosition(pos)
    viz.MainView.setEuler([yaw, pitch, 0])

    model_x = pos[0] + forward[0] * PLAYER_OFFSET
    model_z = pos[2] + forward[2] * PLAYER_OFFSET
    player_group.setPosition([model_x, 0, model_z])
    player_group.setEuler([yaw, 0, 0])
    
maze = None
cat = None
ground = None
current_level = 0
start_time = 0
level_finished = False

def load_level(index):
    global maze, cat, ground, start_time, level_finished

    level_finished = False
    start_time = time.time()

    viz.MainView.setPosition([0, PLAYER_HEIGHT, -5])
    viz.MainView.setEuler([0,0,0])

    player_group.setPosition([0,0,PLAYER_OFFSET])

    if maze: maze.remove()
    if cat: cat.remove()
    if ground: ground.remove()

    info.message(f"Līmenis {index+1}! Atrodi kaķi!")

    ground = viz.addChild('ground.osgb')
    ground.setScale([40,1,40])
    ground.collideMesh()

    maze = viz.addChild(levels[index])
    maze.collideMesh()

    if os.path.exists(cat_files[index]):
        cat = viz.addChild(cat_files[index])
        cat.setScale([30,30,30])
    else:
        import vizshape
        cat = vizshape.addSphere(radius=0.5)

    cat.setPosition([40,1,40])

def update():
    global current_level, level_finished

    move_player()

    remaining = LEVEL_TIME - (time.time() - start_time)
    timer_text.message(f"Laiks: {int(remaining)} s")

    if remaining <= 0:
        info.message("Laiks beidzies! Spēle beigusies!")
        viz.quit()
        return

    if cat and not level_finished:
        d = vizmat.Distance(player_group.getPosition(), cat.getPosition())
        if d < TARGET_RADIUS:
            level_finished = True
            current_level += 1

            if current_level >= len(levels):
                info.message("Apsveicam! Spēle pabeigta!")
                viz.quit()
            else:
                info.message("Kaķis atrasts!")
                vizact.ontimer2(1,0, lambda: load_level(current_level))

vizact.ontimer(0, update)
load_level(0)
