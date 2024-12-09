import turtle
import colorsys as color
turtle.bgcolor("black")
turtle.title("studymuch")
turtle.tracer(2)
h = 0.4

for i in range(90):
    c = color.hsv_to_rgb(h,1,1)
    h += 0.005
    turtle.width(4)
    turtle.color(c)
    turtle.fillcolor("black")
    turtle.begin_fill()
    turtle.fd(i)
    turtle.circle(20, steps=4)
    turtle.fd(i)
    turtle.right(72)
    turtle.fd(i)
    turtle.end_fill()
    turtle.fd(i)
    turtle.right(1)
turtle.done()

