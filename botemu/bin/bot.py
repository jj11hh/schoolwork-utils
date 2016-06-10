#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from math import pi, sin, cos, sqrt
from config import *

class Bot(object):
    def __init__(self, screen, color, pos):
        self.botimage = pygame.image.load(BOTIMAGE).convert_alpha()
        self.botimage_scaled = pygame.transform.scale(self.botimage, BOTAREA[1])
        self.botsurf = self.botimage.copy()
        self.botsize = self.botsurf.get_size()
        self.botrect = self.botimage.get_rect()
        size = self.botsize
        self.surf = pygame.Surface((int(size[0] * sqrt(2)), int(size[1] * sqrt(2))), flags = SRCALPHA)
        self.rect = self.surf.get_rect()
        self.rect.center = pos
        self.bgcolor = color
        self.surf.fill(self.bgcolor)
        self.realposx = float(pos[0])
        self.realposy = float(pos[1])
        self.botrect.center = (self.rect.width / 2, self.rect.height / 2)
        self.surf.blit(self.botsurf, self.botrect)
        self.scr = screen
        self.scr_rect = screen.get_rect()
        self.scr_size = self.scr.get_size()
        (self.scr_width, self.scr_height) = self.scr.get_size()
        self.direct = 0.0
        self.motos = [0.0, 0.0]
        self.paused = False
        self.snapshot = self.get_snapshot()

    
    def get_snapshot(self):
        _botrect = self.rect
        if self.rect.top < 0:
            _botrect.top = 0
        if self.rect.left < 0:
            _botrect.left = 0
        if self.rect.right > self.scr.get_rect().width:
            _botrect.right = self.scr.get_rect().width
        if self.rect.bottom > self.scr.get_rect().height:
            _botrect.bottom = self.scr.get_rect().height
        _botarea = pygame.transform.scale(self.scr.subsurface(self.rect), tuple(map(lambda x: int(x * sqrt(2)), BOTAREA[1])))
        _botarea = pygame.transform.rotate(_botarea, -(self.direct) / (2.0 * pi) * 360.0)
        _botrect = self.botrect.copy()
        _botrect.width = BOTAREA[1][0]
        _botrect.height = BOTAREA[1][1]
        _botrect.center = map(lambda x: x / 2, (_botarea.get_rect().width, _botarea.get_rect().height))
        _botarea = _botarea.subsurface(_botrect)
        _botarea.blit(self.botimage_scaled, self.botimage_scaled.get_rect())
        return _botarea

    
    def get_sensor(self, n):
        if not 0 <= n < 7:
            raise IndexError
        sensor_point = SENSOR_POINTS[n]
        return self.snapshot.get_at(sensor_point) == (0, 0, 0, 255)

    
    def set_moto(self, motonum, val):
        self.motos[motonum] = val

    
    def speed_inc(self, n, val):
        self.motos[n] += val

    
    def pause(self):
        self.paused = not (self.paused)

    
    def stop(self):
        self.motos[0] = 0
        self.motos[1] = 0

    
    def info(self):
        return "moto#0:%f|moto#1:%f%s" % (self.motos[0], self.motos[1], '|paused' if self.paused else '')

    
    def update(self):
        if not self.paused:
            speed = (-self.motos[0] + -self.motos[1]) / 2.0
            deltaspeed = self.motos[1] - self.motos[0]
            angv = float(deltaspeed) / float(self.botsize[0])
            self.direct += angv
            if self.direct > 2 * pi:
                self.direct %= 2 * pi
            elif self.direct < 0:
                self.direct += 2 * pi
            self.botsurf = pygame.transform.rotate(self.botimage, self.direct /(2 * pi)*360)
            self.botrect = self.botsurf.get_rect()
            self.botrect.center = (self.rect.width / 2, self.rect.height / 2)
            self.surf.fill(self.bgcolor)
            self.surf.blit(self.botsurf, self.botrect)
            ang = -(self.direct) + pi / 2
            v = (cos(ang) * speed, sin(ang) * speed)
            self.realposx += v[0]
            self.realposy += v[1]
            if self.realposx < self.rect.width / 2:
                self.realposx += self.scr_width - self.rect.width
            if self.realposx > self.scr_width - self.rect.width / 2:
                self.realposx -= self.scr_width - self.rect.width
            if self.realposy > self.scr_height - self.rect.height / 2:
                self.realposy -= self.scr_height - self.rect.height
            if self.realposy < self.rect.height / 2:
                self.realposy += self.scr_height - self.rect.height
            self.snapshot = self.get_snapshot()
        self.rect.center = (int(self.realposx), int(self.realposy))


if __name__ == '__main__':
    App().run()
    exit(0)
 
