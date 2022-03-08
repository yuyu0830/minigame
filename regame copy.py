import pygame as pg

WIDTH = 1280
HEIGHT = 720
SIZE = [WIDTH, HEIGHT]
TITLE = "SH mini game"
FRAME = 50

def isin(v, a, b):
    if v > a and v < b: return True
    return False

class set():
    # 초기화 및 변수 지정    
    def __init__(self):
        # 스크린 설정
        self.screen = pg.display.set_mode(SIZE)
        self.title = pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        # 오프닝 변수
        self.menu_state = 0 #main, ready, instruction
        self.op_select = 0

        # 인게임 변수
        self.running = True
        self.state = 1 
        self.pressed_key = []
        self.lastkey = 0
        
        # start_버튼 이미지
        # self.start_load = pg.image.load("first_copy/image/start_load.png")
        # self.start_msg = pg.image.load("first_copy/image/start_msg.png")
        self.bg_ingame = pg.image.load("first_copy/image/ingame_screen.png")
        self.bg_instruction = pg.image.load("first_copy/image/instruction.png")
        self.bg_gameover = [] # Yes, No
        self.bg_gameover.append(pg.image.load("first_copy/image/game_over_screen_yes.png"))
        self.bg_gameover.append(pg.image.load("first_copy/image/game_over_screen_no.png"))
        self.bg_ready = [] # Nor, Eas, Har
        self.bg_ready.append(pg.image.load("first_copy/image/ready_screen_easy.png"))
        self.bg_ready.append(pg.image.load("first_copy/image/ready_screen_nomal.png"))
        self.bg_ready.append(pg.image.load("first_copy/image/ready_screen_hard.png"))
        self.bg_menu = [] # Str, Dis, Exi
        self.bg_menu.append(pg.image.load("first_copy/image/background1.png"))
        self.bg_menu.append(pg.image.load("first_copy/image/background0.png")) 
        self.bg_menu.append(pg.image.load("first_copy/image/background2.png"))

        self.img_pad_line = pg.image.load("first_copy/image/pad_line.png")
        self.img_red_line = pg.image.load("first_copy/image/red_line.png")
        self.img_notepad = [] # No, Ce, Sd
        self.img_notepad.append(pg.image.load("first_copy/image/note_pad.png"))
        self.img_notepad.append(pg.image.load("first_copy/image/nomal_note_pad.png"))
        self.img_notepad.append(pg.image.load("first_copy/image/side_note_pad.png"))
        self.img_note = [] # Ce, Sd
        self.img_note.append(pg.image.load("first_copy/image/nomal_note.png"))
        self.img_note.append(pg.image.load("first_copy/image/side_note.png"))
        self.img_score = [] # Ex, Gd, Bd
        self.img_score.append(pg.image.load("first_copy/image/Exerlent.png"))
        self.img_score.append(pg.image.load("first_copy/image/good.png"))
        self.img_score.append(pg.image.load("first_copy/image/bad.png"))
        self.img_mani = [] # C, L, R
        self.img_mani.append(pg.image.load("first_copy/image/menu1.png"))
        self.img_mani.append(pg.image.load("first_copy/image/menu0.png"))
        self.img_mani.append(pg.image.load("first_copy/image/menu2.png")) 

    def run(self):
        if self.state == 1: self.opening()
        elif self.state == 2: self.ingame()
        self.lastkey = 0
        pg.display.update()

    def opening(self):
        if self.menu_state == 0: self.screen.blit(self.bg_menu[self.op_select], [0, 0])
        elif self.menu_state == 1: self.screen.blit(self.bg_ready[self.op_select], [0, 0])
        else: self.screen.blit(self.bg_instruction, [0, 0])
    
        if self.lastkey != 0:
            if self.lastkey == pg.K_LEFT:
                self.op_select -= 1 if self.op_select != 0 else 0
            elif self.lastkey == pg.K_RIGHT:
                self.op_select += 1 if self.op_select != 2 else 0
            elif self.lastkey == pg.K_SPACE:
                if self.menu_state == 0: # when main
                    if self.op_select == 0: self.menu_state = 1 # main to ready
                    elif self.op_select == 1: self.menu_state = 2 # main to instruction
                elif self.menu_state == 1: # when ready
                    if self.op_select == 0: print("easy") # easy
                    elif self.op_select == 1: print("normal") # easy
                    else: print("hard") # easy
                    self.state = 2 # goto ingame!

            elif self.lastkey == pg.K_ESCAPE:
                self.menu_state = 0
        
    def ingame(self):
        pass

g = set()
while g.running:
    g.clock.tick(FRAME)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            g.running = False
        if event.type == pg.KEYDOWN:
            g.pressed_key.append(event.key)
            g.lastkey = event.key
        if event.type == pg.KEYUP:
            g.pressed_key.remove(event.key)

    g.run()