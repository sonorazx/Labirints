import viz
<<<<<<< HEAD
import vizact
import vizmat
import math
import os
import time
import vizcam

viz.go()
=======
import vizcam
import vizact

viz.go()

>>>>>>> 8198995874ae8af0c7012ea501ad4dcdd9e2671b
viz.clearcolor(viz.SKYBLUE)
viz.addDirectionalLight().setEuler(45,-30,0)

<<<<<<< HEAD
PLAYER_HEIGHT = 5 
MOVE_SPEED = 0.1
CAM_DISTANCE = 15
TARGET_RADIUS = 1.5
LEVEL_TIME = 30

levels = [
    r'C:\Users\user\OneDrive\Dokumenti\Labirints\Labirints\labirint1.fbx',
    r'C:\Users\user\OneDrive\Dokumenti\Labirints\Labirints\level2.fbx'
]

cat_files = [
    r'C:\Users\user\OneDrive\Dokumenti\Labirints\Labirints\cat.fbx',
    r'C:\Users\user\OneDrive\Dokumenti\Labirints\Labirints\cat2.fbx'
]
current_level = 0
level_timer = LEVEL_TIME

info = viz.addText("", parent=viz.SCREEN)
info.setPosition([0.33,0.95,0])
info.fontSize(24)

timer_text = viz.addText("", parent=viz.SCREEN)
timer_text.setPosition([0.8,0.95,0])
timer_text.fontSize(24)

player_group = viz.addGroup()
player_group.setPosition([0,0,0])
player_model = viz.addChild(
    r'C:\Users\user\OneDrive\Dokumenti\Labirints\Labirints\cilvecins.fbx',
    parent=player_group
)
player_model.setScale([30,30,30])
player_model.collideMesh()

keys = {'w':False,'a':False,'s':False,'d':False}

def onKeyDown(k):
    if k in keys:
        keys[k] = True
def onKeyUp(k):
    if k in keys:
        keys[k] = False

viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.KEYUP_EVENT, onKeyUp)
viz.MainView.collision( viz.ON )

def move_player():
    pos = list(player_group.getPosition())
    yaw = player_group.getEuler()[0]

    forward = [math.sin(math.radians(yaw)), 0, math.cos(math.radians(yaw))]
    right = [-forward[2], 0, forward[0]]

    move = [0,0,0]

    if keys['w']:
        move[0] += forward[0]
        move[2] += forward[2]
    if keys['s']:
        move[0] -= forward[0]
        move[2] -= forward[2]
    if keys['a']:
        move[0] += right[0]
        move[2] += right[2]
    if keys['d']:
        move[0] -= right[0]
        move[2] -= right[2]

    pos[0] += move[0] * MOVE_SPEED * viz.getFrameTime()
    pos[2] += move[2] * MOVE_SPEED * viz.getFrameTime()
    player_group.setPosition(pos)

    cam_x = pos[0] - forward[0] * CAM_DISTANCE
    cam_z = pos[2] - forward[2] * CAM_DISTANCE
    viz.MainView.setPosition([cam_x, PLAYER_HEIGHT, cam_z])
    viz.MainView.lookAt([pos[0], PLAYER_HEIGHT, pos[2]])

maze = None
cat = None
current_level = 0
current_game_active = True
start_time = None

def load_level(level_index):
    global maze, cat, start_time, current_game_active

    current_game_active = True
    start_time = time.time()

    player_group.setPosition([0,0,0])

    if maze is not None:
        maze.remove()
    if cat is not None:
        cat.remove()


    info.message(f"Līmenis {level_index+1}! Atrodi kaķi!")
    ground = viz.addChild('ground.osgb')
    ground.setScale([40,1,40])
    ground.collideMesh()

    maze = viz.addChild(levels[level_index])
    maze.setScale([1,1,1])
    maze.setPosition([0,0,0])
    maze.collideMesh()

    if os.path.exists(cat_files[level_index]):
        cat = viz.addChild(cat_files[level_index])
        cat.setScale([30,30,30])
    else:
        import vizshape
        cat = vizshape.addSphere(radius=0.25)
        cat.color(viz.YELLOW)
    cat.setPosition([8,0,8])


