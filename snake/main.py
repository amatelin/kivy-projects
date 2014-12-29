from kivy.app import App
from kivy.uix.widget import Widget


class SnakeGame(Widget):
    pass


class SnakeApp(App):

    def build(self):
        game = SnakeGame()
        return game


if __name__ == "__main__":
    SnakeApp().run()
