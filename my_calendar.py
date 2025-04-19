
import pygame
from datetime import datetime
from constants import BOARD_SIZE, GAP, WHITE, BLACK, MARGIN, HEIGHT, WIDTH, BLUE, TILE_SIZE, \
UP_ARROW_LEFT_VERTEX, UP_ARROW_MIDDLE_VERTEX, UP_ARROW_RIGHT_VERTEX, DOWN_ARROW_LEFT_VERTEX, \
DOWN_ARROW_MIDDLE_VERTEX, DOWN_ARROW_RIGHT_VERTEX, BIG_TILE_SIZE

class Calendar():
    def __init__(self, win):
        self.win = win
        self.current_datetime_obj = None
        self.current_year = 0
        self.current_month = 0
        self.current_day = 0
        self.update_current_datetime()
        self.chosen_year = self.current_year
        self.chosen_month = self.current_month
        self.chosen_day = None
        self.description_dims = (0, 0)
        self.chosen_month_obj_list = []
        if self.chosen_year and self.chosen_month and not self.chosen_day:
            self.generate_chosen_month()

    # due to highlight the current day, month and year in the calendar
    def update_current_datetime(self):
        self.current_datetime_obj = datetime.now()
        #self.current_datetime_obj = datetime(2025,6,6) # for tests
        self.current_year = int(self.current_datetime_obj.strftime("%Y"))
        self.current_month = int(self.current_datetime_obj.strftime("%m"))
        self.current_day = int(self.current_datetime_obj.strftime("%d"))

    def render(self):
        self.update_current_datetime()
        self.win.fill(WHITE)
        # draw the border of the board
        pygame.draw.rect(self.win, BLACK, (MARGIN, HEIGHT - WIDTH + MARGIN, \
            BOARD_SIZE, BOARD_SIZE), width=1)
        # draw the up and down arrows (above the board)
        pygame.draw.polygon(self.win, BLACK,
                            [UP_ARROW_LEFT_VERTEX, UP_ARROW_MIDDLE_VERTEX, UP_ARROW_RIGHT_VERTEX],
                            width=0)
        pygame.draw.polygon(self.win, BLACK, 
                            [DOWN_ARROW_LEFT_VERTEX, DOWN_ARROW_MIDDLE_VERTEX, DOWN_ARROW_RIGHT_VERTEX],
                            width=0)
        
        if self.chosen_year and self.chosen_month and not self.chosen_day:
            # draw the content above the board if a specific month has been chosen
            font = pygame.font.SysFont('comicsans', 22)
            chosen_datetime_obj = datetime(self.chosen_year, self.chosen_month, 1)
            month_and_year = font.render(chosen_datetime_obj.strftime("%B") + ' ' + \
                                     chosen_datetime_obj.strftime("%Y"), 1, BLACK)
            self.win.blit(month_and_year, (int(MARGIN + GAP), \
                    int(HEIGHT - WIDTH - month_and_year.get_height())))
            self.description_dims = (month_and_year.get_width(), month_and_year.get_height())
            # draw the content inside the board if a specific month has been chosen
            self.draw_chosen_month()
        
        if self.chosen_year and not self.chosen_month and not self.chosen_day:
            # draw the content above the board if a specific year has been chosen
            font = pygame.font.SysFont('comicsans', 22)
            year = font.render(str(self.chosen_year), 1, BLACK)
            self.win.blit(year, (int(MARGIN + GAP), \
                    int(HEIGHT - WIDTH - year.get_height())))
            self.description_dims = (year.get_width(), year.get_height())
            # draw the content inside the board if a specific year has been chosen
            self.draw_all_months()

        pygame.display.update()

    def draw_chosen_month(self):
        weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        font = pygame.font.SysFont('comicsans', 18)
        for i in range(7):
            weekday = font.render(weekday_list[i], 1, BLACK)
            self.win.blit(weekday, (int(MARGIN + GAP + i*(TILE_SIZE+GAP) + TILE_SIZE / 2 - weekday.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + GAP + TILE_SIZE / 2 - weekday.get_height() / 2)))
            
        first_day_obj = self.chosen_month_obj_list[0]
        for day_obj in self.chosen_month_obj_list:
            j = int(day_obj.strftime("%W")) - int(first_day_obj.strftime("%W")) # the difference between week number of year
            if day_obj.strftime("%w") == '0': # Weekday as a number 0-6, 0 is Sunday
                weekday_num = 7 # conversion Sunday to 7
            else:
                weekday_num = int(day_obj.strftime("%w")) # from 1 to 6 (from Monday to Saturday)
            # highlight the current day on the chosen (and also current) month and year
            if self.chosen_year == self.current_year and self.chosen_month == self.current_month \
                and int(day_obj.strftime("%d")) == self.current_day:
                color = BLUE
            else:
                color = BLACK
            pygame.draw.rect(self.win, color, (MARGIN + GAP + (weekday_num-1)*(TILE_SIZE+GAP), \
                HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(TILE_SIZE+GAP), \
                TILE_SIZE, TILE_SIZE), width=1)
            day_num = font.render(str(int(day_obj.strftime("%d"))), 1, color) # Day of month 1-31
            self.win.blit(day_num, (int(MARGIN + GAP + (weekday_num-1)*(TILE_SIZE+GAP) + TILE_SIZE / 2 - day_num.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(TILE_SIZE+GAP) + TILE_SIZE / 2 - day_num.get_height() / 2)))

    def generate_chosen_month(self):
        self.chosen_month_obj_list = []
        if self.chosen_month in (1,3,5,7,8,10,12):
            last_day = 31
        elif self.chosen_month in (4,6,9,11):
            last_day = 30
        else: # chosen month is February
            if self.last_day_of_february_is_valid(29, self.chosen_month, self.chosen_year):
                last_day = 29
            else:
                last_day = 28
        for i in range(1, last_day+1):
            self.chosen_month_obj_list.append(datetime(self.chosen_year, self.chosen_month, i))

    def last_day_of_february_is_valid(self, day, month, year):
        if day == 29 and month == 2:
            if year%4 == 0 and year%100 != 0 or year%400 == 0:
                return True # February 29 is valid
            return False # February 29 is not valid
        #return True # not concern February 29
    
    def change_chosen_month(self, next=True):
        if next:
            if self.chosen_month == 12:
                self.chosen_year += 1
                self.chosen_month = 1
            else:
                self.chosen_month += 1
        else: # previous month
            if self.chosen_month == 1:
                self.chosen_year -= 1
                self.chosen_month = 12
            else:
                self.chosen_month -= 1
        self.generate_chosen_month()

    def generate_months(self):
        self.chosen_month = None

    def draw_all_months(self):
        month_num_list = [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12)]
        font = pygame.font.SysFont('comicsans', 22)
        for j in range(3):
            for i in range(4):
                # highlight the current month in the chosen (and also current) year
                if self.chosen_year == self.current_year and \
                    month_num_list[j][i] == self.current_month: 
                    color = BLUE
                else:
                    color = BLACK
                pygame.draw.rect(self.win, color, (MARGIN + GAP + i*(BIG_TILE_SIZE+GAP), \
                    HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP), \
                    BIG_TILE_SIZE, BIG_TILE_SIZE), width=1)
                month = font.render(datetime(self.chosen_year, month_num_list[j][i], 1).strftime("%b"), 1, color) # Month name, short version
                self.win.blit(month, (int(MARGIN + GAP + i*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE / 2 - month.get_width() / 2), \
                    int(HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE / 2 - month.get_height() / 2)))

    def change_chosen_year(self, next=True):
        if next:
            self.chosen_year += 1
        else: # previous year
            self.chosen_year -= 1

    def choose_month(self, pos_x, pos_y):
        month_num_list = [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12)]
        for j in range(3):
            for i in range(4):
                if pos_x >= MARGIN + GAP + i*(BIG_TILE_SIZE+GAP) and \
                pos_x <= MARGIN + (i+1)*(BIG_TILE_SIZE+GAP) and \
                pos_y >= HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP) and \
                pos_y <= HEIGHT - WIDTH + MARGIN + (j+1)*(BIG_TILE_SIZE+GAP):
                    self.chosen_month = month_num_list[j][i]
                    self.generate_chosen_month()
                    return
