from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import \
    OptionProperty, \
    ObjectProperty, \
    NumericProperty, \
    ReferenceListProperty, \
    ListProperty, \
    BooleanProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.graphics import Rectangle, Ellipse, Triangle, Line
from random import randint


class Snake(Widget):
    head = ObjectProperty(None)
    tail = ObjectProperty(None)

    def move(self):
        next_tail_pos = list(self.head.position)
        self.head.move()
        self.tail.add_block(next_tail_pos)

    def remove(self):
        self.tail.remove()
        self.head.remove()

    def get_position(self):
        return self.head.position

    def get_full_position(self):
        return self.head.position + self.tail.blocks_positions

    def set_position(self, position):
        self.head.position = position

    def get_direction(self):
        return self.head.direction

    def set_direction(self, direction):
        self.head.direction = direction


class SnakeTail(Widget):
    size = NumericProperty(3)
    blocks_positions = ListProperty()
    tail_blocks = ListProperty()

    def remove(self):
        self.size = 3
        for block in self.tail_blocks:
            self.canvas.remove(block)
        self.tail_blocks = []
        self.blocks_positions = []

    def add_block(self, pos):
        # if tail block position outside of the game, don't add
        # (happens when snake was out of bounds)
        if pos[0]<1 or pos[0]>SnakeGame.col_number \
        or pos[1]<1 or pos[1]>SnakeGame.row_number:
            return 

        self.blocks_positions.append(pos)
        if len(self.blocks_positions) > self.size:
            self.blocks_positions.pop(0)

        with self.canvas:
            for block_pos in self.blocks_positions:
                x = (block_pos[0] - 1) * self.width
                y = (block_pos[1] - 1) * self.height
                coord = (x, y)
                block = Rectangle(pos=coord, size=(self.width, self.height))
                self.tail_blocks.append(block)
                if len(self.tail_blocks) > self.size:
                    last_block = self.tail_blocks.pop(0)
                    self.canvas.remove(last_block)


class SnakeHead(Widget):
    direction = OptionProperty(
        "Right", options=["Up", "Down", "Left", "Right"])
    points = ListProperty([0] * 6)
    x_position = NumericProperty(0)
    y_position = NumericProperty(0)
    position = ReferenceListProperty(x_position, y_position)
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)

    def is_on_board(self):
        return self.state

    def show(self):
        with self.canvas:
            if not self.is_on_board():
                self.object_on_board = Triangle(points=self.points)
                self.state = True
            else:
                self.canvas.remove(self.object_on_board)
                self.object_on_board = Triangle(points=self.points)

    def remove(self):
        if self.is_on_board():
            self.canvas.remove(self.object_on_board)
            self.object_on_board = ObjectProperty(None)
            self.state = False

    def move(self):
        if self.direction == "Right":
            self.position[0] += 1
            x0 = self.position[0] * self.width
            y0 = (self.position[1] - 0.5) * self.height
            x1 = x0 - self.width
            y1 = y0 + self.height / 2
            x2 = x0 - self.width
            y2 = y0 - self.height / 2
        elif self.direction == "Left":
            self.position[0] -= 1
            x0 = (self.position[0] - 1) * self.width
            y0 = (self.position[1] - 0.5) * self.height
            x1 = x0 + self.width
            y1 = y0 - self.height / 2
            x2 = x0 + self.width
            y2 = y0 + self.height / 2
        elif self.direction == "Up":
            self.position[1] += 1
            x0 = (self.position[0] - 0.5) * self.width
            y0 = self.position[1] * self.height
            x1 = x0 - self.width / 2
            y1 = y0 - self.height
            x2 = x0 + self.width / 2
            y2 = y0 - self.height
        elif self.direction == "Down":
            self.position[1] -= 1
            x0 = (self.position[0] - 0.5) * self.width
            y0 = (self.position[1] - 1) * self.height
            x1 = x0 + self.width / 2
            y1 = y0 + self.height
            x2 = x0 - self.width / 2
            y2 = y0 + self.height
        self.points = [x0, y0, x1, y1, x2, y2]
        self.show()


class Fruit(Widget):
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)
    duration = NumericProperty(10)
    interval = NumericProperty(1)

    def remove(self, *args):
        if self.is_on_board():
            self.canvas.remove(self.object_on_board)
            self.object_on_board = ObjectProperty(None)
            self.state = False

    def is_on_board(self):
        return self.state

    def pop(self, pos):
        self.pos = pos
        with self.canvas:
            x = (pos[0] - 1) * self.size[0]
            y = (pos[1] - 1) * self.size[1]
            coord = (x, y)
            self.state = True
            self.object_on_board = Ellipse(pos=coord, size=self.size)




