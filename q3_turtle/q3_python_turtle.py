# HIT137 Assignment 2 - Question 3
#
# Group Name: SYDN 28
# Group Members:
# Krish Rajbhandari - S395754
# Noor-E-Sefat Ahmed - S394047
# Mehedi Hasan - S395003
# Suyog Kadariya - S393829
#
# This program draws a recursive geometric pattern (like Koch snowflake edges)
# using Python's turtle graphics.
# It starts with a polygon, and each side is replaced with smaller edges
# depending on the recursion depth.

import turtle

# Function to draw one edge with recursion
def draw_koch_segment(t, length, depth):
    """
    Recursive function:
    - If depth = 0, just draw a straight line
    - If depth > 0, break the edge into 3 parts
        and replace the middle with a "dent-like" (2 triangle sides)
    """
    if depth == 0:
        # Base case to draw straight line
        t.forward(length)
    else:
        # Break the line into 3 smaller parts
        length = length / 3

        # Draw first part
        draw_koch_segment(t, length, depth - 1)

        # Make an indentation (triangle peak)
        t.left(60)
        draw_koch_segment(t, length, depth - 1)
        t.right(120)
        draw_koch_segment(t, length, depth - 1)
        t.left(60)

        # Draw last part
        draw_koch_segment(t, length, depth - 1)

# Function to draw the polygon in all sides
def draw_polygon(t, sides, length, depth):
    """
    Draws a polygon with given number of sides.
    Each side is not straight, but replaced with recursive edges.
    """
    for _ in range(sides):
        draw_koch_segment(t, length, depth)  # draw one edge
        t.right(360 / sides)  # turn angle for next side

def main():
    # Ask the user for input values
    sides = int(input("Enter the number of sides: "))
    length = int(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    # Set up turtle window
    screen = turtle.Screen()
    screen.bgcolor("white")  # background color
    t = turtle.Turtle()
    t.speed(5)  # medium speed so we can see drawing happen

    # Move turtle a bit so drawing looks centered
    t.penup()
    t.goto(-length/2, length/3)
    t.pendown()

    # Draw the fractal polygon
    draw_polygon(t, sides, length, depth)

    # Finish, This keeps the window open until closed by user
    turtle.done()

if __name__ == "__main__":
    main()
