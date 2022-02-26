import pygame
import os
import random

pygame.font.init()

SIRKA, VYSKA = 1920, 1080
PLOCHA = pygame.display.set_mode((SIRKA, VYSKA))

pygame.display.set_caption("StarShip")

pozadie = pygame.transform.scale(pygame.image.load(os.path.join("pictures", "pozadie_.png")), (SIRKA, VYSKA))

zlta_lod = pygame.image.load(os.path.join("pictures", "zlta_lod.png"))
laser_zlty = pygame.image.load(os.path.join("pictures", "laser_zlty.png"))

zelena_lod = pygame.image.load(os.path.join("pictures", "zelena_lod.png"))
cervena_lod = pygame.image.load(os.path.join("pictures", "cervena_lod.png"))
modra_lod = pygame.image.load(os.path.join("pictures", "modra_lod.png"))
oranzova_lod = pygame.image.load(os.path.join("pictures", "oranzova_lod.png"))
fialova_lod = pygame.image.load(os.path.join("pictures", "fialova_lod.png"))
ruzova_lod = pygame.image.load(os.path.join("pictures", "ruzova_lod.png"))
boss_lod = pygame.image.load(os.path.join("pictures", "boss_lod.png"))

laser_zeleny = pygame.image.load(os.path.join("pictures", "laser_zeleny.png"))
laser_cerveny = pygame.image.load(os.path.join("pictures", "laser_cerveny.png"))
laser_modry = pygame.image.load(os.path.join("pictures", "laser_modry.png"))
laser_oranzovy = pygame.image.load(os.path.join("pictures", "laser_oranzovy.png"))
laser_fialovy = pygame.image.load(os.path.join("pictures", "laser_fialovy.png"))
laser_ruzovy = pygame.image.load(os.path.join("pictures", "laser_ruzovy.png"))
laser_boss = pygame.image.load(os.path.join("pictures", "laser_boss.png"))


class Lod:
    COOLDOWN = 25

    def __init__(self, x, y, vydrz=100):
        self.x = x
        self.y = y
        self.vydrz = vydrz
        self.lod_obr = None
        self.laser_obr = None
        self.lasery = []
        self.cool_down_pocitadlo = 0

    def zobrazit(self, okno):
        okno.blit(self.lod_obr, (self.x, self.y))

        for laser in self.lasery:
            laser.zobrazit(okno)

    def pohyb_laserov(self, rychlost, obj):
        self.cooldown()

        for laser in self.lasery:
            laser.pohyb(rychlost)

            if laser.mimo_obr(VYSKA):
                self.lasery.remove(laser)

            elif laser.kolizia(obj):
                obj.vydrz -= 10
                self.lasery.remove(laser)

    def strielat(self):
        if self.cool_down_pocitadlo == 0:
            laser = Laser(self.x, self.y, self.laser_obr)
            self.lasery.append(laser)
            self.cool_down_pocitadlo = 1

    def cooldown(self):
        if self.cool_down_pocitadlo >= self.COOLDOWN:
            self.cool_down_pocitadlo = 0

        elif self.cool_down_pocitadlo > 0:
            self.cool_down_pocitadlo += 1

    def get_height(self):
        return self.lod_obr.get_height()

    def get_width(self):
        return self.lod_obr.get_width()


class Boss_Lod:
    COOLDOWN = 25

    def __init__(self, x, y, vydrz=100):
        self.x = x
        self.y = y
        self.vydrz = vydrz
        self.lod_obr = None
        self.laser_obr = None
        self.lasery = []
        self.cool_down_pocitadlo = 0

    def zobrazit(self, okno):
        okno.blit(self.lod_obr, (self.x, self.y))

        for laser in self.lasery:
            laser.zobrazit(okno)

    def pohyb_laserov(self, rychlost, obj):
        self.cooldown()

        for laser in self.lasery:
            laser.pohyb(rychlost)

            if laser.mimo_obr(VYSKA):
                self.lasery.remove(laser)

            elif laser.kolizia(obj):
                obj.vydrz -= 25
                self.lasery.remove(laser)

    def strielat(self):
        if self.cool_down_pocitadlo == 0:
            laser = Laser(self.x, self.y, self.laser_obr)
            self.lasery.append(laser)
            self.cool_down_pocitadlo = 1

    def cooldown(self):
        if self.cool_down_pocitadlo >= self.COOLDOWN:
            self.cool_down_pocitadlo = 0

        elif self.cool_down_pocitadlo > 0:
            self.cool_down_pocitadlo += 1

    def get_height(self):
        return self.lod_obr.get_height()

    def get_width(self):
        return self.lod_obr.get_width()


