from graph import *
from random import randint
from time import sleep
#квадрат это минимальный размер 1го объекта, константа 25px


class Arena():
	#В основном этом классе создается очки для каждого квадрата на экране и цвет арены закрашивается на черный
	size = None #размер 1 ной клетки, не менять! 
	widht = 500 #ширина арены
	height = 600#высота арены
	points = [] #будем объект all points
	points_coordinates = []#будем хранить координаты очков, и убирать в функций Pacman если он съел очко
	radius = 1

	def __init__(self, size):
		self.size = size
		
		#background color
		brushColor('black')
		rectangle(0, 0, 500, 600)

		#создание очков 
		for i in range(20):
			for j in range(24):
				penColor('white')
				brushColor('white')
				self.points.append(circle(i*25+13, j*25+13, self.radius))
				self.points_coordinates.append([i*25, j*25]) # x, y

	def get_point(self, x, y):
		#если очко находится в том квадрате котором находится pacman съесть очко
		if [x, y] in self.points_coordinates:
			index = self.points_coordinates.index([x, y])
			deleteObject(self.points[index])

			self.points_coordinates[index] = [-1, -1]

		
class Box():
	#В этом классе создается стены
	size = None #размер 1 ной клетки, не менять!
	boxes = []
	boxes_coordinates = [] #будем хранить координаты каждого квадрата стены на арене и проверять в функций объекте PacMan сталкнулся ли Pacman со стеной

	def __init__(self, size):
		self.size = size

		penSize(4)
		penColor('green')
		brushColor('grey')
		for i in range(20):
			#верхняя стена
			self.boxes.append(rectangle(i*self.size, 0, i*self.size+self.size, 0+self.size))
			self.boxes_coordinates.append([i*self.size, 0])
			#нижняя стена			
			self.boxes.append(rectangle(i*self.size, 575, i*self.size+self.size, 575+self.size))
			self.boxes_coordinates.append([i*self.size, 575])
		for i in range(24):
			#левая стена
			self.boxes.append(rectangle(0, i*self.size, 0+self.size, i*self.size+self.size))
			self.boxes_coordinates.append([0, i*self.size])
			#правая стена			
			self.boxes.append(rectangle(475, i*self.size, 475+self.size, i*self.size+self.size))
			self.boxes_coordinates.append([475, i*self.size])

	def check_wall(self, x, y):
		if [x, y] in self.boxes_coordinates:
			#если есть стена тогда return True
			return True
		else:
			#если нету стены тогда return False 
			return False


class Stone():
	#В этом классе создается камни
	size = None #размер 1 ной клетки, не менять!
	stones = []
	stones_coordinates = [] #будем хранить координаты каждого квадрата стены на арене и проверять в функций объекте PacMan сталкнулся ли Pacman со стеной


	def __init__(self, size, count):
		self.size = size

		penSize(4)
		penColor('green')
		brushColor('grey')
		for i in range(count):
			x = randint(1, 19) #размер арены по координате x
			y = randint(1, 23) #размер арены по координате y

			self.stones.append(rectangle(x*self.size, y*self.size, x*self.size+self.size, y*self.size+self.size))
			self.stones_coordinates.append([x*self.size, y*self.size])

	def check_stone(self, x, y):
		if [x, y] in self.stones_coordinates:
			#если есть стена тогда return True
			return True
		else:
			#если нету стены тогда return False 
			return False


