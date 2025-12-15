import viz
import vizfx
import vizcam
import vizact
import vizmat

viz.go

viz.clearcolor(viz.SKYBLUE)

ground = viz.addChild('ground.osgb')
ground.setScale([50,1,50])
ground.setPosition([0,0,0])
ground.color(viz.GREEN)

EXIT_MODEL_FILE = "cat.fbx"

LEVEL = {
    "maze": "labirint1.fbx",
    "start": [0,1.8,0],
    "exitPos": [10,0,10]
}

mazeModel = None
exitModel = None

player = viz.MainView
vizcam.MouseLook()
viz.mouse.setVisible(False)

MOVE_SPEED = 3.0
keys = {"w":False, "s":False, "a":False, "d":False}

playerCollider = viz.addChild(viz.COLLISION_CAPSULE, scale=[0.3,1.8,0.3]
playerCollider.visible(viz.OFF)
playerCollider.collideMesh()
playerCollider.enable(viz.COLLIDE_NOTIFY)
playerCollider.setParent(player)

def keyDown(key):
	if key in keys:
		keys[key] = True
viz.callback(viz.KEYDOWN_EVENT,keyDown)

def keyUp(key):
	if key in keys:
		keys[key] = False
viz.callback(viz.KEYUP_EVENT,keyUp)

def updateMovement():
	move = viz.Vector(0,0,0)
	
	if keys["w"]:
		move += player.getForward()
	if keys["s"]:
		move -= player.getForward()
	if keys["a"]:
		move -= player.getRight()
	if keys["d"]:
		move += player.getRight()
		
	if move.lenght() > 0.001:
		move.normalize()
		move += MOVE_SPEED * viz.getFrameElapsed()
		
		player.setPosition(player.getPosition() + move)
		
		if player.collide(mazeModel1):
			player.setPosition(player.getPosition() - move)
			
			move_x = viz.Vector(move[0],0,0)
			player.setPosition(player.getPosition() + move_x)
			if player.collide(mazeModel1):
				player.setPosition(player.getPosition() - move_x)
				
				move_z = viz.Vector(0,0,move[2])
				player.setPosition(player.getPosition() + move_z)
				if player.collide(mazeModel1):
					player.setPosition(player.getPosition() - move_z)
					
vizact.ontimer(0, updateMovement)