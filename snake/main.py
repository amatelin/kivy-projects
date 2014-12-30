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


class SnakeHead(Widget):
    direction = OptionProperty(
        "Right", options=["Up", "Down", "Left", "Right"])
    next_direction = OptionProperty(
        "Right", options=["Up", "Down", "Left", "Right"])
    points = ListProperty([0] * 6)
    x_position = NumericProperty(0)
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
    score = NumericProperty(0)
    mov_start_pos = ListProperty()
    mov_current_pos = ListProperty()
    mov_triggered = BooleanProperty(False)

    def new_snake(self):
        pass

    def update(self, dt):
        self.snake.move()
        self.snake.render()

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
                    self.snake.next_direction = "Right"
                else:
                    self.snake.next_direction = "Left"
            else:
                if delta[1] > 0:
                    self.snake.next_direction = "Up"
                else:
                    self.snake.next_direction = "Down"
            self.mov_triggered = True
            print "Changed direction"


class SnakeApp(App):

    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1.0 / 1)
        return game


if __name__ == "__main__":
    SnakeApp().run()
