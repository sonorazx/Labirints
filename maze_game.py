import viz
import vizcam
import vizact

viz.go()

viz.clearcolor(viz.SKYBLUE)
viz.addDirectionalLight().setEuler(45,-30,0)

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
