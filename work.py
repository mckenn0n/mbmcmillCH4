from __future__ import division #Added so that work.py will run with Python 2.7
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pygame
import random
count = 0
def ranNum():
 	return random.uniform(0, 1)

class Ring():#self.moons.append(Ring(self.size + 0.1, self.size + 0.3, 20, 20, (1, 1, 1), 1.2))
	def __init__(self, inner_r, outer_r, n, rings, color, rotZ):
		self.inner_r = inner_r
		self.outer_r = outer_r
		self.n = n
		self.rings = rings
		self.color = color
		self.rotZ = rotZ
		return

	def render(self):
		glPushMatrix()
		glColor3f(self.color[0], self.color[1], self.color[2])
		# glRotatef(45.0, 1, 0, 0)  
		# glRotatef(45, 0, 1, 0) 
		glRotatef(self.rotZ, 1, 0, 0) 
		glutWireTorus(self.inner_r, self.outer_r, self.n, self.rings)
		glPopMatrix()
		return

class Cube():
	def __init__(self, size, translate, speed_list_XYZ):
		self.size = size
		self.translate = translate
		self.rotX = 0
		self.rotY = 0
		self.rotZ = 0
		self.speed_list_XYZ = speed_list_XYZ
		return

	def render(self):
		glPushMatrix()

		glColor3f(ranNum(), ranNum(), ranNum())
		glTranslatef(self.translate[0], self.translate[1], self.translate[2]) 
		glRotatef(self.rotX, 1, 0, 0)  
		glRotatef(self.rotY, 0, 1, 0) 
		glRotatef(self.rotZ, 0, 0, 1) 
		# glutWireSphere(self.size,self.s1,self.s2)
		glutWireCube(self.size) 
		self.rotX += self.speed_list_XYZ[0] #3
		self.rotY += self.speed_list_XYZ[1] #2
		self.rotZ += self.speed_list_XYZ[2] #1.5
		glPopMatrix()
		return

class Sphere():
	def __init__(self, size, translate, s1, s2, speed_list_XYZ):
		self.size = size
		self.translate = translate
		self.s1 = s1
		self.s2 = s2
		self.rotX = 0
		self.rotY = 0
		self.rotZ = 0
		self.speed_list_XYZ = speed_list_XYZ
		return

	def render(self):
		glPushMatrix()

		glColor3f(ranNum(), ranNum(), ranNum())
		glTranslatef(self.translate[0], self.translate[1], self.translate[2]) 
		glRotatef(self.rotX, 1, 0, 0)  
		glRotatef(self.rotY, 0, 1, 0) 
		glRotatef(self.rotZ, 0, 0, 1) 
		glutWireSphere(self.size,self.s1,self.s2)
		# glutWireCube(self.size) 
		self.rotX += self.speed_list_XYZ[0] #3
		self.rotY += self.speed_list_XYZ[1] #2
		self.rotZ += self.speed_list_XYZ[2] #1.5
		glPopMatrix()
		return


class moon():
	def __init__(self, size, dist, color, speed):
		self.size = size
		self.dist = dist
		self.color = color
		self.speed = speed
		self.rotY = 35
		return

	def render(self):
		glPushMatrix()
		glColor3f(self.color[0], self.color[1], self.color[2])
		#glRotatef(90.0, 1, 0, 0)  
		glRotatef(self.rotY, 0, 1, 0) 
		#glRotatef(35.0, 0, 0, 1) 
		glTranslatef(0.0, 0.0, self.dist) 
		glutWireSphere(self.size,20,20)
		self.rotY += self.speed
		glPopMatrix()
		return

