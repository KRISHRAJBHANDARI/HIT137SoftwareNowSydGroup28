import turtle

def draw_koch_segment(t, length, depth):
    """Recursively draw a single Koch segment."""
    if depth == 0:
        t.forward(length)
    else:
        length /= 3
        draw_koch_segment(t, length, depth - 1)
        t.left(60)
        draw_koch_segment(t, length, depth - 1)
        t.right(120)
        draw_koch_segment(t, length, depth - 1)
        t.left(60)
        draw_koch_segment(t, length, depth - 1)

def draw_polygon(t, sides, length, depth):
    """Draw the fractal polygon with Koch-like edges."""
    for _ in range(sides):
        draw_koch_segment(t, length, depth)
        t.right(360 / sides)

def main():
    # User input
    sides = int(input("Enter the number of sides: "))
    length = int(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    # Turtle setup
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)  # fastest speed

    # Draw the fractal polygon
    draw_polygon(t, sides, length, depth)

    # Finish
    turtle.done()

if __name__ == "__main__":
    main()
