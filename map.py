#! /usr/bin/env python

from __future__ import division, print_function, unicode_literals

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyglet.gl import *
from pyglet.window import key

from cocos.actions import *
from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite


class SpriteLayer(Layer):

    is_event_handler = True     #: enable pyglet's events

    def __init__(self, index=1):
        super(SpriteLayer, self).__init__()
        self.index = index

        self.image = pyglet.resource.image('grossini.png')
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        self.image_sister1 = pyglet.resource.image('grossinis_sister1.png')
        self.image_sister1.anchor_x = self.image_sister1.width // 2
        self.image_sister1.anchor_y = self.image_sister1.height // 2

        self.image_sister2 = pyglet.resource.image('grossinis_sister2.png')
        self.image_sister2.anchor_x = self.image_sister2.width // 2
        self.image_sister2.anchor_y = self.image_sister2.height // 2

    def on_key_release(self, keys, mod):
        # LEFT: go to previous scene
        # RIGTH: go to next scene
        # ENTER: restart scene
        if keys == key.LEFT:
            self.index -= 1
            if self.index < 1:
                self.index = len(tests)
        elif keys == key.RIGHT:
            self.index += 1
            if self.index > len(tests):
                self.index = 1

        if keys in (key.LEFT, key.RIGHT, key.ENTER):
            director.replace(get_sprite_test(self.index))
            return True

    # def on_exit( self ):
    #    for o in self.objects:
    #        o.stop()


class SpriteMoveTo(SpriteLayer):

    def on_enter(self):
        super(SpriteMoveTo, self).on_enter()

        sprite3 = Sprite(self.image)
        self.add(sprite3)
        sprite3.position = 320, 300
        sprite3.do(MoveTo((620, 300), 4))


if __name__ == "__main__":
    director.init(resizable=True, caption='Cocos - Sprite demo')
#    director.window.set_fullscreen(True)
    director.run(Scene(SpriteMoveTo(1)))
