import pygame as pg

WIDTH = 1280
HEIGHT = 720
SIZE = [WIDTH, HEIGHT]
TITLE = "SH mini game"
FRAME = 120


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
        self.state = 2
        self.pressed_key = []
        self.lastkey = []
        self.usedkey = [pg.K_d, pg.K_f, pg.K_j, pg.K_k]
        self.speed = 10

        
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
        self.img_health_bar = pg.image.load("first_copy/image/img_health_bar.png")
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
        self.white_num = []
        self.black_num = []
        for i in range(10):
            self.white_num.append(pg.image.load("first_copy/image/n_w_{}.png".format(i)))
            self.black_num.append(pg.image.load("first_copy/image/n_b_{}.png".format(i)))
        self.new_song() #나중에 지우기

    def run(self):
        if self.state == 1: self.opening()
        elif self.state == 2: self.ingame()
        self.lastkey = []
        pg.display.update()

    def opening(self):
        if self.menu_state == 0: self.screen.blit(self.bg_menu[self.op_select], [0, 0])
        elif self.menu_state == 1: self.screen.blit(self.bg_ready[self.op_select], [0, 0])
        else: self.screen.blit(self.bg_instruction, [0, 0])
    
        if self.lastkey != []:
            if pg.K_LEFT in self.lastkey:
                self.op_select -= 1 if self.op_select != 0 else 0
            elif pg.K_RIGHT in self.lastkey:
                self.op_select += 1 if self.op_select != 2 else 0
            elif pg.K_SPACE in self.lastkey:
                if self.menu_state == 0: # when main
                    if self.op_select == 0: self.menu_state = 1 # main to ready
                    elif self.op_select == 1: self.menu_state = 2 # main to instruction
                elif self.menu_state == 1: # when ready
                    if self.op_select == 0: print("easy") # easy
                    elif self.op_select == 1: print("normal") # easy
                    else: print("hard") # easy
                    self.new_song()
                    self.state = 2 # goto ingame!

            elif pg.K_ESCAPE in self.lastkey:
                self.menu_state = 0
    
    def new_song(self):
        self.note_num = 0
        self.bpm = 128
        self.bps = 60 / self.bpm
        self.start_ticks = pg.time.get_ticks()
        self.temp_song = [[2.0, 1], [2.2, [1, 3]], [2.3, 2], [2.7, [0, 2]], [3.0, 1], [4.0, 1], [4.0, 1], [24.0, 3]] #timing, line
        self.next_note = self.temp_song[0]
        self.inscreen_note = [] #height, line
        self.last_score = 0
        self.score = 0
        self.life = 100
        
    def ingame(self):
        self.update()
        self.draw()
        
    def update(self):
        self.game_time = ((pg.time.get_ticks() - self.start_ticks) / 1000)
        self.game_beat = self.game_time / self.bps

        if self.next_note[0] <= self.game_time:
            if type(self.next_note[1]) == type([]):
                for i in range(len(self.next_note[1])):
                    self.inscreen_note.append([0, self.next_note[1][i]])
            else:
                self.inscreen_note.append([0, self.next_note[1]])
            self.note_num += 1
            self.next_note = self.temp_song[self.note_num]
        self.life -= 0.05 #난이도에 맞춰 속도 조절

    def draw(self):
        self.screen.blit(self.bg_ingame, [0, 0])
        self.screen.blit(self.img_notepad[0], [421, 598])
        self.screen.blit(self.img_health_bar, [860, 0])
        pg.draw.rect(self.screen, [255, 147, 30], [868, 8, (404 * self.life * 0.01), 32])
        temp = self.score
        for i in range(6):
            self.screen.blit(self.white_num[temp % 10], [1260-(i*25), 50])
            temp = temp // 10
        pg.rect.Rect
        for i in range(4):
            if self.usedkey[i] in self.pressed_key:
                self.screen.blit(self.img_pad_line, [420+(110*i), 0])
        if self.last_score != 0:
            self.screen.blit(self.img_score[self.last_score - 1], [515, 100])
        self.draw_note()

    def draw_note(self):
        delete_list = []
        for i, [h, line] in enumerate(self.inscreen_note):
            self.screen.blit(self.img_note[0 if line in[1, 2] else 1], [420+(110*line), h])
            if isin(self.inscreen_note[i][0], 500, 670) and self.usedkey[line] in self.lastkey:
                delete_list.append(i)
                if isin(h, 610, 650): a, b = 1, 4
                elif isin(h, 575, 660): a, b = 2, 2
                elif isin(h, 525, 670): a, b = 3, 1
                self.last_score = a
                self.score += int(100 - abs(625 - h))
                self.life += b
                if self.life > 100: self.life = 100

            elif self.inscreen_note[i][0] <= 720: 
                self.inscreen_note[i][0] += self.speed
            else: 
                delete_list.append(i)
                self.life -= 5
        for i in reversed(delete_list):
            self.inscreen_note.pop(i)
        
g = set()
while g.running:
    g.clock.tick(FRAME)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            g.running = False
        if event.type == pg.KEYDOWN:
            g.pressed_key.append(event.key)
            g.lastkey.append(event.key)
        if event.type == pg.KEYUP:
            g.pressed_key.remove(event.key)

    g.run()


#할일
# 콤보 만들기
# 점수 구현
# 맞출 경우 효과
# 목숨 만들기