class Hrac(Lod):
    def __init__(self, x, y, vydrz=100):
        super().__init__(x, y, vydrz)
        self.lod_obr = zlta_lod
        self.laser_obr = laser_zlty
        self.mask = pygame.mask.from_surface(self.lod_obr)
        self.max_vydrz = vydrz

    def zobrazit(self, okno):
        super().zobrazit(okno)
        self.vydrz_lista(okno)

    def pohyb_laserov(self, rychlost, objekty):
        self.cooldown()

        for laser in self.lasery:
            laser.pohyb(rychlost)

            if laser.mimo_obr(VYSKA):
                self.lasery.remove(laser)

            else:
                for obj in objekty:
                    if laser.kolizia(obj):
                        objekty.remove(obj)

                        if laser in self.lasery:
                            self.lasery.remove(laser)

    def vydrz_lista(self, okno):
        pygame.draw.rect(okno, (255, 0, 0), (self.x, self.y + self.lod_obr.get_height() + 10,
                                             self.lod_obr.get_width(), 10))
        pygame.draw.rect(okno, (0, 255, 0), (self.x, self.y + self.lod_obr.get_height() + 10,
                                             self.lod_obr.get_width() * (self.vydrz / self.max_vydrz), 10))


class Nepriatel(Lod):
    ZADELENIE = {
        'zelena': (zelena_lod, laser_zeleny),
        'cervena': (cervena_lod, laser_cerveny),
        'modra': (modra_lod, laser_modry),
        'oranzova': (oranzova_lod, laser_oranzovy),
        'fialova': (fialova_lod, laser_fialovy),
        'ruzova': (ruzova_lod, laser_ruzovy)
    }

    def __init__(self, x, y, farba, vydrz=100):
        super().__init__(x, y, vydrz)
        self.lod_obr, self.laser_obr = self.ZADELENIE[farba]
        self.mask = pygame.mask.from_surface(self.lod_obr)

    def pohyb(self, rychlost):
        self.y += rychlost

    def strielat(self):
        if self.cool_down_pocitadlo == 0:
            laser = Laser(self.x - 20, self.y, self.laser_obr)
            self.lasery.append(laser)
            self.cool_down_pocitadlo = 1


class Boss(Boss_Lod):
    def __init__(self, x, y, vydrz=100):
        super().__init__(x, y, vydrz)
        self.lod_obr = boss_lod
        self.laser_obr = laser_boss
        self.mask = pygame.mask.from_surface(self.lod_obr)
        self.max_vydrz = vydrz

    def pohyb(self, rychlost):
        self.y += rychlost

    def strielat(self):
        if self.cool_down_pocitadlo == 0:
            laser = Laser(self.x, self.y+85, self.laser_obr)
            self.lasery.append(laser)
            self.cool_down_pocitadlo = 1


class Laser:
    def __init__(self, x, y, obr):
        self.x = x
        self.y = y
        self.obr = obr
        self.mask = pygame.mask.from_surface(self.obr)

    def zobrazit(self, okno):
        okno.blit(self.obr, (self.x, self.y))

    def pohyb(self, rychlost):
        self.y += rychlost

    def kolizia(self, obj):
        return zrazenie(self, obj)

    def mimo_obr(self, vyska):
        return not (vyska >= self.y >= - 30)


