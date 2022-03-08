import pygame
from pygame.constants import HIDDEN
from random import *
from class_get import *

class g1(var):
    def __init__(self, screen, screen_width, screen_height, state, click_pos):
        super().__init__(screen, screen_width, screen_height, state, click_pos)
        # 폰트
        self.game_font = pygame.font.Font(None, 120)
        self.level_font = pygame.font.Font(None, 80)

        # 색깔
        self.BLACK = (0, 0, 0) # RGB 검정색
        self.WHITE = (255, 255, 255) # RGB 흰색
        self.GRAY = (50, 50, 50)

        # 캐릭터
        self.character_1 = pygame.image.load("first_copy/image/character_1.png")

        # 총
        self.gun = pygame.image.load("first_copy/image/gun.png")
        self.border = 2 # 총 원 둘래 넓이

        # 스타트 버튼, 리스타트 글자 버튼
        self.start_button1 = pygame.image.load("first_copy/image/start_button1.png")
        self.re_msg = self.level_font.render("RESTART", True, self.WHITE)

        self.st_btn = get(self.start_button1)
        self.st_btn.center_pos((self.screen_width, self.screen_height))
        self.r = get(self.re_msg)
        self.re_msg_indi_center = self.r.individual_pos(self.screen_width - self.r.object_width , self.screen_height - (self.r.object_height * 2.5))

        self.start_button1_rect = self.start_button1.get_rect(center = (screen_width / 2, screen_height /2))
        self.re_msg_rect = self.re_msg.get_rect(center = self.re_msg_indi_center)
        
        # 변수
        self.curr_level = 1 # 현재 레벨
        self.display_time = None # 숫자를 보여주는 시간
        self.start_ticks = None # 시간 계산 (현재 시간 정보를 저장)
        
        # 프레임 변수
        self.clock = pygame.time.Clock()

        # 게임 시작 여부
        self.start1 = False
        # 숫자 숨김 여부 (사용자가 1을 클릭, 보여주는 시간 초과)
        self.hidden = False
        # 게임 오버 여부
        self.over = False
        # 현재 상황
        self.screen_state = 0 # 게임 시작 전, 1 = 게임중, 2 = 게임 오버

        # 이동할 좌표
        self.to_x = 0
        self.to_y = 0
        # 캐릭터 체력
        self.hp = 10
        # 캐릭터 속도
        self.character_speed = 0.3
        # 캐릭터 좌표
        self.character_x = 0
        self.character_y = 0
    
        print("g1 state: "+str(self.screen_state))
        self.setup(self.curr_level)
    
        # 루프 시작
        while self.state == 2:
            self.fps = self.clock.tick(30)
            self.click_pos = None
            # 이벤트 루프
            for event in pygame.event.get(): # 무슨 이벤트 발생?
                if event.type == pygame.QUIT: # 창이 닫히는 이벤트?
                    set.run = False # 게임이 더 이상 실행중이 아님
                elif event.type == pygame.MOUSEBUTTONUP: # 사용자가 마우스 클릭했을때
                    self.click_pos = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 1
                        print(event.key)
                    if event.key == pygame.K_w:
                        self.to_y += self.character_speed
                        print(event.key)
                    if event.key == pygame.K_s:
                        self.to_y -= self.character_speed
                    if event.key == pygame.K_a:
                        self.to_x += self.character_speed
                    if event.key == pygame.K_d:
                        self.to_x -= self.character_speed

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.to_y = 0
                    if event.key == pygame.K_s:
                        self.to_y = 0
                    if event.key == pygame.K_a:
                        self.to_x = 0
                    if event.key == pygame.K_d:
                        self.to_x = 0

            # 화면 전체를 까맣게 칠하기
            self.screen.fill(self.BLACK)

            if self.start1 == True:
                if self.screen_state == 1:# 게임 중
                    self.display_game_screen() # 게임화면 표시

            elif self.start1 == False: # 게임시작 여부가 False 일 때, 
                if self.over == True:
                    self.screen_state = 2 # 게임오버
                    self.game_over_screen() # 게임오버 화면 표시
                else:
                    self.screen_state = 0 # 게임 시작 전
                    self.hidden = False
                    self.display_start_screen() # 시작화면 표시
            

            # 사용자가 클릭한 좌표값이 있다면 (어딘가 클릭)
            if self.click_pos:
                self.check_buttons(self.click_pos)
                print("g1 start : "+str(self.start1)+", g1 state : "+ str(self.screen_state))

            # 화면 업데이트
            pygame.display.update()

    # 캐릭터 크리기
    def character_draw(self): 
        c = character(self.character_1)
        c.center_pos(self.screen_width, self.screen_height, self.character_x, self.character_y)
        c.character_blit(self.screen, self.character_1, c.screen_center_blit_pos)
       
        self.character_x += self.to_x * self.fps
        self.character_y += self.to_y * self.fps

    def gun_draw(self):
        g = gun_n_bullet(self.screen, self.click_pos, self.gun, self.character_1, (self.character_x, self.character_y))
        g.gun_frame_circle(self.border, self.WHITE)
        g.gun_shoot() # 총 그리기 로직
        g.gun_draw(self.screen, self.gun)

    # 레벨에 맞게 설정
    def setup(self, level):
        # 얼마동안 숫자를 보여줄지
        self.display_time = 7 - (level // 3)
        self.display_time = max(self.display_time, 2) # 1초 미만이면 1초로 처리

        # 얼마나 많은 숫자를 보여 줄 것인가?
        number_count = (level // 3) + 5
        number_count = min(number_count, 20) # 만약 20 을 초과하면 20 으로 처리

        # 실제 화면에 grid 형태로 숫자를 랜덤으로 배치
        self.shuffle_grid(number_count)

    # 숫자 섞기 (이 프로젝트에서 가장 중요)
    def shuffle_grid(self, number_count):
        rows = 5
        columns = 9

        cell_size = 130 # 각 Grid cell 별 가로, 세로 크기
        button_size = 110 # Grid cell 내에 실제로 그려질 버튼 크기
        screen_left_margin = 55 # 전체 스크린 왼쪽 여백
        screen_top_margin = 20 #전체 스크린 위쪽 여백
        self.number_buttons = []

        # [0, 0, 0, 0, 0, 0, 0, 0, 0]
        grid = [[0 for col in range(columns)] for row in range(rows)] # 5 x 9

        number = 1 # 시작 숫자 1부터 number_count 까지, 만약 5 라면 5까지 숫자를 랜덤으로 배치
        while number <= number_count:
            row_idx = randrange(0, rows) # 0, 1, 2, 3, 4 중에서 랜덤 뽑기
            col_idx = randrange(0, columns) # 0~ 8 중에서 랜덤으로 뽑기

            if grid[row_idx][col_idx] == 0:
                grid[row_idx][col_idx] = number # 숫자 지정
                number += 1

                # 현재 grid cell 위치 기준으로 x, y 위치를 구함
                center_x = screen_left_margin + (col_idx * cell_size) + ( cell_size / 2 )
                center_y = screen_top_margin + ( row_idx * cell_size) + ( cell_size / 2 )

                # 숫자 버튼 만들기
                self.button = pygame.Rect(0, 0, button_size, button_size)
                self.button.center = (center_x, center_y)

                self.number_buttons.append(self.button)

        # 배치된 랜덤 숫자 확인 
        print(grid)

    # 시작 화면 보여주기
    def display_start_screen(self):

        self.st_btn.blit_center(self.screen, self.start_button1)

        self.msg = self.level_font.render(f"now level : {self.curr_level}", True, self.WHITE)
        m = get(self.msg)
        m_center = m.individual_pos(m.object_width / 2, m.object_height / 2)
        self.msg_rect = self.msg.get_rect(center = m_center)

        m.blit(self.screen, self.msg)

    # pos 에 해당하는 버튼 확인
    def check_buttons(self, pos):
        if self.start1: # 게임이 시작했으면?
            self.check_number_buttons(pos)
            print("g1 start : "+str(self.start1)+", g1 state : "+ str(self.screen_state))

        if self.screen_state == 0:
            if self.start_button1_rect.collidepoint(pos):
                self.start1 = True
                self.screen_state = 1
                self.start_ticks = pygame.time.get_ticks() # 타이머 시작 (현재 시간을 저장)

        if self.screen_state == 2:
            if self.re_msg_rect.collidepoint(pos):
                self.game_over()

    # 게임 화면 보여주기
    def display_game_screen(self):
        
        if not self.hidden:
            elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000 # ms -> sec
            if elapsed_time > self.display_time:
                self.hidden = True

        for idx, rect in enumerate(self.number_buttons, start = 1):
            if self.hidden: # 숨김 처리
                # 버튼 사각형 그리기
                pygame.draw.rect(self.screen, self.GRAY, rect)
            else:
                # 실제 숫자 텍스트
                cell_text = self.game_font.render(str(idx), True, self.WHITE)
                text_rect = cell_text.get_rect(center = rect.center)
                self.screen.blit(cell_text, text_rect)
                
        self.character_draw()
        self.gun_draw()

    def check_number_buttons(self, pos):

        for self.button in self.number_buttons:
            if self.button.collidepoint(pos):
                if self.button == self.number_buttons[0]: # 올바른 숫자 클릭
                    print("Correct")
                    del self.number_buttons[0]
                    if not self.hidden:
                        self.hidden = True # 숫자 숨김 처리
                else: # 잘못된 숫자 클릭
                    self.start1 = False
                    self.over = True
                    self.screen_state = 2
                    self.game_over_screen()
                    print("Wrong")
                    break

        # 모든 숫자를 다 맞췄을 때 레벨을 업해줌
        if len(self.number_buttons) == 0:
            self.start1 = False
            self.hidden = False
            self.over = False
            self.curr_level += 1
            self.setup(self.curr_level)


    # 게임 종료 처리, 메시지도 보여줌
    def game_over(self):
        self.hidden = False
        self.start1  = False
        self.over = False

        self.number_buttons = []
        self.curr_level = 1
        self.setup(self.curr_level)
        self.screen_state = 0
        
    # 게임 종료 되었을 때 나타나는 스크린
    def game_over_screen(self):
        msg = self.game_font.render(f"Your level is {self.curr_level}", True, self.WHITE)
        msg_rect = msg.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
        
        self.screen.fill(self.BLACK)
        self.screen.blit(msg, msg_rect)
        self.r.blit(self.screen, self.re_msg)
