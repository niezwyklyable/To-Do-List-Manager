
import pygame
from datetime import datetime
from constants import BOARD_SIZE, GAP, WHITE, BLACK, MARGIN, HEIGHT, WIDTH, BLUE, TILE_SIZE, \
UP_ARROW_LEFT_VERTEX, UP_ARROW_MIDDLE_VERTEX, UP_ARROW_RIGHT_VERTEX, DOWN_ARROW_LEFT_VERTEX, \
DOWN_ARROW_MIDDLE_VERTEX, DOWN_ARROW_RIGHT_VERTEX, BIG_TILE_SIZE, RED, ORANGE, RADIUS, CYAN

class Calendar():
    def __init__(self, win, tasks):
        self.win = win
        self.current_datetime_obj = None
        self.current_year = 0
        self.current_month = 0
        self.current_day = 0
        self.current_decade = 0
        self.update_current_datetime()
        self.chosen_decade = self.current_decade
        self.chosen_year = self.current_year
        self.chosen_month = self.current_month
        self.chosen_day = None
        self.description_dims = (0, 0)
        self.chosen_month_obj_list = []
        self.chosen_decade_list = []
        if self.chosen_year and self.chosen_month and not self.chosen_day:
            self.generate_chosen_month()
        self.events = []
        self.extract_events(tasks)
        self.chosen_day_event_list = []

    # extract events and deadlines from the all tasks
    def extract_events(self, tasks):
        for t in tasks:
            if t.datetime_obj:
                self.events.append(t)

    # due to highlight the current day, month and year in the calendar
    def update_current_datetime(self):
        self.current_datetime_obj = datetime.now()
        #self.current_datetime_obj = datetime(2025,6,6) # for tests
        self.current_year = int(self.current_datetime_obj.strftime("%Y"))
        self.current_month = int(self.current_datetime_obj.strftime("%m"))
        self.current_day = int(self.current_datetime_obj.strftime("%d"))
        self.current_decade = int(str(self.current_year)[0:3] + '0')

    def render(self):
        self.update_current_datetime()
        self.win.fill(WHITE)
        # draw the border of the board
        # highlight the border of the board on the chosen (and also current) day
        if self.chosen_year == self.current_year and self.chosen_month == self.current_month \
            and self.chosen_day == self.current_day:
            color = BLUE
        else:
            color = BLACK
        pygame.draw.rect(self.win, color, (MARGIN, HEIGHT - WIDTH + MARGIN, \
            BOARD_SIZE, BOARD_SIZE), width=1)
        # draw the up and down arrows (above the board)
        pygame.draw.polygon(self.win, BLACK,
                            [UP_ARROW_LEFT_VERTEX, UP_ARROW_MIDDLE_VERTEX, UP_ARROW_RIGHT_VERTEX],
                            width=0)
        pygame.draw.polygon(self.win, BLACK, 
                            [DOWN_ARROW_LEFT_VERTEX, DOWN_ARROW_MIDDLE_VERTEX, DOWN_ARROW_RIGHT_VERTEX],
                            width=0)
        
        if not self.chosen_year and not self.chosen_month and not self.chosen_day:
            # draw the content above the board if a specific decade has been chosen
            font = pygame.font.SysFont('comicsans', 22)
            decade = font.render(f'{self.chosen_decade} - {self.chosen_decade+9}', 1, BLACK)
            self.win.blit(decade, (int(MARGIN + GAP), \
                    int(HEIGHT - WIDTH - decade.get_height())))
            self.description_dims = (decade.get_width(), decade.get_height())
            # draw the content inside the board if a specific decade has been chosen
            self.draw_chosen_decade()

        if self.chosen_year and not self.chosen_month and not self.chosen_day:
            # draw the content above the board if a specific year has been chosen
            font = pygame.font.SysFont('comicsans', 22)
            year = font.render(str(self.chosen_year), 1, BLACK)
            self.win.blit(year, (int(MARGIN + GAP), \
                    int(HEIGHT - WIDTH - year.get_height())))
            self.description_dims = (year.get_width(), year.get_height())
            # draw the content inside the board if a specific year has been chosen
            self.draw_chosen_year()

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

        if self.chosen_year and self.chosen_month and self.chosen_day:
            # draw the content above the board if a specific day has been chosen
            font = pygame.font.SysFont('comicsans', 22)
            if self.chosen_year == self.current_year and self.chosen_month == self.current_month \
            and self.chosen_day == self.current_day:
                color = BLUE
            else:
                color = BLACK
            chosen_datetime_obj = datetime(self.chosen_year, self.chosen_month, self.chosen_day)
            day_month_and_year = font.render(str(int(chosen_datetime_obj.strftime("%d"))) + \
                                    ' ' + chosen_datetime_obj.strftime("%B") + ' ' + \
                                     chosen_datetime_obj.strftime("%Y"), 1, color)
            self.win.blit(day_month_and_year, (int(MARGIN + GAP), \
                    int(HEIGHT - WIDTH - day_month_and_year.get_height())))
            self.description_dims = (day_month_and_year.get_width(), day_month_and_year.get_height())
            # draw the content inside the board if a specific day has been chosen
            self.draw_chosen_day()

        pygame.display.update()

    def draw_chosen_decade(self):
        font = pygame.font.SysFont('comicsans', 22)
        for j in range(4):
            for i in range(4):
                # do not draw if None value is given
                if self.chosen_decade_list[j][i] == None:
                    continue
                # highlight the current year in the chosen (and also current) decade
                if self.chosen_decade == self.current_decade and \
                    self.chosen_decade_list[j][i] == self.current_year: 
                    color = BLUE
                else:
                    color = BLACK
                # draw the border of the big tile
                pygame.draw.rect(self.win, color, (MARGIN + GAP + i*(BIG_TILE_SIZE+GAP), \
                    HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP), \
                    BIG_TILE_SIZE, BIG_TILE_SIZE), width=1)
                # draw the events and deadlines as the points at the rendered year in the big tile area
                for e in self.events:
                    if self.chosen_decade == self.current_decade and \
                    int(e.datetime_obj.strftime("%Y")) == self.chosen_decade_list[j][i]:
                        pygame.draw.circle(self.win, ORANGE, (int(MARGIN + GAP + i*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE/2), \
                            int(HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP) + 4/5*BIG_TILE_SIZE)), radius=RADIUS)
                # draw the year number in the center of the big tile area
                year = font.render(str(self.chosen_decade_list[j][i]), 1, color)
                self.win.blit(year, (int(MARGIN + GAP + i*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE / 2 - year.get_width() / 2), \
                    int(HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE / 2 - year.get_height() / 2)))

    def draw_chosen_year(self):
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
                # draw the border of the big tile
                pygame.draw.rect(self.win, color, (MARGIN + GAP + i*(BIG_TILE_SIZE+GAP), \
                    HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP), \
                    BIG_TILE_SIZE, BIG_TILE_SIZE), width=1)
                # draw the events and deadlines as the points at the rendered month in the big tile area
                for e in self.events:
                    if int(e.datetime_obj.strftime("%Y")) == self.chosen_year and \
                    int(e.datetime_obj.strftime("%m")) == month_num_list[j][i]:
                        pygame.draw.circle(self.win, ORANGE, (int(MARGIN + GAP + i*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE/2), \
                            int(HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP) + 4/5*BIG_TILE_SIZE)), radius=RADIUS)
                # draw the month name in the center of the big tile area
                month = font.render(datetime(self.chosen_year, month_num_list[j][i], 1).strftime("%b"), 1, color) # Month name, short version
                self.win.blit(month, (int(MARGIN + GAP + i*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE / 2 - month.get_width() / 2), \
                    int(HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP) + BIG_TILE_SIZE / 2 - month.get_height() / 2)))

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
            # draw the border of the tile
            pygame.draw.rect(self.win, color, (MARGIN + GAP + (weekday_num-1)*(TILE_SIZE+GAP), \
                HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(TILE_SIZE+GAP), \
                TILE_SIZE, TILE_SIZE), width=1)
            # draw the events and deadlines as the points at the rendered day in the tile area
            for e in self.events:
                if int(e.datetime_obj.strftime("%Y")) == self.chosen_year and \
                int(e.datetime_obj.strftime("%m")) == self.chosen_month and \
                e.datetime_obj.strftime("%d") ==  day_obj.strftime("%d"):
                    pygame.draw.circle(self.win, ORANGE, (int(MARGIN + GAP + (weekday_num-1)*(TILE_SIZE+GAP) + TILE_SIZE/2), \
                         int(HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(TILE_SIZE+GAP) + 4/5*TILE_SIZE)), radius=RADIUS)
            # draw the day number in the center of the tile area
            day_num = font.render(str(int(day_obj.strftime("%d"))), 1, color) # Day of month 1-31
            self.win.blit(day_num, (int(MARGIN + GAP + (weekday_num-1)*(TILE_SIZE+GAP) + TILE_SIZE / 2 - day_num.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(TILE_SIZE+GAP) + TILE_SIZE / 2 - day_num.get_height() / 2)))

    def draw_chosen_day(self):
        font = pygame.font.SysFont('comicsans', 18)
        if self.chosen_day_event_list:
            temp_counter = 0
            for e in self.chosen_day_event_list:
                # active task color settings
                if e.state == 'to-do':
                    color = CYAN
                elif e.state == 'completed':
                    color = BLUE
                # with time
                if e.time:
                    info = font.render(f'#{e.task_number}: {e.time} - {e.target_info} | [{e.state}]', 1, color)
                # without time
                else:
                    info = font.render(f'#{e.task_number}: {e.target_info} | [{e.state}]', 1, color)
                self.win.blit(info, (int(MARGIN + GAP), \
                    int(HEIGHT - WIDTH + MARGIN + GAP + temp_counter*info.get_height())))
                temp_counter += 1
        else:
            # draw no task message
            no_task_info = font.render('There is no tasks detected on the chosen day.', 1, RED)
            self.win.blit(no_task_info, (int(MARGIN + GAP), \
                int(HEIGHT - WIDTH + MARGIN + GAP)))

    def generate_last_day_of_month(self, month, year):
        if month in (1,3,5,7,8,10,12):
            last_day = 31
        elif month in (4,6,9,11):
            last_day = 30
        else: # chosen month is February
            if year%4 == 0 and year%100 != 0 or year%400 == 0:
                last_day = 29
            else:
                last_day = 28
        return last_day

    def generate_all_years_list(self):
        # create a list of tuples of 100 years before the current year and 100 year after current year (201 years in total)
        all_years_list = []
        for y in range(self.current_year-100, self.current_year+100, 4):
            temp_tuple = tuple()
            for _ in range(4):
                temp_tuple += (y, )
                y += 1
            all_years_list.append(temp_tuple)
        all_years_list.append((self.current_year + 100, None, None, None))
        return all_years_list

    def generate_chosen_decade(self, years_before_first_decade=False, years_after_last_decade=False):
        self.chosen_year = None
        all_years_list = self.generate_all_years_list()
        # extract the specific range of years which are before the first decade in all generated years
        if years_before_first_decade:
            self.chosen_decade_list = all_years_list[0:4]
        # extract the specific range of years which are after the last decade in all generated years
        elif years_after_last_decade:
            self.chosen_decade_list = all_years_list[-4:]
        # extract the specific range of years including the chosen decade which will be ready to view on the board
        else:
            for t in all_years_list:
                if self.chosen_decade in t:
                    pointer = all_years_list.index(t)
                    break
            self.chosen_decade_list = all_years_list[pointer:pointer+4]

    def generate_chosen_year(self):
        self.chosen_month = None
        if self.chosen_year >= self.chosen_decade + 10 and self.chosen_decade + 20 < self.current_year + 100:
            self.chosen_decade += 10
        elif self.chosen_year < self.chosen_decade and self.chosen_decade - 10 > self.current_year - 100:
            self.chosen_decade -= 10

    def generate_chosen_month(self):
        self.chosen_day = None
        self.chosen_month_obj_list = []
        last_day = self.generate_last_day_of_month(self.chosen_month, self.chosen_year)
        for i in range(1, last_day+1):
            self.chosen_month_obj_list.append(datetime(self.chosen_year, self.chosen_month, i))

    def generate_chosen_day(self):
        # extract events which happen only on the chosen day
        self.chosen_day_event_list = []
        for e in self.events:
            if int(e.datetime_obj.strftime("%Y")) == self.chosen_year and \
            int(e.datetime_obj.strftime("%m")) == self.chosen_month and \
            int(e.datetime_obj.strftime("%d")) == self.chosen_day:
                self.chosen_day_event_list.append(e)
        if self.chosen_day_event_list == []:
            return
        # filtering and sorting events
        temp_filtered_tasks = [] # with time
        temp_filtered_tasks_without_time = []
        for e in self.chosen_day_event_list:
            if e.time == None:
                temp_filtered_tasks_without_time.append(e) # append events without time
            else:
                temp_filtered_tasks.append(e) # append events which have be set time
        # sort events with time only by time
        sorted_temp_filtered_tasks_by_minutes = sorted(temp_filtered_tasks, key=lambda e: e.get_time()[1])
        sorted_temp_filtered_tasks_by_hours = sorted(sorted_temp_filtered_tasks_by_minutes, key=lambda e: e.get_time()[0])
        # concatenate two lists in specific order (events without time and events with time)
        sorted_temp_filtered_tasks = temp_filtered_tasks_without_time + sorted_temp_filtered_tasks_by_hours
        # sort all events by state (completed/to-do)
        self.chosen_day_event_list = sorted(sorted_temp_filtered_tasks, key=lambda e: e.get_state())
            
    def change_chosen_decade(self, next=True):
        all_years_list = self.generate_all_years_list()
        if next:
            for t in all_years_list:
                if self.chosen_decade + 20 in t: # it is 20 not 10 because of the bugg concerning self.chosen_decade_list
                    self.chosen_decade += 10
                    break
            else:
                self.generate_chosen_decade(years_after_last_decade=True)
                return
        else: # previous decade
            for t in all_years_list:
                if self.chosen_decade - 10 in t:
                    self.chosen_decade -= 10
                    break
            else:
                self.generate_chosen_decade(years_before_first_decade=True)
                return
        self.generate_chosen_decade()

    def change_chosen_year(self, next=True):
        if next:
            # do not let change the year when it reaches max value
            if self.chosen_year == self.current_year + 100:
                return
            self.chosen_year += 1
            if self.chosen_year >= self.chosen_decade + 10 and self.chosen_decade + 20 < self.current_year + 100:
                self.chosen_decade += 10
        else: # previous year
            # do not let change the year when it reaches min value
            if self.chosen_year == self.current_year - 100:
                return
            self.chosen_year -= 1
            if self.chosen_year < self.chosen_decade and self.chosen_decade - 10 > self.current_year - 100:
                self.chosen_decade -= 10

    def change_chosen_month(self, next=True):
        if next:
            if self.chosen_month == 12:
                # do not let change the year when it reaches max value
                if self.chosen_year == self.current_year + 100:
                    return
                self.chosen_year += 1
                self.chosen_month = 1
            else:
                self.chosen_month += 1
        else: # previous month
            if self.chosen_month == 1:
                # do not let change the year when it reaches min value
                if self.chosen_year == self.current_year - 100:
                    return
                self.chosen_year -= 1
                self.chosen_month = 12
            else:
                self.chosen_month -= 1
        self.generate_chosen_month()

    def change_chosen_day(self, next=True):
        if next:
            if self.chosen_day == self.generate_last_day_of_month(self.chosen_month, self.chosen_year):
                if self.chosen_month == 12:
                    # do not let change the year when it reaches max value
                    if self.chosen_year == self.current_year + 100:
                        return
                    self.chosen_year += 1
                    self.chosen_month = 1
                    self.chosen_day = 1
                else:
                    self.chosen_month += 1
                    self.chosen_day = 1
            else:
                self.chosen_day += 1
        else: # previous day
            if self.chosen_day == 1:
                if self.chosen_month == 1:
                    # do not let change the year when it reaches min value
                    if self.chosen_year == self.current_year - 100:
                        return
                    self.chosen_year -= 1
                    self.chosen_month = 12
                    self.chosen_day = 31
                else:
                    self.chosen_month -= 1
                    self.chosen_day = self.generate_last_day_of_month(self.chosen_month, self.chosen_year)
            else:
                self.chosen_day -= 1
        self.generate_chosen_day()

    def choose_year(self, pos_x, pos_y):
        for j in range(4):
            for i in range(4):
                if pos_x >= MARGIN + GAP + i*(BIG_TILE_SIZE+GAP) and \
                pos_x <= MARGIN + (i+1)*(BIG_TILE_SIZE+GAP) and \
                pos_y >= HEIGHT - WIDTH + MARGIN + GAP + j*(BIG_TILE_SIZE+GAP) and \
                pos_y <= HEIGHT - WIDTH + MARGIN + (j+1)*(BIG_TILE_SIZE+GAP):
                    self.chosen_year = self.chosen_decade_list[j][i]
                    self.generate_chosen_year()
                    return

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

    def choose_day(self, pos_x, pos_y):
        first_day_obj = self.chosen_month_obj_list[0]
        for day_obj in self.chosen_month_obj_list:
            j = int(day_obj.strftime("%W")) - int(first_day_obj.strftime("%W")) # the difference between week number of year
            if day_obj.strftime("%w") == '0': # Weekday as a number 0-6, 0 is Sunday
                weekday_num = 7 # conversion Sunday to 7
            else:
                weekday_num = int(day_obj.strftime("%w")) # from 1 to 6 (from Monday to Saturday)
            if pos_x >= MARGIN + GAP + (weekday_num-1)*(TILE_SIZE+GAP) and \
            pos_x <= MARGIN + weekday_num*(TILE_SIZE+GAP) and \
            pos_y >= HEIGHT - WIDTH + MARGIN + GAP + (j+1)*(TILE_SIZE+GAP) and \
            pos_y <= HEIGHT - WIDTH + MARGIN + (j+2)*(TILE_SIZE+GAP):
                self.chosen_day = int(day_obj.strftime("%d")) # Day of month 1-31
                self.generate_chosen_day()
                return
    