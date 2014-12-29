from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import OptionProperty, ObjectProperty
from kivy.clock import Clock

class SnakeHead(Widget):
    direction = OptionProperty("Right", options=["Up", "Down", "Left", "Right"])

    def move(self):
        self.x += 10

class SnakeGame(Widget):
    snake = ObjectProperty(None)

    def update(self, dt):
        self.snake.move()





class SnakeApp(App):

    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1.0 / 2)
        return game


if __name__ == "__main__":
    SnakeApp().run()
