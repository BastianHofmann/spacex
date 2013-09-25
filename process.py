import pygame, sys

def process(app, player):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()

	if keys[pygame.K_d]:
		player.velx = 8
	elif keys[pygame.K_a]:
		player.velx = -8
	else:
		player.velx = 0

	if keys[pygame.K_SPACE]:
		if player.shot is None:
			player.shoot()

	if keys[pygame.K_r]:
		if app.running == False:
			app.run()

	# if keys[pygame.K_d]:
	# 	player.velx = 8