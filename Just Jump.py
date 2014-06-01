import pygame as py
from pygame.locals import QUIT, KEYDOWN, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_UP, K_r, K_RETURN
from random import randrange

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
TRAP_SIZE = 5

class Title(object):
	
	def __init__(self):
		self.font = py.font.SysFont("Courier New", 30)
		self.title = self.font.render("Just Jump", 1, (255, 255, 255))
		self.x = SCREEN_WIDTH / 2 - self.title.get_width() / 2
		self.y = 20
		self.limit = 2
	
	def Render(self, screen):
		screen.blit(self.title, (randrange(self.x - self.limit, self.x + self.limit), randrange(self.y - self.limit, self.y + self.limit)))
		
	def Update(self):
		pass

class MenuState(object):
	
	def __init__(self, statesManager):
		self.font = py.font.SysFont("Courier New", 15)
		self.string_play = "Play"
		self.string_credits = "Credits"
		
		self.label_play = self.font.render("Play", 0, (255, 255, 255))
		self.label_credits = self.font.render("Credits", 0, (255, 255, 255))
		
		self.title = Title()
		
		self.selected = 0
		
		self.statesManager = statesManager
		
	def Render(self, screen):
		self.title.Render(screen)
		
		x, y = 20, 120
		
		lineBreak = 20
		limit = 1
		
		if self.selected == 0:
			screen.blit(self.label_play, (randrange(x - limit, x + limit), randrange(y - limit, y + limit) + lineBreak * 0))
		else:
			screen.blit(self.label_play, (x, y + lineBreak * 0))
			
		if self.selected == 1:
			screen.blit(self.label_credits, (randrange(x - limit, x + limit), randrange(y - limit, y + limit) + lineBreak * 1))
		else:
			screen.blit(self.label_credits, (x, y + lineBreak * 1))
		
		
	def Update(self):
		self.title.Update()
		
		self.Controls()
		self.UpdateStrings()
		self.UpdateLabels()
	
	def UpdateLabels(self):
		self.label_play = self.font.render(self.string_play, 0, (255, 255, 255))
		self.label_credits = self.font.render(self.string_credits, 0, (255, 255, 255))
		
	def Controls(self):
		key = py.key.get_pressed()
		
		if key[K_UP] and self.selected == 1:
			self.selected = 0
		elif key[K_DOWN] and self.selected == 0:
			self.selected = 1
			
		if key[K_RETURN] and self.selected == 0:
			self.statesManager.state = 1
			
	def UpdateStrings(self):
		self.string_play = "Play"
		self.string_credits = "Credits"
		
		if self.selected == 0:
			self.string_play = "[ Play ]"
		elif self.selected == 1:
			self.string_credits = "[ Credits ]"
			
		
			
			
		
class GameState(object):

	def __init__(self):
		self.player = Player()
		self.trapsManager = TrapsManager()
		self.collisionsManager = CollisionsManager()
	
		
	def Render(self, screen):

		self.player.Render(screen)
		self.trapsManager.Render(screen)
		
	def Update(self):
		self.player.Update()
		self.trapsManager.Update()
		
		self.UpdateCollisions()
				
	def UpdateCollisions(self):
		for projectile in self.trapsManager.projectilesManager.projectiles:
			if self.collisionsManager.Check(self.player, projectile) and not self.player.dead:
				self.player.Die()


class StatesManager(object):
	
	def __init__(self):
		self.state = 0
		self.gameState = GameState()
		self.menuState = MenuState(self)
	
	def Render(self, screen):
		if self.state == 0:
			self.menuState.Render(screen)
		elif self.state == 1:
			self.gameState.Render(screen)
	
	def Update(self):
		if self.state == 0:
			self.menuState.Update()
		elif self.state == 1:
			self.gameState.Update()

class Particle(object):
	
	def __init__(self, x, y, vx, vy):
		self.x, self.y, self.size = x, y, TRAP_SIZE
		self.color = (255, 100, 100)
		self.vx = vx
		self.vy = vy
		self.outBounds = False
		self.gravity = 0.65
	
	def Update(self):
		self.ApplyGravity()
		self.Move()
		self.CheckBounds()
		
	def CheckBounds(self):
		if (self.x < 0 or
		self.x + self.size > SCREEN_WIDTH or
		self.y < 0 or
		self.y + self.size > SCREEN_HEIGHT):
			self.outBounds = True
		
	def ApplyGravity(self):
		self.vy += self.gravity
		
	def Move(self):
		self.x += self.vx
		self.y += self.vy
		
	def Render(self, screen):
		py.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

		
class ParticlesManager(object):
	
	def __init__(self):
		self.particles = []
		
	def Update(self):
		for particle in self.particles:
			particle.Update()
			if particle.outBounds:
				self.particles.remove(particle)
				
	def Render(self, screen):
		for particle in self.particles:
			particle.Render(screen)
	
	def AddParticle(self, x, y, vx, vy):
		self.particles.append(Particle(x, y, vx, vy))


class CollisionsManager(object):
	def Check(self, ob1, ob2):
		if (ob1.x > ob2.x + ob2.size or
		ob1.y > ob2.y + ob2.size or
		ob1.x + ob1.width < ob2.x or
		ob1.y + ob1.height < ob2.y):
			return False
		else:
			return True

