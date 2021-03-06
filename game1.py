#! /usr/bin/env python

from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "t 0.1, s, q"
tags = "TMX, tiles, Driver"

import pyglet
from pyglet.window import key

pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()

import cocos
from cocos import tiles, actions, layer

  
def main():
    global keyboard, scroller
    from cocos.director import director
    director.init(width=960, height=640, autoscale=False, resizable=True)

    scroller = layer.ScrollingManager()
    test_layer = tiles.load('road-map.tmx')['map0']
    scroller.add(test_layer)

    main_scene = cocos.scene.Scene(scroller)
    

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    def on_key_press(key, modifier):
        if key == pyglet.window.key.Z:
            if scroller.scale == .75:
                scroller.do(actions.ScaleTo(1, 2))
            else:
                scroller.do(actions.ScaleTo(.75, 2))
        elif key == pyglet.window.key.D:
            test_layer.set_debug(True)
        
        
    director.window.push_handlers(on_key_press)

    director.run(main_scene)

if __name__ == '__main__':
    main()