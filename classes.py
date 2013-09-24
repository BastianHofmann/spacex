import pygame
from random import randint

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

	List = pygame.sprite.Group()
	
	def __init__(self, x, y, width, height, image):
		BaseClass.__init__(self, x, y, width, height, image)

		Player.List.add(self)

		self.velx = 0
		self.shots = pygame.sprite.Group()

	def motion(self, resolution):
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

		for shot in self.shots:
			shot.motion(resolution)

	def shoot(self):
		shot = Shot(self.rect.x, self.rect.y, 5, 9, 'resources/bullet.png')

		self.shots.add(shot)

class Shot(BaseClass):

	List = pygame.sprite.Group()
	
	def __init__(self, x, y, width, height, image):
		BaseClass.__init__(self, x, y, width, height, image)

		Player.List.add(self)

		self.vely = 20

	def motion(self, resolution):
		self.rect.y -= self.vely

		if self.rect.y > resolution[1]:
			self.List.remove(self)
		