def update():
    global current_level, current_game_active
    
    if not current_game_active:
        return 

    move_player()

    elapsed = time.time() - start_time
    remaining = LEVEL_TIME - elapsed
    timer_text.message(f"Laiks: {int(remaining)} s")

    if remaining <= 0:
        info.message("Laiks beidzies! Spēle beigusies!")
        viz.quit()
        return

    if cat is not None:
        distance = vizmat.Distance(player_group.getPosition(), cat.getPosition())
        if distance < TARGET_RADIUS:
            info.message(f"Kaķis atrasts! Līmenis {current_level+1} pabeigts!")
            current_game_active = False
            current_level += 1
            if current_level >= len(levels):
                info.message("Apsveicam! Spēle pabeigta!")
                viz.quit()
            else:
                vizact.ontimer2(1,0, lambda: load_level(current_level))


vizact.ontimer(0, update)
load_level(current_level)
=======
ground = viz.add('ground.osgb')
ground.setScale([50,1,50])
ground.color(viz.GREEN)


maze = viz.add('labirint1.obj')
maze.setPosition([0,0,0])
maze.setScale([1,1,1])
maze.collideMesh()
maze.disable(viz.CULL_FACE)

exitObj = viz.add('cat.obj')
exitObj.setPosition([10,0,10])
exitObj.setScale([5,5,5])
exitObj.collideMesh()

camera = vizcam.KeyboardCamera()
viz.MainView.setParent(camera)
viz.MainView.setPosition([0,1.8,-5])

playerCollider = viz.addChild(viz.COLLISION_CAPSULE, scale=[0.3,1.8,0.3])
playerCollider.visible(viz.OFF)
playerCollider.collideMesh()
playerCollider.setParent(camera)
playerCollider.setPosition([0,0,0])

def zoomCamera(e):
    zoomSpeed = 0.5
    x,y,z = camera.getPosition()
    if e.button == viz.MOUSE_WHEEL_UP:
        camera.setPosition([x,y,z-zoomSpeed])
    elif e.button == viz.MOUSE_WHEEL_DOWN:
        camera.setPosition([x,y,z+zoomSpeed])

viz.callback(viz.MOUSEDOWN_EVENT, zoomCamera)

MOVE_SPEED = 5.0
ACCELERATION = 15.0
velocity = viz.Vector(0,0,0)
keys = {"w":False,"a":False,"s":False,"d":False}

def keyDown(key):
    key = key.lower()
    if key in keys: keys[key] = True

def keyUp(key):
    key = key.lower()
    if key in keys: keys[key] = False

viz.callback(viz.KEYDOWN_EVENT, keyDown)
viz.callback(viz.KEYUP_EVENT, keyUp)

def updateMovement():
    global velocity
    desired = viz.Vector(0,0,0)
    if keys["w"]: desired += camera.getForward()
    if keys["s"]: desired -= camera.getForward()
    if keys["a"]: desired -= camera.getRight()
    if keys["d"]: desired += camera.getRight()

    if desired.length() > 0.001:
        desired.normalize()
        desired *= MOVE_SPEED
    else:
        desired = viz.Vector(0,0,0)

    frame_time = viz.getFrameElapsed()
    velocity += (desired - velocity) * min(ACCELERATION*frame_time,1)

    oldPos = camera.getPosition()
    camera.setPosition(oldPos + velocity * frame_time)
    playerCollider.setPosition(camera.getPosition())

    if playerCollider.collide(maze):

        camera.setPosition(oldPos)
        playerCollider.setPosition(oldPos)

        move_x = viz.Vector(velocity[0]*frame_time,0,0)
        camera.setPosition(oldPos + move_x)
        playerCollider.setPosition(camera.getPosition())
        if playerCollider.collide(maze):
            camera.setPosition(oldPos)
            playerCollider.setPosition(oldPos)

            move_z = viz.Vector(0,0,velocity[2]*frame_time)
            camera.setPosition(oldPos + move_z)
            playerCollider.setPosition(camera.getPosition())
            if playerCollider.collide(maze):
                camera.setPosition(oldPos)
                playerCollider.setPosition(oldPos)

vizact.ontimer(0, updateMovement)

def checkExit():
    if playerCollider.collide(exitObj):
        viz.message("Level Complete!")

vizact.ontimer(0.05, checkExit)
>>>>>>> 8198995874ae8af0c7012ea501ad4dcdd9e2671b
