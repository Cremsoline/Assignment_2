import turtle

def draw_recursive_edge(length, depth):
    """
    Recursively draws a single edge of the polygon by applying the 
    geometric pattern rules defined in the assignment.
    
    Rules applied:
    1. Each edge is divided into three equal segments.
    2. The middle segment is replaced by an inward-pointing equilateral triangle.
    3. One edge becomes four smaller edges, each 1/3 the original length.
    4. Process repeats until the specified recursion depth is reached.

    Args:
        length (float): The current length of the edge to be drawn.
        depth (int): The current recursion level (0 draws a straight line).
    """
    if depth == 0:
        # Base case: depth is 0, so we just draw a straight line
        turtle.forward(length)
    else:
        # Calculate 1/3 of the length for the new sub-segments
        segment_length = length / 3
        
        # Angles to create an inward-pointing equilateral triangle indentation:
        # 0: move forward, 60: turn left, -120: sharp right, 60: turn back to original path
        for angle in [0, 60, -120, 60]:
            turtle.left(angle)
            # Recursively call the function for each of the 4 new segments
            draw_recursive_edge(segment_length, depth - 1)

def draw_geometric_pattern(sides, length, depth):
    """
    Draws the complete initial polygon and applies the recursive 
    edge transformation to every side of that polygon.

    Args:
        sides (int): The number of sides for the starting shape (e.g., 4 for a square).
        length (float): The length of each side of the initial polygon.
        depth (int): The number of times to apply the recursive pattern rules.
    """
    # Calculate the exterior angle of the polygon
    angle = 360 / sides
    for _ in range(sides):
        draw_recursive_edge(length, depth)
        # Turn to start drawing the next major side of the polygon
        turtle.left(angle)

# --- Coordinate Tracking for Centering ---
# These variables help us calculate the bounding box of the drawing 
# so we can center the final pattern on the screen.
min_x = max_x = min_y = max_y = 0

def update_bounds():
    """Updates the global boundary variables based on the turtle's current position."""
    global min_x, max_x, min_y, max_y
    x, y = turtle.position()
    min_x, max_x = min(min_x, x), max(max_x, x)
    min_y, max_y = min(min_y, y), max(max_y, y)

# Overriding the forward method to automatically track boundaries while drawing
original_forward = turtle.forward
def forward_with_tracking(dist):
    original_forward(dist)
    update_bounds()
turtle.forward = forward_with_tracking

# --- User Input Section ---

sides = int(input("Enter the number of sides: "))
length = float(input("Enter the side length: "))
depth = int(input("Enter the recursion depth: "))

# --- Turtle Environment Setup ---
screen = turtle.Screen()
screen.bgcolor("black")  # Set a high-contrast background
turtle.color("cyan")     # Set the drawing color
turtle.speed(0)          # Set to the fastest animation speed
turtle.hideturtle()      # Hide the cursor for a cleaner look


# We use tracer(0) to perform the calculations instantly without showing them
turtle.penup()
turtle.goto(0, 0)
turtle.tracer(0, 0)
draw_geometric_pattern(sides, length, depth)

# Calculate the center point of the drawn shape
offset_x = (min_x + max_x) / 2
offset_y = (min_y + max_y) / 2

# Second Pass: Draw the Centered Pattern 
turtle.clear()
turtle.penup()
# Start the drawing at a position that centers the pattern relative (0,0)
turtle.goto(-offset_x, -offset_y)
turtle.setheading(0)
turtle.pendown()
turtle.tracer(1, 0)  # Re-enable animation for the final drawing

draw_geometric_pattern(sides, length, depth)

# Keep the window open until the user closes it
turtle.done()