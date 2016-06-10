# -*- coding: utf-8 -*-

import thread
from sys import exit
from math import pi,sqrt

import pygame
from pygame.locals import *
import bot
import cli

from config import *

class App(object):
    def __init__(self,fontfile=FONT_FILE,fontsize=FONT_SIZE,\
                 botcolor=BOTCOLOR,\
                 botpos=BOTPOS, bgimage=BGIMAGE, bgcolor=BGCOLOR,\
                 icon=ICON, winsize=WINSIZE):

        self.caption = 'Botemu -- Created By Jiang'

        pygame.init()

        self.fpsclock=pygame.time.Clock()

        self.font=pygame.font.Font(fontfile, fontsize)

        self.screen = pygame.display.set_mode(winsize,0,32)
        self.bgcolor = bgcolor
        self.bgimage = pygame.image.load(bgimage).convert_alpha()

        self.botmap = self.screen.subsurface(pygame.Rect(BOTMAP))
        self.botmap.fill(self.bgcolor)
        self.botmap.blit(self.bgimage,self.bgimage.get_rect())

        self.bot=bot.Bot(self.botmap,botcolor,botpos)

        self.bot.update()
        self.botmap.blit(self.bot.surf,self.bot.rect)

        _botrect = self.bot.rect
        self.botarea = self.screen.subsurface(pygame.Rect(BOTAREA))

        _botarea = self.bot.snapshot
        self.botarea.blit(_botarea,_botarea.get_rect())

        pygame.display.set_caption(self.caption)

        if icon:
            pygame.display.set_icon(pygame.image.load(icon))

        self.paused = False
        pygame.display.flip()

        self.keyhandlers={
        K_p : self.pause,
        K_ESCAPE:lambda:pygame.event.post(pygame.event.Event(pygame.QUIT)),
        K_s : self.bot.stop,
        K_j : lambda:self.bot.speed_inc(0, 0.1),
        K_k : lambda:self.bot.speed_inc(1, 0.1),
        K_n : lambda:self.bot.speed_inc(0,-0.1),
        K_m : lambda:self.bot.speed_inc(1,-0.1),
        }

    def pause(self):
        self.bot.paused = not self.bot.paused

    def run(self):
        while True:
            self.fpsclock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                    return

                if event.type == pygame.KEYDOWN:
                    handler = self.keyhandlers.get(event.key)
                    if callable(handler):handler()

            self.botmap.fill(self.bgcolor)
            self.botmap.blit(self.bgimage,self.bgimage.get_rect())

            _botarea = self.bot.snapshot
            self.botarea.blit(_botarea,_botarea.get_rect())

            self.bot.update()
            self.botmap.blit(self.bot.surf,self.bot.rect)

            fontsurf=self.font.render(self.bot.info(),True,(0,0,0))
            fontrect=fontsurf.get_rect()
            self.screen.blit(fontsurf,fontrect)

            pygame.display.update()

            fps = self.fpsclock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pygame.display.set_caption(with_fps)

    def start(self):
        cmd = cli.Cli(self)
        thread.start_new_thread(cmd.cmdloop,())
        self.run()

if __name__ == "__main__":
    app=App()
    app.run()

