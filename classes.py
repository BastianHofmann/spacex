import pygame, math
from random import randint
from process import process

class Application():
	
	screen = None

	font = None

	clock = None

	fps = 0

	resolution = []

	running = False

	caption = ''

	def __init__(self, caption, resolution, fps):
		self.screen = pygame.display.set_mode(resolution)
		self.font = font = pygame.font.SysFont(None, 20)
		self.clock = clock = pygame.time.Clock()
		self.fps = fps
		self.resolution = resolution
		self.caption = caption

	def run(self):
		self.running = True

		loop = Loop(self)

		pygame.display.set_caption(self.caption)

		loop.player = Player(100, self.resolution[1] - 50, 20, 18, 'resources/player.png')
		loop.images.append(pygame.image.load('resources/space_map.png'))
		loop.images.append(pygame.image.load('resources/death.png'))
		loop.difficulty = 50

		while True:
			loop.tick()
			self.clock.tick(self.fps)


class Loop():

	player = None

	images = []

	def __init__(self, app):
		self.app = app
	
	def tick(self):
		process(self.player)
		self.player.motion(self.app.resolution)
		if self.player.alive():
			if randint(1, self.difficulty) == 1:
				Enemy(randint(0, 340), -20, 18, 18, 'resources/rock.png', self.player)
				if self.difficulty > 10 and randint(1, 5) == 1:
					self.difficulty -= 1

			for enemy in Enemy.List:
				enemy.motion(self.app.resolution, self.difficulty)

			for explosion in Explosion.List:
				explosion.update()

			self.score = self.app.font.render('score: ' + str(self.player.score), True, (255, 255, 0))
		else:
			self.app.running = False

		self.draw()

	def draw(self):
		self.app.screen.fill((0, 255, 0))
		self.app.screen.blit(self.images[0], self.images[0].get_rect())
		BaseClass.Sprites.draw(self.app.screen)
		if self.app.running == False:
			self.app.screen.blit(self.images[1], self.images[1].get_rect())
		self.app.screen.blit(self.score, (10, 10))
		pygame.display.flip()
		
		

class BaseClass(pygame.sprite.Sprite):

	Sprites = pygame.sprite.Group()

	def __init__(self, x, y, width, height, image):
		pygame.sprite.Sprite.__init__(self)

		BaseClass.Sprites.add(self)

		self.image = self.make_image(image)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height

	def make_image(self, image):
		return pygame.transform.scale2x(pygame.image.load(image))


class Player(BaseClass):

	score = 0

	List = pygame.sprite.Group()

	shot = None
	
	def __init__(self, x, y, width, height, image):
		BaseClass.__init__(self, x, y, width, height, image)

		self.List.add(self)

		self.velx = 0

	def motion(self, resolution):
		self.score += 1

		if self.velx > 0:
			self.image = self.make_image('resources/player_r.png')
		elif self.velx < 0:
			self.image = self.make_image('resources/player_l.png')
		else:
			self.image = self.make_image('resources/player.png')

		self.rect.x += self.velx

		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x + self.width + 20> resolution[0]:
			self.rect.x = resolution[0] - self.width - 20

		if self.shot is not None:
			self.shot.motion(resolution)

		for enemy in Enemy.List:
			if pygame.sprite.collide_rect(self, enemy):
				self.kill()

	def shoot(self):
		if self.alive():
			self.shot = Shot(self.rect.x + 15, self.rect.y, 5, 9, 'resources/bullet.png', self)

	def set_shot(self, shot):
		self.shot = shot

class Shot(BaseClass):

	List = pygame.sprite.Group()
	
	def __init__(self, x, y, width, height, image, player):
		BaseClass.__init__(self, x, y, width, height, image)

		self.List.add(self)

		self.vely = 20
		self.player = player

	def motion(self, resolution):
		self.rect.y -= self.vely

		if self.rect.y < 0:
			self.destroy()

	def destroy(self):
		self.kill()
		self.player.set_shot(None)


class Enemy(BaseClass):

	List = pygame.sprite.Group()
	
	def __init__(self, x, y, width, height, image, player):
		BaseClass.__init__(self, x, y, width, height, image)

		self.List.add(self)
		self.player = player

	def motion(self, resolution, difficulty):
		self.rect.y += math.sqrt(55 - difficulty)

		if self.rect.y > resolution[1]:
			self.kill()

		for shot in Shot.List:
			if pygame.sprite.collide_rect(self, shot):
				self.kill()
				shot.destroy()
				self.player.score += 200
				Explosion(self.rect.x, self.rect.y, 18, 18, 'resources/explosion0.png')


class Explosion(BaseClass):

	List = pygame.sprite.Group()

	ticks = 0
	
	def __init__(self, x, y, width, height, image):
		BaseClass.__init__(self, x, y, width, height, image)

		self.List.add(self)

	def update(self):
		self.ticks += 1

		if self.ticks % 5:
			self.image = self.make_image('resources/explosion' + str(self.ticks / 5) + '.png')

		if self.ticks > 30:
			self.kill()
		