class Ghost():
	#В этой функций создается камни
	size = None #размер 1 ной клетки, не менять!
	radius = 10 #радиус тела pacmana, не менять!
	box = None
	stones = None
	ghosts = []
	ghosts_coordinates = []
	ghosts_direction = []
	center = 13 #смещение в центр квадрата для начального зарисовывания ghosts

	def __init__(self, size, count, box: Box, stones: Stone):
		self.size = size
		self.box = box
		self.stones = stones

		penSize(1)
		penColor('purple')
		brushColor('purple')
		for i in range(count):
			x = None
			y = None

			while True:
				x = randint(1, 19)*25 #размер арены по координате x
				y = randint(1, 23)*25 #размер арены по координате y

				is_wall = self.box.check_wall(x, y)
				is_stone = self.stones.check_stone(x, y)

				if is_wall==False and is_stone==False:
					break

			self.ghosts.append(circle(x+self.center, y+self.center, self.radius))
			self.ghosts_coordinates.append([x, y])
			self.ghosts_direction = ['stoped']*len(self.ghosts)

	def moveGhost(self):
		const = 3 #когда мы перемещаем ghost он смещается в угол квадрата в которой он стоит и чтобы обратно его перенести в центр мы используем эту константу
		for i in range(len(self.ghosts)):
			x_move = None
			y_move = None

			#если остановился меняем напрвление
			if self.ghosts_direction[i]=='stoped':
				#рандомно выбираем в какую сторону повернется ghost, если застрял
				random_direction = randint(1, 4)
				direction_dict = {1: 'right',
								  2: 'left',
								  3: 'up',
								  4: 'down'}

				self.ghosts_direction[i] = direction_dict[random_direction]
			#продолжаем двигаться по направлении
			if self.ghosts_direction[i]=='right':
				x_move = self.ghosts_coordinates[i][0] + self.size
				y_move = self.ghosts_coordinates[i][1] + 0
			elif self.ghosts_direction[i]=='left':
				x_move = self.ghosts_coordinates[i][0] - self.size
				y_move = self.ghosts_coordinates[i][1] + 0
			elif self.ghosts_direction[i]=='up':
				x_move = self.ghosts_coordinates[i][0] + 0
				y_move = self.ghosts_coordinates[i][1] - self.size
			elif self.ghosts_direction[i]=='down':
				x_move = self.ghosts_coordinates[i][0] + 0
				y_move = self.ghosts_coordinates[i][1] + self.size


			#если в пусти есть стена остановиться
			is_wall = self.box.check_wall(x_move, y_move)
			is_stone = self.stones.check_stone(x_move, y_move)

			if is_wall==False and is_stone==False:
				#изменить направление тела pacmana
				moveObjectTo(self.ghosts[i], x_move+const, y_move+const)

				#изменяем текущее значение pacmana   
				self.ghosts_coordinates[i][0] = x_move
				self.ghosts_coordinates[i][1] = y_move
			else:
				self.ghosts_direction[i] = 'stoped'

class Energizer():
	size = None
	box = None
	stones = None
	energizer = []
	energizer_coordinates = []
	time = 45

	def __init__(self, size, count, box: Box, stones: Stone):
		self.size = size
		self.box = box
		self.stones = stones

		penSize(1)
		penColor('orange')
		brushColor('pink')
		for i in range(count):
			x = None
			y = None

			while True:
				x = randint(1, 19)*25 #размер арены по координате x
				y = randint(1, 23)*25 #размер арены по координате y

				is_wall = self.box.check_wall(x, y)
				is_stone = self.stones.check_stone(x, y)

				if is_wall==False and is_stone==False:
					break

			self.energizer.append(circle(x+13, y+13, 4))
			self.energizer_coordinates.append([x, y])

	def get_point(self, x, y):
		if [x, y] in self.energizer_coordinates:
			index = self.energizer_coordinates.index([x, y])
			deleteObject(self.energizer[index])

			self.energizer_coordinates[index] = [-1, -1]
			return self.time



