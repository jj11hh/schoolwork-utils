# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import sys

import genes

black= 0,0,0
white=255,255,255
font_file="wqy-mono.ttf"

class Statu_area():
    def __init__(self):
        self.surf=pygame.Surface((600,100))
        self.rect=self.surf.get_rect()
        self.rect.topleft=(0,0)
        self.image=self.surf
        self.font=pygame.font.Font(font_file,32)
        self.updated=True
    def set_text(self,text):
        text_surf=self.font.render(text,True,white)
        self.surf.fill(black)
        self.surf.blit(text_surf,text_surf.get_rect())
        self.updated=True
        
class Record_area():
    def __init__(self,listofitem):
        self.surf=pygame.Surface((300,600))
        self.rect=self.surf.get_rect()
        self.rect.topleft=(600,0)
        self.image=self.surf
        self.count=len(listofitem)
        self.font=pygame.font.Font(font_file,32)
        if self.count:
            self.char_height=self.rect.height/self.count
        self.items=listofitem
        self.records=dict([(item,0) for item in listofitem])
        self.updated=True

        i=0
        for item in self.items:
            _surf=self.font.render(item+":"+str(self.records[item]),True,white)
            _rect=_surf.get_rect().move([0,i*self.char_height])
            self.surf.blit(_surf,_rect)
            i+=1

    def inc_item(self,item):
        self.records[item]+=1
        offset=self.items.index(item)
        _surf=self.font.render(item+":"+str(self.records[item]),True,white)
        _rect=_surf.get_rect().move([0,offset*self.char_height])
        _mask=_surf.copy()
        _mask.fill(black)
        self.surf.blit(_mask,_rect)
        self.surf.blit(_surf,_rect)
        self.updated=True

    def update(self):
        pass
class Gamete(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.target=(0,0)
        self.speed=[0,0]
        self.ttl=0
        self.font=pygame.font.Font(font_file,50)
        self.text=""
        self.text_surf=self.font.render(self.text,True,white)
        self.image.blit(self.text_surf,self.text_surf.get_rect().move((10,10)))
        self.before=True
        self.hover=False
        
    def update(self):

        if self.is_stop() and self.hover:
            self.when_hover()
            return
        if self.is_stop():return
        
        self.d=(self.target[0]-self.rect.centerx,self.target[1]-self.rect.centery)
        self.speed=[self.d[0]/self.ttl,self.d[1]/self.ttl]
        self.ttl-=1
        self.rect.move_ip(self.speed)
    def is_stop(self):
        if self.ttl==0:return True
        else:return False
    def set_text(self,text):
        self.text=text
        self.text_surf=self.font.render(self.text,True,white)
        self.image=self.firstimage.copy()
        self.image.blit(self.text_surf,self.text_surf.get_rect().move((10,10)))

    def when_hover(self):
        pass

    def move_to_target(self,callback=0,ttl=240):
        self.ttl=ttl
        self.before=False
        self.hover=True
        if callback:self.when_hover=callback

class Sperm(Gamete):
    def __init__(self):
        
        self.firstimage=pygame.image.load("sperm.png").convert_alpha()
        self.image=self.firstimage.copy()
        self.rect=self.image.get_rect()
        Gamete.__init__(self)

class Egg(Gamete):
    def __init__(self):
        self.firstimage=pygame.image.load("egg.png").convert_alpha()
        self.image=self.firstimage.copy()
        self.rect=self.image.get_rect()
        Gamete.__init__(self)

class Zygote(Gamete):
    def __init__(self):
        self.firstimage=pygame.image.load("zygote.png").convert_alpha()
        self.image=self.firstimage.copy()
        self.rect=self.image.get_rect()
        Gamete.__init__(self)
        
    def update(self):
        pass

class Demo():
    def __init__(self,records):
        if len(records)==0:
            raise ValueError
        pygame.init()

        self.screen = pygame.display.set_mode((800,600),0,32)
        pygame.display.set_caption("演示窗口")

        self.sperm=Sperm()
        self.egg=Egg()
        self.zygote=Zygote()
        self.zygote.rect.center=self.zygote.target=400,500

        self.records=records
        self.listofp=genes.make_p(records[0][0])
        self.all_children=genes.make_all_children(self.listofp)

        self.record_area=Record_area(self.all_children)
        
        self.statu_area=Statu_area()

        self.all_sprites=[self.zygote,self.egg,self.sperm]


        self.clock=pygame.time.Clock()

        self.index=0
        self.running=True
        self.animation_finished=True
        self.animation_ttl=300
        self.pause=False
        self.update_statu()

    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.running==False:
                    pygame.quit()
                    return
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == K_p: 
                        if self.pause!=True:
                            self.pause=True
                        else: self.pause=False
                        self.update_statu()
                    if event.key == K_PAGEUP and self.animation_ttl>0:
                        self.animation_ttl-=20
                        self.update_statu()
                    if event.key == K_PAGEDOWN and self.animation_ttl<300:
                        self.animation_ttl+=20
                        self.update_statu()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        return
            
            self.screen.fill(black)
            
            updates=[]
            
            if self.statu_area.updated or True:
                self.screen.blit(self.statu_area.image,self.statu_area.rect)
                updates.append(self.statu_area.rect)
                self.statu_area.updated=False
            
            if self.pause==False:
            
                for sprite in self.all_sprites:
                    rect_before=sprite.rect
                    sprite.update()
                    self.screen.blit(sprite.image,sprite.rect)
                    updates.append(rect_before)
                    updates.append(sprite.rect)
        
                if self.record_area.updated:
                    self.screen.blit(self.record_area.image,self.record_area.rect)
                    updates.append(self.record_area.rect)
                    self.record_area.updated=False

                if self.animation_finished==True and self.index<len(self.records):
                    self.show_record(self.records[self.index])

            pygame.display.update(updates)
        
    def update_statu(self):
        self.statu_text="Count:%d/%d|" % (self.index+1, len(self.records))
        self.statu_text+="Speed:%dFPL|" % self.animation_ttl
        if self.pause==True:
            self.statu_text+="Paused"
        self.statu_area.set_text(self.statu_text)
        self.statu_area.updated=True
    def show_record(self,record):
        self.animation_finished=False
        self.sperm.rect.center=100,200
        self.sperm.set_text(record[0])
        self.egg.rect.center=400,200
        self.egg.set_text(record[1])
        self.sperm.target=self.egg.target=400,500
        self.sperm.move_to_target(ttl=self.animation_ttl)
        self.egg.move_to_target(self.reset_pos,ttl=self.animation_ttl)
        
    def reset_pos(self):
        self.animation_finished=True
    
        self.all_sprites.append(self.zygote)

        self.zygote.rect.center=self.zygote.target=400,500
        print self.index
        self.zygote.set_text(self.records[self.index][2])
        self.record_area.inc_item(self.records[self.index][2])
        self.egg.hover=self.sperm.hover=False
        self.index+=1
        self.update_statu()



if __name__=="__main__":
    demo=Demo([("ab","AB","AaBb"),("aB","AB","AaBB")])
    demo.run()

