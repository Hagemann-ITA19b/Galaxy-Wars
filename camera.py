import pygame
def mouse_control(self):
	camera_borders = {'left': 10, 'right': 10, 'top': 10, 'bottom': 10}
	mouse = pygame.math.Vector2(pygame.mouse.get_pos())
	left_border = camera_borders['left']
	top_border = camera_borders['top']
	right_border = self.screen.get_size()[0] - camera_borders['right']
	bottom_border = self.screen.get_size()[1] - camera_borders['bottom']


	# Can't get out of the screen
	if self.background.rect.left > 0:
		self.background.rect.left = 0
		for ship in self.ships:
			ship.rect.left = ship.rect.left - self.offset[0]
			ship.waypoint_x = ship.waypoint_x - self.offset[0]

	if self.background.rect.top > 0:
		self.background.rect.top = 0
		for ship in self.ships:
			ship.rect.top = ship.rect.top + self.offset[1]
			ship.waypoint_y = ship.waypoint_y + self.offset[1]

	if self.background.rect.right < self.screen.get_size()[0]:
		self.background.rect.right = self.screen.get_size()[0]
		for ship in self.ships:
			ship.rect.right = ship.rect.right - self.offset[0]
			ship.waypoint_x = ship.waypoint_x - self.offset[0]

	if self.background.rect.bottom < self.screen.get_size()[1]:
		self.background.rect.bottom = self.screen.get_size()[1]
		for ship in self.ships:
			ship.rect.bottom = ship.rect.bottom + self.offset[1]
			ship.waypoint_y = ship.waypoint_y + self.offset[1]

	





	if top_border < mouse.y < bottom_border:
		if mouse.x < left_border:
			self.offset = (5, 0)
			pygame.mouse.set_pos((left_border,mouse.y))
		elif mouse.x > right_border:
			self.offset = (-5, 0)
			pygame.mouse.set_pos((right_border,mouse.y))
	elif mouse.y < top_border:
		if mouse.x < left_border:
			self.offset = (5, -5)
			pygame.mouse.set_pos((left_border,top_border))
		if mouse.x > right_border:
			self.offset = (-5, -5)
			pygame.mouse.set_pos((right_border,top_border))
	elif mouse.y > bottom_border:
		if mouse.x < left_border:
			self.offset = (5, 5)
			pygame.mouse.set_pos((left_border,bottom_border))
		if mouse.x > right_border:
			self.offset = (-5, 5)
			pygame.mouse.set_pos((right_border,bottom_border))
	if left_border < mouse.x < right_border:
		if mouse.y < top_border:
			self.offset = (0, -5)
			pygame.mouse.set_pos((mouse.x,top_border))
		if mouse.y > bottom_border:
			self.offset = (0, 5)
			pygame.mouse.set_pos((mouse.x,bottom_border))
	if left_border < mouse.x < right_border and top_border < mouse.y < bottom_border:
		self.offset = (0, 0)