class PacMan():
	size = None #размер 1 ной клетки, не менять!
	body = None #переменная где будем хранить тело pacmana(круг, желтая)
	mouth = None #переменная где будем хранить рот pacmana(треугольник, черная)
	mouth_opened = False #с каждым шагом pacman открывает/закрывает рот, булевая функция чтобы наблюдать за этим движением
	arena = None#переменная где храним объект Arena
	energizers = None#переменная где храним объект Energizer
	box = None #переменная где храним объект Box
	stones = None #переменная где храним объект Stone
	radius = 10 #радиус тела pacmana, не менять!
	energized = 0#время которое дается чтобы стать невидимым для Ghost
	color = {}

	#начальные позиций pacmana
	current_x = None
	current_y = None

	center = 13 #смещение в центр квадрата для начального зарисовывания pacmana

	def __init__(self, size, arena: Arena, energizers: Energizer, box: Box, stones: Stone):
		self.size = size
		self.arena = arena
		self.energizers = energizers
		self.stones = stones
		self.box = box
		#создаем тело pacmana
		penSize(1)
		penColor('yellow')
		brushColor('yellow')

		while True:
			self.current_x = randint(1, 19)*25 #размер арены по координате x
			self.current_y = randint(1, 23)*25 #размер арены по координате y

			is_wall = self.box.check_wall(self.current_x, self.current_y)
			is_stone = self.stones.check_stone(self.current_x, self.current_y)

			if is_wall==False and is_stone==False:
				break

		self.body = circle(self.current_x+self.center, self.current_y+self.center, self.radius)

		for i in range(self.energizers.time+1):
			g = int((self.energizers.time-i)* (255/self.energizers.time))

			self.color[i] = [255, g, 0]

	def mouth_open_close(self):
		#фунция отвечает чтобы pacman открывал/закрывал рот
		if self.mouth_opened==True:
			self.mouth_opened = False
		elif self.mouth_opened==False:
			self.mouth_opened = True

	def mouth_side(self, side):
		#фунция отвечает чтобы pacman pacman поменял лицевую сторону
		penSize(1)
		penColor('black')
		brushColor('black')

		bite = 6 #это основание треуголика, ширина рота pacmana
		lips = 10#это расстояние от центра пакамана и его основания которая лежит перпендикулярно
		const = self.center#начальная точка рота(треугольика) pacmana это его центр мы его берем как константу

		if side=='right':
			self.mouth = polygon( [(self.current_x+const,      self.current_y+const),      (self.current_x+const+lips, self.current_y+const-bite), 
								   (self.current_x+const+lips, self.current_y+const+bite), (self.current_x+const,      self.current_y+const)] )
		elif side=='left':
			self.mouth = polygon( [(self.current_x+const,      self.current_y+const),      (self.current_x+const-lips, self.current_y+const-bite), 
								   (self.current_x+const-lips, self.current_y+const+bite), (self.current_x+const,      self.current_y+const)] )
		elif side=='up':
			self.mouth = polygon( [(self.current_x+const,      self.current_y+const),      (self.current_x+const-bite, self.current_y+const-lips), 
								   (self.current_x+const+bite, self.current_y+const-lips), (self.current_x+const,      self.current_y+const)] )
		elif side=='down':
			self.mouth = polygon( [(self.current_x+const,      self.current_y+const),      (self.current_x+const-bite, self.current_y+const+lips), 
								   (self.current_x+const+bite, self.current_y+const+lips), (self.current_x+const,      self.current_y+const)] )

	def movePacman(self, direction):
		const = 3 #когда мы перемещаем pacmana он смещается в угол квадрата в которой он стоит и чтобы обратно его перенести в центр мы используем эту константу
		
		x_move = 0
		y_move = 0
		#вычисляем в какую сторону повернется pacman
		if direction=='right':
			x_move = self.current_x + self.size
			y_move = self.current_y + 0
		elif direction=='left':
			x_move = self.current_x - self.size
			y_move = self.current_y + 0
		elif direction=='up':
			x_move = self.current_x + 0
			y_move = self.current_y - self.size
		elif direction=='down':
			x_move = self.current_x + 0
			y_move = self.current_y + self.size

		#если в пути есть очко съесть
		self.arena.get_point(x_move, y_move)
		#если в пути есть Energizer
		# if self.energizers.get_point(x_move, y_move) == True:
		self.energized = self.energizers.time if self.energizers.get_point(x_move, y_move) == self.energizers.time else self.energized
		
		#если в пусти есть стена остановиться
		is_wall = self.box.check_wall(x_move, y_move)
		is_stone = self.stones.check_stone(x_move, y_move)

		if is_wall==False and is_stone==False:
			#изменить направление тела pacmana
			if pacman.energized == 0:
				moveObjectTo(self.body, x_move+const, y_move+const)
			else:
				deleteObject(self.body)

				if self.energized==1 or self.energized==2:
					penSize(1)
					penColor('yellow')
					brushColor('yellow')
					self.body = circle(x_move+self.center, y_move+self.center, self.radius)
				else:
					r = self.color[self.energized][0]
					g = self.color[self.energized][1]
					b = self.color[self.energized][2]
					penSize(1)
					penColor(r, g, b)
					brushColor(r, g, b)
					self.body = circle(x_move+self.center, y_move+self.center, self.radius)

			#изменить направление рота pacmana
			deleteObject(self.mouth)

			#изменяем текущее значение pacmana   
			self.current_x = x_move
			self.current_y = y_move

			#изменить движение рота pacmana закрыть/открыть
			self.mouth_open_close()

			#изменить лицевую сторону pacmana
			if self.mouth_opened==False:
				self.mouth_side(direction)
		else:
			if pacman.energized != 0:
				deleteObject(self.body)

				if self.energized==1 or self.energized==2:
					penSize(1)
					penColor('yellow')
					brushColor('yellow')
					self.body = circle(self.current_x+self.center, self.current_y+self.center, self.radius)
				else:
					r = self.color[self.energized][0]
					g = self.color[self.energized][1]
					b = self.color[self.energized][2]
					penSize(1)
					penColor(r, g, b)
					brushColor(r, g, b)
					self.body = circle(self.current_x+self.center, self.current_y+self.center, self.radius)

	def died(self):
		#если pacman умер изменить его цвет на красный
		penSize(1)
		penColor('white')
		brushColor('white')
		self.body = circle(self.current_x+self.center, self.current_y+self.center, self.radius)
	


