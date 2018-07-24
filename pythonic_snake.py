from tkinter import Tk, Canvas
import random

# screen width
WIDTH = 600
# screen height
HEIGHT = 400
# snake's segment size
SEG_SIZE = 20
# game status
IN_GAME = True

score = 0


# Helper functions
def create_apple():  # create apple in random position
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)

    # BLOCK is a red circle (apple)
    BLOCK = c.create_oval(posx, posy,
                          posx + SEG_SIZE,
                          posy + SEG_SIZE,
                          fill="red")

def main():
    global IN_GAME
    global score
    if IN_GAME:
        # moves snake
        s.move()
        # Your score
        c.create_text(50, 10, text="Your score: " + str(score), font="Arial 10", fill="#ff0000")
        # define head coordinates
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # GAME OVER when collides with borders
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # eating apples
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            score += 1
            c.create_rectangle(0, 0, 100, 15, fill="black")
            c.create_text(50, 10, text="Your score: " + str(score), font="Arial 10", fill="#ff0000")
            create_apple()

        # self-eating
        else:
            # loop all snake segments
            for i in range(len(s.segments) - 1):
                if c.coords(s.segments[i].instance) == head_coords:
                    IN_GAME = False
        root.after(100, main)
    # GAME OVER
    else:
        c.create_text(WIDTH / 2, HEIGHT / 2,
                      text="GAME OVER!",
                      font="Arial 20",
                      fill="#ff0000")


class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="white")


class Snake(object):
    def __init__(self, segments):
        self.segments = segments

        # available snake moves
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0), "Right": (1, 0)}

        self.disallowedDirectionChanges = [
            ("Down", "Up"),
            ("Up", "Down"),
            ("Right", "Left"),
            ("Left", "Right"),
        ]

        # initial movement direction
        self.vector = self.mapping["Right"]

    def move(self):  # moves the snake
        # loop all segments except the first one
        for i in range(len(self.segments)-1):
            segment = self.segments[i].instance
            x1, y1, x2, y2 = c.coords(self.segments[i+1].instance)
            # for every segment set the coordinates of segment after it
            c.coords(segment, x1, y1, x2, y2)

        # segment coordinates behind the head
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)

        # set head in the same direction as in the move vector
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0]*SEG_SIZE,
                 y1 + self.vector[1]*SEG_SIZE,
                 x2 + self.vector[0]*SEG_SIZE,
                 y2 + self.vector[1]*SEG_SIZE)

    def change_direction(self, event):  # change snake's move directions
        # event == symbol of pressed button
        # change direction if this button is in available directions
        if event.keysym in self.mapping:
            for pair in self.disallowedDirectionChanges:
                if self.vector == self.mapping[pair[0]] and event.keysym == pair[1]:
                    return 0
            self.vector = self.mapping[event.keysym]

    def add_segment(self):  # add snake segment
        # define the last segment
        last_seg = c.coords(self.segments[0].instance)
        # define coordinates where to set the next segment
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        # insert one more segment in defined coordinates
        self.segments.insert(0, Segment(x, y))


# create window
root = Tk()
# set window name
root.title("Snake")

# create class instance Canvas and set background
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
c.grid()
# set focus on Canvas for catching keypress
c.focus_set()
# creating segments and snake
segments = [Segment(SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE*2, SEG_SIZE),
            Segment(SEG_SIZE*3, SEG_SIZE)]
s = Snake(segments)
# Reaction on keypress
c.bind("<KeyPress>", s.change_direction)

create_apple()
main()
# run window
root.mainloop()