class planet():
	def __init__(self, size, dist, color, speed, hasMoon, hasRing, c):
		self.moons = []
		self.rings = []
		self.size = size
		self.c = c
		self.dist = dist
		self.color = color
		self.speed = speed/2
		self.rotY = 160
		self.hasMoon = hasMoon
		self.hasRing = hasRing
		if self.hasRing:
			if self.c == 0:
				self.moons.append(Ring(self.size -.3, self.size + .5, 2, 20, (1, 1, 1), 90))
			if self.c == 1:
				self.moons.append(Ring(self.size -.3, self.size + .5, 2, 20, (0, 0.807843, 0.819608), 0))


		if self.hasMoon:
			self.moons.append(moon(self.size/3, self.size + .2, (1, 1, 1), 1.2))
		return

	def render(self):
		# glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glColor3f(self.color[0], self.color[1], self.color[2])
		glRotatef(90.0, 1, 0, 0)  
		glRotatef(self.rotY, 0, 1, 0) 
		glRotatef(35.0, 0, 0, 1) 
		glTranslatef(0.0, 0.0, self.dist) 
		glutWireSphere(self.size,20,20) 
		self.rotY += self.speed
		for m in self.moons:
			m.render();
		glPopMatrix()	
		
		return

class GLContext():
	def __init__(self, screen):
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		self.cubes = []
		self.spheres = []
		self.screen = screen
		self.aspect = screen.get_width()/screen.get_height()
		self.planets = []
		gluPerspective(45.0, self.aspect, 0.1, 200.0)
		self.rot = 0
		self.rot2 = 45
		self.planets.append(planet(.2, 4, (0.7, 0.6, 1.0), 5, False, False, -1))
		self.planets.append(planet(.3, 5, (1, 0.647059, 0), 4, False, False, -1))
		self.planets.append(planet(.3, 6.2, (0, 0, 0.8), 3.5, True, False, -1))
		self.planets.append(planet(.25, 7.5, (0.545098, 0.0, 0.0), 2.5, False, False, -1))
		self.planets.append(planet(.8, 10, (0.823529, 0.705882, 0.54902), 1.5, False, False, -1))
		self.planets.append(planet(.5, 12, (.85, 0.643137, 0.12549), 1.3, False, True, 0))
		self.planets.append(planet(.4, 14, (0, 0.807843, 0.819608), 1.2, False, True, 1))
		self.planets.append(planet(.4, 16, (0, 0, 0.501961), 1.15, False, False, -1))
		self.planets.append(planet(.08, 19, (0, 1, 1), 1.1, False, False, -1))
		self.cubes.append(Cube(.5, (10, 10, 5), (3, 2, 1.5)))
		self.spheres.append(Sphere(.25, (10, 10, 5), 20, 20, (3, 2, 1.5)));
		self.spheres.append(Sphere(.75, (10, 10, 5), 20, 2, (4, 5, 10)));
		self.spheres.append(Sphere(1.75, (10, 10, 5), 3, 3, (1, 1, 1)));
		self.spheres.append(Sphere(1, (10, 10, 5), 20, 20, (0, 1, 0)));
		self.cubes.append(Cube(1.5, (10, 10, 5), (1, 0, 0)))
		self.spheres.append(Sphere(2, (10, 10, 5), 3, 2, (1, 1, 1)));
		return

	def check_events(self):
 		for event in pygame.event.get():
 			if event.type == pygame.QUIT:
 				exit()
 				if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
 					exit()
 		return


	def display(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		#glBegin(GL_QUADS)

		glColor3f(1.0, 1.0, 0.0)
		glTranslatef(0.0, 0.0, -30.0) #trasnlates scene -1.0 units in depth (away from the camera)
		glRotatef(-70.0, 1, 0, 0)  
		glRotatef(20.0, 0, 1, 0) 
		glRotatef(self.rot, 0, 0, 1) 

		glutWireSphere(2,20,20) 
		self.rot -= .5
		for p in self.planets:
			p.render()
		for c in self.cubes:
			c.render()
		for s in self.spheres:
			s.render()

		#glEnd()
		glPopMatrix()

		return
def main():
	pygame.init() #initializes PyGame
	glutInit()
	screen = pygame.display.set_mode((600,600), pygame.OPENGL|pygame.DOUBLEBUF) #makes screen context for our application
	context=GLContext(screen) #makes OpenGL context for your application

	#Your display loop!
	while True:
		context.check_events() #checks for user events
		context.display() #calls display function
		pygame.display.flip() #swaps buffers and sends rendered image to screen

#ensures that main() gets called when the program runs
if __name__ == '__main__':
	try:
		main()
	finally:
		pygame.quit()