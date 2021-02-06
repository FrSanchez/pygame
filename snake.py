#! /usr/bin/env python

# June 1, 2006
# MIT License

import math, os, pygame as pg, random
from pygame.locals import *

# game constants
SCREENRECT = Rect(0, 0, 960, 640)
SCORE = 0

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_sound(file):
    """ because pygame can be be compiled without mixer.
    """
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None

def load_image(file):
    """ loads an image, prepares it for play
    """
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = load_image(filename)
    def imgat(self, rect, colorkey = None):
        rect = Rect(rect)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey((0,0,0))
        return image
    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs

class Ground:
    tileside = 32
    # when drawing tiles, the origin is at (topx, topy),
    # so that a filled tile map will be centered on the screen
    topx = 0
    topy = 0
    # numxtiles, numytiles, and rect refer to the region where the ball is allowed to be in
    numxtiles = 30
    numytiles = 20
    rect = pg.Rect(topx + tileside, topy + tileside, tileside*(numxtiles), tileside*(numytiles))
    def __init__(self):
        self.background = pg.Surface(SCREENRECT.size).convert()
        self.makebg()
    def drawtile(self, tile, x, y):
        self.background.blit(tile, (self.topx + self.tileside*x, self.topy + self.tileside*y))
    def makebg(self):
        topBottom = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        center =    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
        for x in range(len(topBottom)):
            self.drawtile(self.tiles[topBottom[x]], x, 0)
            self.drawtile(self.tiles[topBottom[x]], x, 19)
        for y in range(1, 19):
            for x in range(len(center)):
                self.drawtile(self.tiles[center[x]], x, y)

class Fruit(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect().move(x * Ground.tileside, y * Ground.tileside)

    def update(self):
        self.rect.move_ip(0, 1)

class Score(pg.sprite.Sprite):
    """ to keep track of the score.
    """

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 32)
        self.font.set_italic(1)
        self.color = pg.Color("red")
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(400, 1)

    def update(self):
        """ We only update the score in update() when it has changed.
        """
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)

class Body(pg.sprite.Sprite):
    def __init__(self, x, y, dirx, diry):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect().move(x * Ground.tileside, y * Ground.tileside)
        self.dirx = dirx
        self.diry = diry

    def update(self):
        self.rect.move_ip(self.dirx * Snake.speed, self.diry * Snake.speed)

class Snake(pg.sprite.Sprite):
    speed = 2
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[img]
        self.rect = self.image.get_rect().move(x * Ground.tileside, y * Ground.tileside)
        self.dirx = 0
        self.diry = 1
        self.key = img
       
    def move(self, dx, dy):
        if (self.key != 1):
            return False
        if (self.dirx - dx) == 0:
            return False
        if (self.diry - dy) == 0:
            return False
        if (dx == dy):
            return False
        self.dirx = dx
        self.diry = dy
        return True

    def update(self):
        self.rect.move_ip(self.dirx * Snake.speed, self.diry * Snake.speed)
        print("snake update ", self.rect.left / Ground.tileside, self.rect.top / Ground.tileside)
    

def main():
    # Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    # set the display mode
    winstyle = 0 # | FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    # load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    spritesheet = SpriteSheet('sprites.png')

    Ground.tiles = spritesheet.imgsat([(96,0 , 32,32 ), # light
                                        (64, 0, 32, 32)]) #dark

    Fruit.image = spritesheet.imgat((32, 0, 32, 32))
    Snake.images = spritesheet.imgsat([(0, 0, 32, 32), # body
                                        (128, 0, 32, 32)]) # head

    # decorate the game window
    pg.display.set_caption('Snake')

    # create the background
    ground = Ground()
    screen.blit(ground.background, (0, 0))
    pg.display.flip()

    fruits = pg.sprite.Group()
    snakes = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()

    Fruit.containers = all, fruits
    Score.containers = all
    Snake.containers = all, snakes

    clock = pg.time.Clock()
    Fruit(10, 1)
    snake = Snake(15, 10, 1)
    Snake(15, 9, 0)
    Snake(15, 8, 0) 
    Snake(15, 7, 0)
    

    global SCORE
    if pg.font:
        all.add(Score())

    while 1:

        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return
        keystate = pg.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, ground.background)

        # update all the sprites
        all.update()

        dirx = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        diry = keystate[pg.K_DOWN] - keystate[pg.K_UP]
        snake.move(dirx, diry)

        # draw the scene
        dirty = all.draw(screen)
        pg.display.update(dirty)

        # cap the framerate
        clock.tick(30)

    if pg.mixer:
        pg.mixer.music.fadeout(1000)
    pg.time.wait(1000)
    pg.quit()

# call the "main" function if running this script
if __name__ == "__main__":
    main()