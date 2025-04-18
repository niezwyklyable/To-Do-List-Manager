
import pygame
from datetime import datetime
from constants import BOARD_SIZE, GAP, WHITE, BLACK, MARGIN, HEIGHT, WIDTH

class Calendar():
    def __init__(self, win):
        self.win = win
        self.current_datetime_obj = None
        self.update_current_datetime()
        self.chosen_year = self.current_year
        self.chosen_month = self.current_month
        self.chosen_day = None
        self.tile_size = (BOARD_SIZE - GAP * (7 + 1)) // 7
        self.chosen_month_obj_list = []
        if self.chosen_year and self.chosen_month:
            self.generate_chosen_month()

    # due to highlight the current day on the calendar
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
            BOARD_SIZE, BOARD_SIZE))
        pygame.draw.rect(self.win, WHITE, (MARGIN + 1, HEIGHT - WIDTH + MARGIN + 1, \
            BOARD_SIZE - 2, BOARD_SIZE - 2))
        
        if self.chosen_year and self.chosen_month and not self.chosen_day:
            # draw the content above the board if a specific month has been chosen
            font = pygame.font.SysFont('comicsans', 22)
            chosen_datetime_obj = datetime(self.chosen_year, self.chosen_month, 1)
            month_and_year = font.render(chosen_datetime_obj.strftime("%B") + ' ' + \
                                     chosen_datetime_obj.strftime("%Y"), 1, BLACK)
            self.win.blit(month_and_year, (int(MARGIN + GAP), \
                    int(HEIGHT - WIDTH - month_and_year.get_height())))
            # draw the content inside the board if a specific month has been chosen
            self.draw_chosen_month()
        pygame.display.update()

    def draw_chosen_month(self):
        weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        font = pygame.font.SysFont('comicsans', 18)
        for i in range(7):
            # pygame.draw.rect(self.win, BLACK, (MARGIN + GAP + i*(self.tile_size+GAP), \
            #     HEIGHT - WIDTH + MARGIN + GAP, \
            #     self.tile_size, self.tile_size))
            # pygame.draw.rect(self.win, WHITE, (MARGIN + GAP + i*(self.tile_size+GAP) + 1, \
            #     HEIGHT - WIDTH + MARGIN + GAP + 1, \
            #     self.tile_size - 2, self.tile_size - 2))
            weekday = font.render(weekday_list[i], 1, BLACK)
            self.win.blit(weekday, (int(MARGIN + GAP + i*(self.tile_size+GAP) + self.tile_size / 2 - weekday.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + GAP + self.tile_size / 2 - weekday.get_height() / 2)))
            
        #font = pygame.font.SysFont('comicsans', 18)
        first_day_obj = self.chosen_month_obj_list[0]
        for day_obj in self.chosen_month_obj_list:
            j = int(day_obj.strftime("%W")) - int(first_day_obj.strftime("%W")) # the difference between week number of year
            if day_obj.strftime("%w") == '0': # Weekday as a number 0-6, 0 is Sunday
                weekday_num = 7 # conversion Sunday to 7
            else:
                weekday_num = int(day_obj.strftime("%w")) # from 1 to 6 (from Monday to Saturday)
            pygame.draw.rect(self.win, BLACK, (MARGIN + GAP + (weekday_num-1)*(self.tile_size+GAP), \
                HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(self.tile_size+GAP), \
                self.tile_size, self.tile_size))
            pygame.draw.rect(self.win, WHITE, (MARGIN + GAP + (weekday_num-1)*(self.tile_size+GAP) + 1, \
                HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(self.tile_size+GAP) + 1, \
                self.tile_size - 2, self.tile_size - 2))
            day_num = font.render(str(int(day_obj.strftime("%d"))), 1, BLACK) # Day of month 1-31
            self.win.blit(day_num, (int(MARGIN + GAP + (weekday_num-1)*(self.tile_size+GAP) + self.tile_size / 2 - day_num.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(self.tile_size+GAP) + self.tile_size / 2 - day_num.get_height() / 2)))

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
    