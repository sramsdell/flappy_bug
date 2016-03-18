#-------------------------------------------------------------------------------
# Name:        Flappy Bug
# Purpose:      Flappy bird clone for practice
#
# Author:      Steve
#
# Created:     1/14/2016
# Copyright:   (c) Stevie 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame,sys,random

SIZE = (400,400)
BLACK = (0,0,0)
RED = (255,0,0)

pygame.init()
screen = pygame.display.set_mode(SIZE)

class Imageinfo():
    def __init__(self,size,center,radius):
        self.size = size
        self.center = center
        self.radius = radius
    def get_size(self):
        return self.size
    def get_radius(self):
        return self.radius
    def get_center(self):
        return self.center



class Bug():
    def __init__(self,pos,vel,image,imagesize):
        self.pos = pos
        self.vel = vel
        self.image = pygame.image.load(image)
        self.size = imagesize
        self.center = (imagesize[0]/2,imagesize[1]/2)
        self.radius = imagesize[0]/2
    def update(self):

        self.vel[1] += .15
        self.pos[1] += self.vel[1]
        if self.pos[1] <= 0:
            self.pos[1] = 0
            self.vel[1] += 4

    def render(self,screen):
        if self.vel[1] <= 0:
            screen.blit(self.image,self.pos,(32,0,32,32))
        else:
            screen.blit(self.image,self.pos,(0,0,32,32))
    def get_center(self):
        return self.center
    def get_radius(self):
        return self.radius

    def get_pos(self):
        return self.pos

    def jump(self):
        self.vel[1] = 0
        self.vel[1] -=5

    def reset(self):
        self.vel[1] = 0
        self.pos = [SIZE[0]/2,SIZE[1]/2]

class Wall():
    def __init__(self,pos,vel):
        self.pos = list(pos)
        self.vel = list(vel)
        self.thickness = 50 + (game.get_score()*3)
        self.gap = 125 - game.get_score()

    def get_pos(self):
        return self.pos
    def get_gap(self):
        return self.gap
    def get_thickness(self):
        return self.thickness
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def render(self,screen):

        pygame.draw.rect(screen, RED,[self.pos,[self.thickness,-SIZE[1]]])
        pygame.draw.rect(screen, RED,[[self.pos[0],self.pos[1]+self.gap],[self.thickness,SIZE[1]]])


class Game_manager():
    def __init__(self):
        self.wall_set = set([])
        self.score = -1
        self.highscore = 0

    def get_wall_set(self):
        return self.wall_set.copy()
    def add_wall_set(self,wall):
        self.wall_set.add(wall)
    def remove_wall_set(self,wall):
        self.wall_set.discard(wall)

    def get_score(self):
        return self.score
    def add_score (self,num):
        self.score += num

    def get_highscore(self):
        return self.highscore

    def alt_highscore(self,score):
        self.highscore = score

    def reset(self,screen,manager,bug):
        highscore()
        manager.currentstate.change(IntroState(screen))
        self.wall_set = set([])
        bug.reset()
        self.score = -1

def highscore():
    if game.get_score() > game.get_highscore():
        game.alt_highscore(game.get_score())



def bug_walls_collide(screen,manager,bug,walls):
    if bug.get_pos()[1]+bug.get_center()[1] >= SIZE[1]-bug.get_radius():
        game.reset(screen,manager,a_bug)

    for wall in walls:
        if bug.get_pos()[1] + bug.get_center()[1]<= wall.get_pos()[1] + bug.get_radius()or bug.get_pos()[1] + bug.get_center()[1] >= wall.get_pos()[1]+wall.get_gap()-bug.get_radius():
            if bug.get_pos()[0] + bug.get_center()[0] >= wall.get_pos()[0] - bug.get_radius() and bug.get_pos()[0] + bug.get_center()[0] <= wall.get_pos()[0] + wall.get_thickness() + bug.get_radius():
                game.reset(screen,manager,a_bug)


def wall_spawn(wall_set):
    wallgap = 100
    if len(wall_set) < 1:
        a_wall = Wall([SIZE[0],random.randint(0,SIZE[1]-100)],[-2-(game.get_score()/20.0),0])
        game.add_wall_set(a_wall)
        game.add_score(1)

def wall_process(screen,wall_set):

    for wall in wall_set:
        wall.update()
        wall.render(screen)
        if wall.get_pos()[0] <= 0:
            game.remove_wall_set(wall)


def main():

    clock = pygame.time.Clock()
    running = True
    manager = TransitionManager(screen)

    while running:
        running = manager.state.event_handler(pygame.event.get())

        manager.update()
        manager.render(screen)
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


class TransitionManager:
    #note state is "self" breaking convention for better understanding
    def __init__(self,screen):
        self.change(IntroState(screen))

    def change(self,state):
        self.state = state
        self.state.currentstate = self

    def update(self):
        self.state.update()

    def render(self,screen):
        self.state.render(screen)


class MasterState:
    def __init__(self,screen):
        self.screen = screen

    def quit(self,event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return False

class PlayState(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.myfont = pygame.font.SysFont("fixedsys", 20)
    def update(self):
        self.scorelabel = self.myfont.render("Score = "+str(game.get_score()),1,RED)
    def render(self,screen):
        screen.fill(BLACK)
        logic(screen,self)
        a_bug.update()
        a_bug.render(screen)
        screen.blit(self.scorelabel,(20,20))

    def event_handler(self,events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    a_bug.jump()
                elif event.key == pygame.K_p:
                    self.currentstate.change(IntroState(screen))
        return True

def logic(screen,manager):
    wall_spawn(game.get_wall_set())
    wall_process(screen,game.get_wall_set())
    bug_walls_collide(screen,manager,a_bug,game.get_wall_set())

class IntroState(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.font = pygame.font.SysFont("fixedsys",24)
        self.text = self.font.render("Flappy Bug; SPACE to start",1,BLACK)
        #self.high = self.font.render("Highscore: "+str(game.get_highscore()),1,BLACK)
    def update(self):
        self.high = self.font.render("Highscore: "+str(game.get_highscore()),1,BLACK)
    def render(self,screen):
        screen.fill(RED)
        screen.blit(self.text,(SIZE[0]/2-100,SIZE[1]/2))
        screen.blit(self.high,(SIZE[0]/2-50,SIZE[1]/2+50))
    def event_handler(self,events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.currentstate.change(PlayState(screen))
        return True
a_bug = Bug([SIZE[0]/2,SIZE[1]/2],[0,0],"ugly_bug.png",(32,32))
game = Game_manager()

if __name__ == '__main__':
    main()
