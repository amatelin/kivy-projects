from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import OptionProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock

class SnakeHead(Widget):
    direction = OptionProperty("Right", options=["Up", "Down", "Left", "Right"])
    velocity = NumericProperty(0)

    def move(self):
        self.x += self.velocity

class SnakeGame(Widget):
    snake = ObjectProperty(None)

    def update(self, dt):
        self.snake.move()

        # out of bounds
        if self.snake.x < self.x or self.snake.x > self.width \
        or self.snake.y < self.y or self.snake.y > self.height:
            self.snake.velocity *= -1





class SnakeApp(App):

    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1.0 / 5)
        return game


if __name__ == "__main__":
    SnakeApp().run()