def keyPressed(event):
	global direction
	if event.keycode == VK_LEFT: 
		direction = 'left'
	if event.keycode == VK_RIGHT:
		direction = 'right'
	if event.keycode == VK_UP:
		direction = 'up'
	if event.keycode == VK_DOWN:
		direction = 'down'


def check_intersection():
	#проверяет pacman и ghost по координатам пересечения 
	global arena
	global stones
	global box
	global pacman
	global ghosts
	global direction
	global gameOver
	global energizers
	if pacman.energized == 0:
		if [pacman.current_x, pacman.current_y] in ghosts.ghosts_coordinates:
			deleteObject(pacman.mouth)
			deleteObject(pacman.body)
			for i in arena.points:
				deleteObject(i)
			for i in stones.stones:
				deleteObject(i)
			for i in box.boxes:
				deleteObject(i)
			for i in energizers.energizer:
				deleteObject(i)
			for i in ghosts.ghosts:
				deleteObject(i)
			gameOver = True 
			pacman.died()
	else:
		pacman.energized -= 1

def update():
	global pacman
	global ghosts
	global direction
	global gameOver
	if direction != None:
		if gameOver==True:
			sleep(2)
			exit()
		#проверить pacman и ghost в одной ячейке?
		check_intersection()
		if gameOver==False:
			pacman.movePacman(direction)
		#проверить pacman и ghost в одной ячейке?
		check_intersection()
		if gameOver==False:
			ghosts.moveGhost()
			


size = 25 #размер 1го квадрата(блока), не менять!
arena = Arena(size=size)
box = Box(size=size)
stones = Stone(size=size, count=25)
ghosts = Ghost(size=size, count=5, box=box, stones=stones)
energizers = Energizer(size=size, count=15, box=box, stones=stones)
pacman = PacMan(size=size, arena=arena, energizers=energizers, box=box, stones=stones) #don't change variable name because we use this variable in update() function
gameOver = False

direction = None

onKey(keyPressed)
onTimer(update, 180)
run()