import sys, pygame, time
import userCode

##### renderer
tileTable = None
spriteTable = None
screen = None
mapToTiles = {
		'0':{
			'y':1,
			'x':0
		},
		'1':{
			'y':1,
			'x':1
		},
		'2':{
			'y':1,
			'x':2
		},
		'3':
		{
			'y':1,
			'x':3
		},
		'4':{
			'y':2,
			'x':0
		},
		'5':{
			'y':2,
			'x':1
		},
		'6':{
			'y':2,
			'x':2
		},
		'7':{
			'y':2,
			'x':3
		},
		'8':{
			'y':3,
			'x':0
		},
		'9':{
			'y':3,
			'x':1
		},
		'A':{
			'y':3,
			'x':2
		},
		'B':{
			'y':3,
			'x':3
		},
		'C':{
			'y':4,
			'x':0
		},
		'D':{
			'y':4,
			'x':1
		},
		'E':{
			'y':4,
			'x':2
		},
		'F':{
			'y':4,
			'x':3
		},
	}
def rendererInit():
	global screen
	pygame.init()
	screen = pygame.display.set_mode((160, 160))
	screen.fill((255, 255, 255))
	load_tile_table("tileset/robot.png", 32, 32)
	load_sprite_table("sprite/robot.png", 32, 32)
def load_tile_table(filename, width, height):
	global tileTable
	image = pygame.image.load(filename).convert()
	image_width, image_height = image.get_size()
	tileTable = []
	for tile_x in range(0, image_width // width):
		line = []
		tileTable.append(line)
		for tile_y in range(0, image_height // height):
			rect = (tile_x * width, tile_y * height, width, height)
			line.append(image.subsurface(rect))
	tileTable = tileTable
def load_sprite_table(filename, width, height):
	global spriteTable
	image = pygame.image.load(filename).convert()
	image_width, image_height = image.get_size()
	spriteTable = []
	for tile_x in range(0, image_width // width):
		line = []
		spriteTable.append(line)
		for tile_y in range(0, image_height // height):
			rect = (tile_x * width, tile_y * height, width, height)
			line.append(image.subsurface(rect))

def rendererUpdate():
	global gameMap
	global screen
	screen.fill((255, 255, 255))
	drawMap()
	drawSprite()
	pygame.display.flip()
def drawMap():
	global tileTable
	global screen
	global gameMap
	for y in range(gameMap['height']):
		for x in range(gameMap['width']):
			node = gameMap['map'][y][x]
			tx = mapToTiles[node]['x']
			ty = mapToTiles[node]['y']
			tile = tileTable[tx][ty]
			screen.blit(tile, (x*32, y*32))
def drawSprite():
	global spriteTable
	global screen
	global robot_x
	global robot_y
	global robot_d
	di = ['u','l','r','d'].index(robot_d)
	tile = spriteTable[di][0]
	screen.blit(tile, ((robot_x * 32), (robot_y * 32)))

##### map
gameMap = None
def loadMap(filename):
	global gameMap
	with open(filename) as f:
		#map size
		line = f.readline().split(maxsplit=2)
		h, w = int(line[0]), int(line[1])
		#map shape
		themap = [[0 for x in range(w)] for y in range(h)]
		for y in range(h):
			line = f.readline().strip()
			for x in range(w):
				themap[y][x] = line[x]
		mapObject = {
			'width':w,
			'height':h,
			'map':themap
		}
		gameMap = mapObject

def getNode(x,y):
	global gameMap
	return gameMap['map'][y][x]

##### robot
robot_x = 0
robot_y = 0
robot_d = ''
frontwall = False
leftHandWall = False
backWall = False
rightHandWall = False
def robotInit(x,y,d):
	global robot_x
	global robot_y
	global robot_d
	global frontwall
	global leftHandWall
	global backWall
	global rightHandWall
	robot_x = x
	robot_y = y
	robot_d = d
	frontwall = False
	leftHandWall = False
	backWall = False
	rightHandWall = False

def GTNN(dist):
	for _ in range(dist):
		G1()

def G1():
	global robot_x
	global robot_y
	global robot_d
	isBlocked = whatDoISeeNoUpdate()[0]
	if not isBlocked:
		if robot_d == 'u':
			robot_y -=1
		elif robot_d == 'l':
			robot_x -=1
		elif robot_d == 'd':
			robot_y +=1
		elif robot_d == 'r':
			robot_x +=1
def turnLeft():
	global robot_d
	if robot_d == 'u':
		robot_d = 'l'
	elif robot_d == 'l':
		robot_d = 'd'
	elif robot_d == 'd':
		robot_d = 'r'
	elif robot_d == 'r':
		robot_d = 'u'
	else:
		raise ValueError
def turnRight():
	global robot_d
	if robot_d == 'u':
		robot_d = 'r'
	elif robot_d == 'l':
		robot_d = 'u'
	elif robot_d == 'd':
		robot_d = 'l'
	elif robot_d == 'r':
		robot_d = 'd'
	else:
		raise ValueError

def whatDoISee():
	global frontwall
	global leftHandWall
	global backWall
	global rightHandWall
	frontwall, leftHandWall, backWall, rightHandWall = whatDoISeeNoUpdate()

def whatDoISeeNoUpdate():
	global robot_x
	global robot_y
	global robot_d
	nodeState = getNode(robot_x, robot_y)
	node = int(nodeState,16)
	upwall = node % 2 == 1
	leftwall = (node // 2) % 2 == 1
	rightwall = (node // 4) % 2 == 1
	downwall = (node // 8) % 2 == 1
	if robot_d == 'u':
		frontwall = upwall
		leftHandWall = leftwall
		backWall = downwall
		rightHandWall = rightwall
	elif robot_d == 'l':
		frontwall = leftwall
		leftHandWall = downwall
		backWall = rightwall
		rightHandWall = upwall
	elif robot_d == 'd':
		frontwall = downwall
		leftHandWall = rightwall
		backWall = upwall
		rightHandWall = leftwall
	elif robot_d == 'r':
		frontwall = rightwall
		leftHandWall = upwall
		backWall = leftwall
		rightHandWall = downwall
	return (frontwall, leftHandWall, backWall, rightHandWall)

##### core
robotStartState = ()
if __name__=='__main__':
	rendererInit()
	loadMap('map.txt')
	gameIsRunning = True
	if len(sys.argv) <4:
		x, y, d = 0, 0, 'u'
	else:
		x = int(sys.argv[1])
		y = int(sys.argv[2])
		d = str(sys.argv[3])[0]
	robotStartState = (x,y,d)
	robotInit(x,y,d)
	lastTick = time.time()
	while gameIsRunning:
		rendererUpdate()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameIsRunning = False
		now = time.time()
		if now - lastTick > 0.5:
			lastTick += 0.5
			actionQueue = userCode.update()
			for i in actionQueue:
				if i == 'TL':
					turnLeft()
				elif i == 'TR':
					turnRight()
				elif i == 'G':
					GTNN(1)