class Projectile(object):
	
	def __init__(self, x, y, vx):
		self.x, self.y, self.size = x, y, TRAP_SIZE
		self.vx = vx
		self.outBounds = False
	
	def Update(self):
		self.x += self.vx
		self.CheckBounds()
		
	def CheckBounds(self):
		if (self.x < 0 or
			self.x + self.size > SCREEN_WIDTH or
			self.y < 0 or
			self.y + self.size > SCREEN_HEIGHT):
				self.outBounds = True
	
	def Render(self, screen):
		py.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.size, self.size))


class ProjectilesManager(object):
	
	def __init__(self):
		self.projectiles = []
		
	def Update(self):
		for projectile in self.projectiles:
			projectile.Update()
			if projectile.outBounds:
				self.projectiles.remove(projectile)
				
	def Render(self, screen):
		for projectile in self.projectiles:
			projectile.Render(screen)
			
	def AddProjectile(self, x, y, side):
		self.projectiles.append(Projectile(x, y, 3 * side))

		
class Trap(object):
	
	def __init__(self, x, y, projectilesManager):
		self.x, self.y, self.size = x, y, TRAP_SIZE
		self.color = (255, 255, 255)
		self.projectilesManager = projectilesManager
	
	def Update(self):
		pass
		
	def Shoot(self):
		if self.x < SCREEN_WIDTH / 2:
			side = 1
		else:
			side = -1
			
		self.projectilesManager.AddProjectile(self.x, self.y, side)
		
	def Render(self, screen):
		py.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
		
		
class TrapsManager(object):
	
	def __init__(self):
		self.traps = []
		self.projectilesManager = ProjectilesManager()
		self.SetUpTraps()
		
		self.time = 0
		self.delay = 365
		
	
	def SetUpTraps(self):
		for i in range(5):
			self.traps.append(Trap(0, SCREEN_HEIGHT - 5 - i * 15, self.projectilesManager))
			self.traps.append(Trap(SCREEN_WIDTH - TRAP_SIZE, SCREEN_HEIGHT - 5 - i * 15, self.projectilesManager))
			
	def Update(self):
		for trap in self.traps:
			trap.Update()
		self.projectilesManager.Update()
		
		self.Timer()
		
	def Render(self, screen):
		for trap in self.traps:
			trap.Render(screen)
			
		self.projectilesManager.Render(screen)
	
	def Shoot(self):
		trap = randrange(0, len(self.traps))
		self.traps[trap].Shoot()
		
	def Timer(self):
		if py.time.get_ticks() - self.time > self.delay:
			self.time = py.time.get_ticks()
			self.Shoot()


class Player(object):
	
	def __init__(self):
		self.x, self.y, self.width, self.height = 0, 0, 20, 20
		self.x = SCREEN_WIDTH / 2 - self.width / 2
		self.vx, self.vy = 0, 0
		self.speed = 3
		self.gravity = 0.65
		self.color = (255, 100, 100)
		self.onGround = False
		self.jumpSpeed = 10
		self.particlesManager = ParticlesManager()
		self.dead = False
	
	def Update(self):
		if not self.dead:
			self.Controls()
			self.Move()
			self.CheckBounds()

		self.particlesManager.Update()
		
	def Controls(self):
		key = py.key.get_pressed()
		if key[K_RIGHT]:
			self.vx = self.speed
		elif key[K_LEFT]:
			self.vx = -self.speed
		else:
			self.vx = 0
			
		if key[K_SPACE] and self.onGround or key[K_UP] and self.onGround:
			self.vy = -self.jumpSpeed
			self.onGround = False
		
	def Move(self):
		self.ApplyGravity()
		
		self.x += self.vx
		self.y += self.vy
		
	def ApplyGravity(self):
		if not self.onGround:
			self.vy += self.gravity
		else:
			self.vy = 0
	
	def CheckBounds(self):
		if self.x < 0:
			self.x = 0
		elif self.x + self.width > SCREEN_WIDTH:
			self.x = SCREEN_WIDTH - self.width
			
		if self.y < 0:
			self.y = 0
		elif self.y + self.height > SCREEN_HEIGHT:
			self.y = SCREEN_HEIGHT - self.height
			self.onGround = True
	
	def Die(self):
		for i in range(20):
			self.particlesManager.AddParticle(self.x + self.width / 2, self.y + self.height / 2, randrange(-5, 5), randrange(-18, -8))
		self.dead = True
			
	def Render(self, screen):
		if not self.dead:
			py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
		self.particlesManager.Render(screen)
	
	def Reset(self):
		self.dead = False
		self.x = SCREEN_WIDTH / 2 - self.width / 2
		self.y = 0
		self.onGround = False
		self.vy = 0

		
def main():
	py.init()
	screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	py.display.set_caption("Just Jump")
	
	exit = False
	clear = (0, 0, 0)
	fps = py.time.Clock()
	
	
	statesManager = StatesManager()
	
	while not exit:
		for event in py.event.get():
			if event.type == QUIT:
				exit = True
			if event.type == KEYDOWN:
				if event.key == K_r:
					statesManager.gameState.player.Reset()
				
		screen.fill(clear)
		
		statesManager.Update()
		statesManager.Render(screen)
		
		
			
		py.display.update()
		fps.tick(60)
	return 0

if __name__ == "__main__":
	main()
