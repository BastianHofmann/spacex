import pygame, random
from classes import *
from process import process

pygame.init()

pygame.display.set_caption('SpaceX')

resolution = [360, 480]
screen = pygame.display.set_mode(resolution, 0, 32)
font = pygame.font.SysFont(None, 20)

clock = pygame.time.Clock()
fps = 60

# Instances
player = Player(100, resolution[1] - 50, 20, 18, 'resources/player.png')

background = pygame.image.load('resources/space_map.png')
death = pygame.image.load('resources/death.png')

difficulty = 50
looping = True;

while True:
	process(player)
	# logic
	player.motion(resolution)
	if player.alive():
		if randint(1, difficulty) == 1:
			Enemy(randint(0, 340), -20, 18, 18, 'resources/rock.png', player)
			if difficulty > 10 and randint(1, 5) == 1:
				difficulty -= 1

		for enemy in Enemy.List:
			enemy.motion(resolution, difficulty)

		for explosion in Explosion.List:
			explosion.update()

		score = font.render('score: ' + str(player.score), True, (255, 255, 0))
	else:
		looping = False
	# end logic

	# drawing
	screen.fill((0, 255, 0))
	screen.blit(background, background.get_rect())
	BaseClass.Sprites.draw(screen)
	if looping == False:
		screen.blit(death, death.get_rect())
	screen.blit(score, (10, 10))
	pygame.display.flip()
	# end drawing
	clock.tick(fps)