class SnakeGame(Widget):
    # Children Widgets
    snake = ObjectProperty(None)
    fruit = ObjectProperty(None)

    # User Options
    start_speed = NumericProperty(1)
    border_option = BooleanProperty(False)

    # Internal Options
    col_number = 16
    row_number = 9

    # Game variables
    turn_counter = NumericProperty(0)
    score = NumericProperty(0)

    fruit_rythme = NumericProperty(0)  # Computed from Fruit options

    start_time_coeff = NumericProperty(1)
    running_time_coeff = NumericProperty(1)

    mov_start_pos = ListProperty()
    mov_triggered = BooleanProperty(False)

    def start(self):
        # if border_option is active, draw rectangle around the game area
        if self.border_option:
            with self.canvas.before:
                Line(width=3.,
                     rectangle=(self.x, self.y, self.width, self.height))
        # compute time coeff used as refresh rate for the game
        # using the options provided (default 1.1, max 2)
        self.start_time_coeff += (self.start_speed / 10)
        self.running_time_coeff = self.start_time_coeff

        # instanciate snake
        self.new_snake()

        # start update loop
        self.update()

    def reset(self):
        # reset game variables
        self.turn_counter = 0
        self.running_time_coeff = self.start_time_coeff
        self.score = 0

        # remove the snake widget (+ fruit if need be)
        self.snake.remove()
        self.fruit.remove()

        # unschedule all events (they will be properly rescheduled by the
        # restart mechanism)
        Clock.unschedule(self.pop_fruit)
        Clock.unschedule(self.fruit.remove)
        Clock.unschedule(self.update)

    def new_snake(self):
        # generate random coordinates for the head
        start_coord = (
            randint(2, self.col_number - 2), randint(2, self.row_number - 2))
        self.snake.set_position(start_coord)

        # get random start direction
        rand_index = randint(0, 3)

        # handle consequently (yeah that's messy needs refact)
        start_direction = ["Up", "Down", "Left", "Right"][rand_index]
        self.snake.set_direction(start_direction)

    def pop_fruit(self, *args):
        # get random coordinates for the fruit
        coord = [randint(1, self.col_number), randint(1, self.row_number)]

        # total space occupied by snake
        snake_space = self.snake.get_full_position()

        # if the coordinates are on a space occupied by the snake, re-draw
        while coord in snake_space:
            print "re-drawing"
            coord = [randint(1, self.col_number), randint(1, self.row_number)]

        # pop fruit widget
        self.fruit.pop(coord)
        print "Poped ! at {}".format(coord)

    def update(self, *args):
        if self.turn_counter == 0:
            self.fruit_rythme = self.fruit.interval + self.fruit.duration
            Clock.schedule_interval(
                self.fruit.remove, self.fruit_rythme / self.running_time_coeff)
        elif self.turn_counter == self.fruit.interval:
            self.pop_fruit()
            Clock.schedule_interval(
                self.pop_fruit, self.fruit_rythme / self.running_time_coeff)


        # if game with no borders, check if snake is about to leave the screen
        # if so, replace to corresponding opposite border
        if not self.border_option:
            self.handle_outbound()    

        # move snake
        self.snake.move()

        # check for defeat
        if self.is_defeated():
            self.reset()
            SnakeApp.screen_manager.current = "main_menu_screen"
            return

        if self.fruit.is_on_board():
            if self.snake.get_position() == self.fruit.pos:
                self.fruit.remove()
                self.score += 1
                self.snake.tail.size += 1
                self.running_time_coeff *= 1.05

        self.turn_counter += 1
        Clock.schedule_once(self.update, 1 / self.running_time_coeff)

    def handle_outbound(self):
        position = self.snake.get_position()
        direction = self.snake.get_direction()

        if position[0]==1 and direction == "Left":
            # add the current head position as a tail block
            # otherwise one block would be missed by the normal routine
            self.snake.tail.add_block(list(position))
            self.snake.set_position([self.col_number + 1, position[1]])
        elif position[0]==self.col_number and direction == "Right":
            self.snake.tail.add_block(list(position))            
            self.snake.set_position([0, position[1]])
        elif position[1]==1 and direction == "Down":
            self.snake.tail.add_block(list(position))
            self.snake.set_position([position[0], self.row_number + 1])
        elif position[1] == self.row_number and direction == "Up":
            self.snake.tail.add_block(list(position))
            self.snake.set_position([position[0], 0])

    def is_defeated(self):
        snake_position = self.snake.get_position()

        if snake_position in self.snake.tail.blocks_positions:
            return True

        if self.border_option:
            if snake_position[0] > self.col_number \
            or snake_position[0] < 1 \
            or snake_position[1] > self.row_number \
            or snake_position[1] < 1:
                return True

        return False


    def on_touch_down(self, touch):
        self.mov_start_pos = touch.spos

    def on_touch_up(self, touch):
        self.mov_triggered = False

    def on_touch_move(self, touch):
        delta = Vector(*touch.spos) - Vector(*self.mov_start_pos)
        if (self.mov_triggered == False) \
                and (abs(delta[0]) > 0.1 or abs(delta[1]) > 0.1):
            if abs(delta[0]) > abs(delta[1]):
                if delta[0] > 0:
                    self.snake.set_direction("Right")
                else:
                    self.snake.set_direction("Left")
            else:
                if delta[1] > 0:
                    self.snake.set_direction("Up")
                else:
                    self.snake.set_direction("Down")
            self.mov_triggered = True



class MainMenuScreen(Screen):
    options_popup = ObjectProperty(None)

    def show_popup(self):
        self.options_popup = OptionsPopup()
        self.options_popup.open()


class OptionsPopup(Popup):
    border_option_widget = ObjectProperty(None)
    speed_option_widget = ObjectProperty(None)

    def on_dismiss(self):
        SnakeGame.start_speed = self.speed_option_widget.value
        SnakeGame.border_option = self.border_option_widget.active


class GameScreen(Screen):
    game_widget = ObjectProperty(None)

    def on_enter(self):
        self.game_widget.start()


class SnakeApp(App):
    screen_manager = ObjectProperty(None)

    def build(self):
        SnakeApp.screen_manager = ScreenManager()
        mms = MainMenuScreen(name='main_menu_screen')
        gs = GameScreen(name='game_screen')

        self.screen_manager.add_widget(mms)
        self.screen_manager.add_widget(gs)

        return self.screen_manager


if __name__ == "__main__":
    SnakeApp().run()
