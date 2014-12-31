from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import \
    OptionProperty, \
    ObjectProperty, \
    NumericProperty, \
    ReferenceListProperty, \
    ListProperty, \
    BooleanProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.graphics import Rectangle, Ellipse
from random import randint


class Snake(Widget):
    head = ObjectProperty(None)
    tail = ObjectProperty(None)

    def move(self):
        next_tail_pos = list(self.head.position)
        self.head.move()
        self.tail.add_block(next_tail_pos)

    def set_next_direction(self, direction):
        self.head.direction = direction


class SnakeTail(Widget):
    size = NumericProperty(3)
    blocks_positions = ListProperty()
    tail_blocks = ListProperty()
    block = ObjectProperty(None)

    def add_block(self, pos):
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
    x_position = NumericProperty(10)
    y_position = NumericProperty(1)
    position = ReferenceListProperty(x_position, y_position)

    def move(self):
        print "Rendered {0} at {1}".format(self.direction, self.position)
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


class Fruit(Widget):
    image = ObjectProperty(None)
    duration = NumericProperty(2)
    interval = NumericProperty(3)

    def pop(self, pos):
        with self.canvas:
            x = (pos[0] - 1) * self.size[0]
            y = (pos[1] - 1) * self.size[1]
            coord = (x, y)
            self.image = Ellipse(pos=coord, size=self.size)

    def remove(self):
        self.canvas.remove(self.image)
        self.image = ObjectProperty(None)


class SnakeGame(Widget):
    snake = ObjectProperty(None)
    fruit = ObjectProperty(None)
    fruit_rythme = NumericProperty(0)
    turn_counter = NumericProperty(0)
    score = NumericProperty(0)
    mov_start_pos = ListProperty()
    mov_current_pos = ListProperty()
    mov_triggered = BooleanProperty(False)
    col_number = 20
    row_number = 10

    def new_snake(self):
        start_position = (
            randint(2, self.col_number - 2), randint(2, self.row_number - 2))
        self.snake.head.position = start_position
        start_direction = randint(1, 4)
        if start_direction == 1:
            self.snake.head.direction = "Up"
        if start_direction == 2:
            self.snake.head.direction = "Down"
        if start_direction == 3:
            self.snake.head.direction = "Left"
        if start_direction == 4:
            self.snake.head.direction = "Right"

    def pop_fruit(self, *args):
        coord = (randint(1, 20), randint(1, 10))
        self.fruit.pop(coord)
        print "Poped ! at {}".format(coord)

    def remove_fruit(self, *args):
        if self.fruit.image:
            self.fruit.remove()

    def update(self, dt):
        if self.turn_counter == 0:
            print "A"
            self.fruit_rythme = self.fruit.interval + self.fruit.duration
            Clock.schedule_interval(self.remove_fruit, self.fruit_rythme / 1)
        elif self.turn_counter == self.fruit.interval:
            print "B"
            self.pop_fruit()
            Clock.schedule_interval(self.pop_fruit, self.fruit_rythme / 1)

        self.snake.move()
        snake_position = self.snake.head.position

        if snake_position in self.snake.tail.blocks_positions:
            print "LOOOSER"

        if snake_position[0] > self.col_number \
                or snake_position[0] < 1 \
                or snake_position[1] > self.row_number \
                or snake_position[1] < 1:
            print "LOOOOOSER AGAIN"

        self.turn_counter += 1

    def on_touch_down(self, touch):
        self.mov_start_pos = touch.spos

    def on_touch_up(self, touch):
        self.mov_triggered = False

    def on_touch_move(self, touch):
        self.mov_current_pos = touch.spos

        delta = Vector(*self.mov_current_pos) - Vector(*self.mov_start_pos)
        if (self.mov_triggered == False) \
                and (abs(delta[0]) > 0.15 or abs(delta[1]) > 0.20):
            if abs(delta[0]) > abs(delta[1]):
                if delta[0] > 0:
                    self.snake.set_next_direction("Right")
                else:
                    self.snake.set_next_direction("Left")
            else:
                if delta[1] > 0:
                    self.snake.set_next_direction("Up")
                else:
                    self.snake.set_next_direction("Down")
            self.mov_triggered = True
            print "Changed direction"


class SnakeApp(App):

    def build(self):
        game = SnakeGame()
        game.new_snake()
        Clock.schedule_interval(game.update, 1.0 / 1)
        return game


if __name__ == "__main__":
    SnakeApp().run()
