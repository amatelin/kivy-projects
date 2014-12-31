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
from kivy.graphics import Rectangle


class Snake(Widget):
    head = ObjectProperty(None)
    tail = ObjectProperty(None)

    def move(self):
        next_tail_pos = list(self.head.position)
        self.head.move()
        self.head.render()
        self.tail.add_block(next_tail_pos)
        self.tail.render()

    def set_next_direction(self, direction):
        self.head.next_direction = direction

class SnakeTail(Widget):
    tail_size = NumericProperty(5)
    blocks_positions = ListProperty()
    tail_blocks = ListProperty()
    block = ObjectProperty(None)

    def add_block(self, pos):
        self.blocks_positions.append(pos)
        if len(self.blocks_positions)>self.tail_size:
            self.blocks_positions.pop(0)
        print self.blocks_positions

    def render(self):
        with self.canvas:
            for block_pos in self.blocks_positions:
                x = (block_pos[0]-0.5)*self.width
                y = (block_pos[1]-0.5)*self.height
                coord = (x, y)
                block = Rectangle(pos=coord, size=(self.width, self.height))
                self.tail_blocks.append(block)
                if len(self.tail_blocks)>self.tail_size:
                    last_block = self.tail_blocks.pop(0)
                    self.canvas.remove(last_block)
                print self.tail_blocks

class SnakeHead(Widget):
    direction = OptionProperty(
        "Right", options=["Up", "Down", "Left", "Right"])
    next_direction = OptionProperty(
        "Right", options=["Up", "Down", "Left", "Right"])
    points = ListProperty([0] * 6)
    x_position = NumericProperty(10)
    y_position = NumericProperty(10)
    position = ReferenceListProperty(x_position, y_position)

    def move(self):
        self.direction = self.next_direction
        if self.direction == "Right": 
            self.position[0] += 1
        elif self.direction == "Left":
            self.position[0] -= 1
        elif self.direction == "Up":
            self.position[1] += 1
        elif self.direction == "Down":
            self.position[1] -= 1
        print "Moved {0} at {1}".format(self.direction, self.position)

    def render(self):
        print "Rendered {0} at {1}".format(self.direction, self.position)
        if self.direction == "Right":
            x0 = self.position[0] * self.width
            y0 = (self.position[1] - 0.5) * self.height
            x1 = x0 - self.width
            y1 = y0 + self.height / 2
            x2 = x0 - self.width
            y2 = y0 - self.height / 2
        elif self.direction == "Left":
            x0 = (self.position[0] - 1) * self.width
            y0 = (self.position[1] - 0.5) * self.height
            x1 = x0 + self.width
            y1 = y0 - self.height / 2
            x2 = x0 + self.width
            y2 = y0 + self.height / 2
        elif self.direction == "Up":
            x0 = (self.position[0] - 0.5) * self.width
            y0 = self.position[1] * self.height
            x1 = x0 - self.width / 2
            y1 = y0 - self.height
            x2 = x0 + self.width / 2
            y2 = y0 - self.height
        elif self.direction == "Down":
            x0 = (self.position[0] - 0.5) * self.width
            y0 = (self.position[1] - 1) * self.height
            x1 = x0 + self.width / 2
            y1 = y0 + self.height
            x2 = x0 - self.width / 2
            y2 = y0 + self.height

        self.points = [x0, y0, x1, y1, x2, y2]
        # print self.points


class SnakeGame(Widget):
    snake = ObjectProperty(None)
    # snake_head = ObjectProperty(None)
    # tail_block_template = ObjectProperty(None)
    # tail_position = ListProperty()
    score = NumericProperty(0)
    mov_start_pos = ListProperty()
    mov_current_pos = ListProperty()
    mov_triggered = BooleanProperty(False)

    def new_snake(self):
        pass

    def update(self, dt):
        self.snake.move()

        # out of bounds
        if self.snake.x < self.x or self.snake.x > self.width \
                or self.snake.y < self.y or self.snake.y > self.height:
            self.direction = "Right"

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
        Clock.schedule_interval(game.update, 1.0 / 1)
        return game


if __name__ == "__main__":
    SnakeApp().run()
