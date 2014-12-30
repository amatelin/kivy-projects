from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import OptionProperty, ObjectProperty, NumericProperty, ReferenceListProperty, ListProperty
from kivy.clock import Clock
from kivy.vector import Vector

class SnakeHead(Widget):
    direction = OptionProperty("Right", options=["Up", "Down", "Left", "Right"])
    points = ListProperty([0]*6)
    x_position = NumericProperty(0)
    y_position = NumericProperty(1)
    position = ReferenceListProperty(x_position, y_position)

    def move(self):
        if self.direction=="Right":
            self.position[0]+=1
            x0 = self.position[0]*self.width
            y0 = self.position[1]*self.height/2
            x1 = x0-self.width
            y1 = y0+self.height/2
            x2 = x0-self.width
            y2 = y0-self.height/2
        elif self.direction=="Left":
            self.position[0]-=1
            x0 = (self.position[0]-1)*self.width
            y0 = self.position[1]*self.height/2
            x1 = x0+self.width
            y1 = y0-self.height/2
            x2 = x0+self.width
            y2 = y0+self.height/2  
        elif self.direction=="Up":
            self.position[1]+=1
            x0 = self.position[0]*self.width/2
            y0 = self.position[1]*self.height
            x1 = x0-self.width/2
            y1 = y0-self.height
            x2 = x0+self.width/2
            y2 = y0-self.height  
        elif self.direction=="Down":
            self.position[1]-=1
            x0 = self.position[0]*self.width/2
            y0 = (self.position[1]-1)*self.height
            x1 = x0+self.width/2
            y1 = y0+self.height
            x2 = x0-self.width/2
            y2 = y0+self.height 

        self.points = [x0, y0, x1, y1, x2, y2]

class SnakeGame(Widget):
    snake = ObjectProperty(None)
    score = NumericProperty(0)

    def new_snake(self):
        pass


    def update(self, dt):
        self.snake.move()

        # out of bounds
        if self.snake.x < self.x or self.snake.x > self.width \
        or self.snake.y < self.y or self.snake.y > self.height:
            self.direction = "Right"





class SnakeApp(App):

    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1.0 / 1)
        return game


if __name__ == "__main__":
    SnakeApp().run()
