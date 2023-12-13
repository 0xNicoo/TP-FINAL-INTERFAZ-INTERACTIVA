import cv2
import pyglet
import math

from pyglet.window import mouse
from hand_detector import HandDetector

#WEBCAM CONFIG
webcam = cv2.VideoCapture(0)
webcam_width  = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
webcam_height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)

#PYGLET CONFIG
window = pyglet.window.Window(int(webcam_width), int(webcam_height))
circles = []
circle_cursor = pyglet.shapes.Circle(x=0, y=0, radius=10, color=(255, 0, 0))

palette = []
palette.append(pyglet.shapes.Circle(x=50, y=int(webcam_height)-50, radius=20, color=(255, 0, 0)))#RED
palette.append(pyglet.shapes.Circle(x=50, y=int(webcam_height)-100, radius=20, color=(0, 255, 0)))#GREN
palette.append(pyglet.shapes.Circle(x=50, y=int(webcam_height)-150, radius=20, color=(0, 0, 255)))#BLUE
palette.append(pyglet.shapes.Circle(x=50, y=int(webcam_height)-200, radius=20, color=(255, 255, 0)))#YELLOW
palette.append(pyglet.shapes.Circle(x=50, y=int(webcam_height)-250, radius=20, color=(0, 255, 255)))#CYAN
palette.append(pyglet.shapes.Circle(x=50, y=int(webcam_height)-300, radius=20, color=(255, 0, 255)))#MAGENTA
palette.append(pyglet.shapes.Circle(x=50, y=int(webcam_height)-350, radius=20, color=(255, 255, 255)))#WHITE
goma_hitbox = pyglet.shapes.Circle(x=50, y=int(webcam_height)-420, radius=30, color=(100, 100, 100))
goma_hitbox.visible = False
palette.append(goma_hitbox)

goma = pyglet.sprite.Sprite(img=pyglet.image.load('images/goma.png'))
goma_cursor = pyglet.sprite.Sprite(img=pyglet.image.load('images/goma.png'))
goma_cursor.width = 60
goma_cursor.height = 60
goma_cursor.visible = False

goma.x = 23
goma.y = int(webcam_height)-450
goma.width = 60
goma.height = 60

detector = HandDetector()

@window.event
def on_draw():
    window.clear()

    goma.draw()

    circle_cursor.x, circle_cursor.y = read_webcam()
    goma_cursor.x = circle_cursor.x - 35
    goma_cursor.y = circle_cursor.y - 40
    

    if(detector.hand_drawing):
        circle = pyglet.shapes.Circle(x=circle_cursor.x, y=circle_cursor.y, radius=10, color=circle_cursor.color)
        circles.append(circle)

    for figure in circles:
        figure.draw()

    for color in palette:
        if(is_picking_color(color, circle_cursor) and detector.hand_close):
            if color.color == (100, 100, 100, 255):
                goma_cursor.visible = True
                circle_cursor.visible = False
                circle_cursor.color = (0,0,0,255)
            else:
                goma_cursor.visible = False
                circle_cursor.visible = True
                circle_cursor.color = color.color
        color.draw() 

    circle_cursor.draw()
    goma_cursor.draw()

def read_webcam():
    success, campured_img = webcam.read()
    campured_img = cv2.flip(campured_img, -1)
    cv2.cvtColor(campured_img, cv2.COLOR_BGR2RGB)
    return detector.findHands(img=campured_img)

def is_picking_color(color, cursor):
    distance = math.sqrt((cursor.x - color.x)**2 + (cursor.y - color.y)**2)
    return True if distance < cursor.radius + color.radius else False

pyglet.app.run()
webcam.release()