def zrazenie(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def zaklad():
    spustit = True
    FPS = 60

    zivoty = 10
    level = 0

    score = 0
    score_bonus = 0

    hlavne_pismo = pygame.font.SysFont('Verdana', 30)
    konecne_pismo = pygame.font.SysFont('Verdana', 50)

    rychlost_hraca = 10
    rychlost_laseru = 12

    nepriatelia = []
    nepriatelia_boss = []
    pocet_nepriatelov = 5
    rychlost_nepriatela = 1
    rychlost_bossa = 1
    rychlost_laseru_bossa = 25
    pocet_bossov = 0

    hrac = Hrac(960, 850)  # suradnice zobrazenia mojej lode

    clock = pygame.time.Clock()

    pocitadlo_znicenia = 0
    zniceny = False

    def prekresli_okno():
        PLOCHA.blit(pozadie, (0, 0))

        zobraz_zivoty = hlavne_pismo.render(f"Zivoty: {zivoty}", 1, (255, 255, 255))
        PLOCHA.blit(zobraz_zivoty, (10, 10))

        zobraz_level = hlavne_pismo.render(f"Level: {level}", 1, (255, 255, 255))
        PLOCHA.blit(zobraz_level, (SIRKA - zobraz_level.get_width() - 10, 60))

        zobraz_score = hlavne_pismo.render(f"Score: {score}", 1, (255, 255, 255))
        PLOCHA.blit(zobraz_score, (SIRKA - zobraz_score.get_width() - 10, 10))

        for nepriatel in nepriatelia:
            nepriatel.zobrazit(PLOCHA)

        for boss in nepriatelia_boss:
            boss.zobrazit(PLOCHA)

        if zniceny:
            zobraz_prehru = konecne_pismo.render("Prehral si", 1, (255, 255, 255))
            PLOCHA.blit(zobraz_prehru, (SIRKA / 2 - zobraz_prehru.get_width() / 2, 250))

            zobraz_level = konecne_pismo.render(f"Skoncil si na {level} leveli.", 1, (255, 255, 255))
            PLOCHA.blit(zobraz_level, (SIRKA / 2 - zobraz_level.get_width() / 2, 425))

            zobraz_score = konecne_pismo.render(f"Tvoje skore je {score}", 1, (255, 255, 255))
            PLOCHA.blit(zobraz_score, (SIRKA / 2 - zobraz_score.get_width() / 2, 500))

        hrac.zobrazit(PLOCHA)

        pygame.display.update()

    while spustit:
        clock.tick(FPS)
        prekresli_okno()

        if zivoty <= 0 or hrac.vydrz <= 0:
            zniceny = True
            pocitadlo_znicenia += 1

        if zniceny:
            if pocitadlo_znicenia > FPS * 4:
                spustit = False

            else:
                continue

        klavesy = pygame.key.get_pressed()

        if klavesy[pygame.K_a] and hrac.x - rychlost_hraca > 0:
            hrac.x -= rychlost_hraca

        if klavesy[pygame.K_d] and hrac.x + rychlost_hraca + hrac.get_width() < SIRKA:
            hrac.x += rychlost_hraca

        if klavesy[pygame.K_w] and hrac.y - rychlost_hraca > - 40:
            hrac.y -= rychlost_hraca

        if klavesy[pygame.K_s] and hrac.y + rychlost_hraca + hrac.get_height() < VYSKA:
            hrac.y += rychlost_hraca

        if klavesy[pygame.K_SPACE]:
            hrac.strielat()

        if len(nepriatelia) == 0:
            pocet_nepriatelov += 5
            level += 1

            while 1 < level <= 5:
                score_bonus += 15
                score += 300 + score_bonus * 2
                break

            while 5 < level <= 10:
                score_bonus += 150
                score += 300 + score_bonus * 4
                break

            while 10 < level <= 15:
                score_bonus += 1500
                score += 600 + (score_bonus * 4) * 2
                break

            while level > 15:
                score_bonus += 15000
                score += score + ((score_bonus * 4) * 2) * 2
                break

            for i in range(pocet_nepriatelov):
                nepriatel = Nepriatel(random.randrange(200, SIRKA - 200), random.randrange(- 1200, - 100),
                                      random.choice(['zelena', 'cervena', 'modra', 'oranzova', 'fialova', 'ruzova']))
                nepriatelia.append(nepriatel)

            if int(level) == 5:
                pocet_bossov += 1
                for i in range(pocet_bossov):
                    boss = Boss(random.randrange(200, SIRKA - 200), random.randrange(- 1600, - 1400))
                    nepriatelia_boss.append(boss)

            if int(level) == 10:
                pocet_bossov += 1
                for i in range(pocet_bossov):
                    boss = Boss(random.randrange(200, SIRKA - 200), random.randrange(- 1600, - 1400))
                    nepriatelia_boss.append(boss)

            if int(level) == 15:
                pocet_bossov += 2
                for i in range(pocet_bossov):
                    boss = Boss(random.randrange(200, SIRKA - 200), random.randrange(- 1600, - 1400))
                    nepriatelia_boss.append(boss)

            if int(level) == 20:
                pocet_bossov += 4
                for i in range(pocet_bossov):
                    boss = Boss(random.randrange(200, SIRKA - 200), random.randrange(- 1600, - 1400))
                    nepriatelia_boss.append(boss)

            if int(level) > 20:
                pocet_bossov += 2
                for i in range(pocet_bossov):
                    boss = Boss(random.randrange(200, SIRKA - 200), random.randrange(- 1600, - 1400))
                    nepriatelia_boss.append(boss)

        for nepriatel in nepriatelia[:]:
            nepriatel.pohyb(rychlost_nepriatela)
            nepriatel.pohyb_laserov(rychlost_laseru, hrac)

            if random.randrange(0, 2 * 60) == 1:
                nepriatel.strielat()

            if zrazenie(nepriatel, hrac):
                hrac.vydrz -= 10
                nepriatelia.remove(nepriatel)

            elif nepriatel.y + nepriatel.get_height() > VYSKA:
                zivoty -= 1
                nepriatelia.remove(nepriatel)

        for boss in nepriatelia_boss[:]:
            boss.pohyb(rychlost_bossa)
            boss.pohyb_laserov(rychlost_laseru_bossa, hrac)
        
            if random.randrange(0, 10) == 1:
                boss.strielat()
    
            if zrazenie(boss, hrac):
                hrac.vydrz -= 10
    
            elif boss.y + boss.get_height() > VYSKA:
                zivoty -= 5
                nepriatelia_boss.remove(boss)

        hrac.pohyb_laserov(-rychlost_laseru, nepriatelia)
        hrac.pohyb_laserov(0, nepriatelia_boss)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


def hlavne_menu():
    spustit = True
    nadpisove_pismo = pygame.font.SysFont('Verdana', 60)

    while spustit:
        PLOCHA.blit(pozadie, (0, 0))
        zobraz_nadpis = nadpisove_pismo.render("Stlac tlacidlo na mysi pre pokracovanie", 1, (255, 255, 255))
        PLOCHA.blit(zobraz_nadpis, (SIRKA / 2 - zobraz_nadpis.get_width() / 2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spustit = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                zaklad()

    pygame.quit()


hlavne_menu()

