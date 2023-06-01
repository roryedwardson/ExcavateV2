import keyboard
import time
import random

# Generate grid
grid = []

gridWidth = 10
gridHeight = gridWidth

for y in range(gridHeight):
    row = []
    for x in range(gridWidth):
        row.append(" ")
    grid.append(row)

# For the grid's nested loops, first value is y co-ord, second value is x co-ord
# For example, grid[3][2] = "x"

# Create score and winScore variables
score = 0
winScore = gridWidth * 3



# Display current state of grid to user, with top, bottom and side borders
def display():
    space()
    # print((" " * 7) + "EXCAVATE!")
    print((" " * 7) + f"Target: {winScore}")
    print("_" * ((2 * (gridWidth + 1)) + 1))  # Needs work to allow for different grid sizes
    for line in grid:
        print("| ", end="")
        # Tried range() and len() but neither worked, so implemented this counter to add | to end of each row.
        ln_counter = 0
        for i in line:
            if ln_counter < gridWidth - 1:
                print(i, "", end="")
                ln_counter += 1
            elif ln_counter == gridWidth - 1:
                print(i, "|", end="")

        print("")
        # print(line)
    print(("‾" * ((2 * (gridWidth + 1)) + 1)))
    print((" " * ((3 * gridWidth) // 2) + f"Score: {score}"))
    # Needs work to allow for different grid sizes, see above...


def space():  # Generate numerous empty lines, so that grid remains onscreen in same position
    print(40*"\n", end="")


def is_empty(char):  # Check if a given position is empty
    if char == " ":
        return True
    else:
        return False


def is_rock(char):  # Check if a given position contains a rock
    if char == "0":
        return True
    else:
        return False


# Return coordinates of the location of a given unique string (in this case, "x")
def get_current_pos(obj):
    for line in grid:
        for char in line:
            if char == obj:
                line_ind = grid.index(line)
                row_ind = line.index(char)
                return [line_ind, row_ind]


# Accept keyboard input with WASD to move "x" around the grid to any valid empty space
def move_x():
    if grid[0][0] == "x":  # Workaround to prevent x being stuck at [0][0]
        if keyboard.is_pressed('s'):  # Move down
            down_pos = grid[1][0]
            if is_empty(down_pos):
                grid[0][0] = " "
                grid[1][0] = "x"
        elif keyboard.is_pressed('d'):  # Move right
            right_pos = grid[0][1]
            if is_empty(right_pos):
                grid[0][0] = " "
                grid[0][1] = "x"

    line_ind, row_ind = get_current_pos("x")

    if keyboard.is_pressed('w'):  # Move up
        if line_ind > 0:  # Check for top of grid
            up_pos = grid[line_ind - 1][row_ind]
            if is_empty(up_pos):  # Check for empty space
                grid[line_ind][row_ind] = " "
                line_ind -= 1
                grid[line_ind][row_ind] = "x"
    elif keyboard.is_pressed('s'):  # Move down
        if line_ind < gridHeight - 1:  # Check for bottom of grid
            down_pos = grid[line_ind + 1][row_ind]
            if is_empty(down_pos):  # Check for empty space
                grid[line_ind][row_ind] = " "
                line_ind += 1
                grid[line_ind][row_ind] = "x"
    elif keyboard.is_pressed('a'):  # Move left
        if row_ind > 0:  # Check for left side of grid
            left_pos = grid[line_ind][row_ind - 1]
            if is_empty(left_pos):  # Check for empty space
                grid[line_ind][row_ind] = " "
                row_ind -= 1
                grid[line_ind][row_ind] = "x"
    elif keyboard.is_pressed('d'):  # Move right
        if row_ind < gridWidth - 1:  # Check for right side of grid
            right_pos = grid[line_ind][row_ind + 1]
            if is_empty(right_pos):  # Check for empty space
                grid[line_ind][row_ind] = " "
                row_ind += 1
                grid[line_ind][row_ind] = "x"


# Accept keyboard input I to destroy a rock adjacent to "x"
def excavate_x():
    y_ind, x_ind = get_current_pos("x")

    # check is_pressed
    if keyboard.is_pressed("i"):

        # check above for "0"
        if y_ind > 0:  # Check for top of grid
            if is_rock(grid[y_ind - 1][x_ind]):  # Check for rock
                grid[y_ind - 1][x_ind] = " "  # Destroy rock
                return True

        # check below for "0"
        if y_ind < gridHeight - 1:  # Check for bottom of grid
            if is_rock(grid[y_ind + 1][x_ind]):  # Check for rock
                grid[y_ind + 1][x_ind] = " "  # Destroy rock
                return True

        # check left for "0"
        if x_ind > 0:  # Check for left side of grid
            if is_rock(grid[y_ind][x_ind - 1]):  # Check for rock
                grid[y_ind][x_ind - 1] = " "  # Destroy rock
                return True

        # check right for "0"
        if x_ind < gridWidth - 1:  # Check for right side of grid
            if is_rock(grid[y_ind][x_ind + 1]):  # Check for empty space
                grid[y_ind][x_ind + 1] = " "  # Destroy rock
                return True

    else:
        return False


# Set initial position of x using random integers
def generate_x():
    random_y = random.randrange(0, gridHeight)
    random_x = random.randrange(0, gridWidth)

    grid[random_y][random_x] = "x"


# Create a rock at random coordinates (excluding the position of "x")
# def generate_obstacle():
#     rand_y = random.randrange(gridHeight)
#     rand_x = random.randrange(gridWidth)
#
#     if grid[rand_y][rand_x] != "x":
#         grid[rand_y][rand_x] = "0"

# Get list of available spaces, and create a rock at a random choice from that list
def generate_obstacle():
    spaces = get_spaces()
    if len(spaces) > 0:
        random_space = random.choice(spaces)

        rand_y = random_space[0]
        rand_x = random_space[1]

        grid[rand_y][rand_x] = "0"


# Testing/debug function to manually generate a rock via keyboard command
def obstacle_trigger():
    if keyboard.is_pressed("o"):
        generate_obstacle()


# Check for win state, which occurs when score reaches winScore.
def you_win():
    if score == winScore:
        return True
    else:
        return False


# Check for lose state, which occurs when there are no empty spaces left in grid.
def you_lose():
    if any(" " in z for z in grid):
        return False
    else:
        return True


# Count the number of empty spaces remaining in the grid
def count_spaces():
    space_count = 0
    for col in grid:
        for r in col:
            for i in r:
                if i == " ":
                    space_count += 1
    return space_count


# Get list of coordinates which are currently empty spaces, to streamline rock generation
def get_spaces():
    space_list = []
    for col in grid:
        for r in col:
            for i in r:
                if i == " ":
                    col_ind = grid.index(col)
                    r_ind = col.index(r)
                    space_list.append([col_ind, r_ind])
    return space_list

    # return y, x


def x_exists():
    for col in grid:
        for r in col:
            for i in r:
                if i == "x":
                    return True
                else:
                    return False


def reset():
    # Reset score to zero
    global score
    score = 0
    # Reset all rocks to spaces, reset current x to space
    for col in grid:
        for r in col:
            for i in r:
                if i == "0":
                    col_ind = grid.index(col)
                    r_ind = col.index(r)
                    grid[col_ind][r_ind] = " "
                elif i == "x":
                    col_ind = grid.index(col)
                    r_ind = col.index(r)
                    grid[col_ind][r_ind] = " "
    # Call main()
    main()


# Main function, containing while loop with display() screen refreshes
def main():
    if not x_exists():
        generate_x()
    for i in range(gridWidth):
        generate_obstacle()
    running = True
    while running:
        # Check for win or lose state on every refresh
        if you_win():
            print("\n" + f"You win!")
            play_again()
        if you_lose():
            py, px = get_current_pos("x")
            grid[py][px] = "0"
            display()
            space()
            print(dead, end="")
            print("\nYou lose. Too bad...")
            generate_x()
            play_again()

        # Accept WASD and I input to move "x" and smash rocks
        move_x()
        if excavate_x():
            global score
            score += 1
        # obstacle_trigger()  # testing/debug tool, commented out
        generate_obstacle()
        display()
        time.sleep(0.12)  # Game speed / refresh rate

        # Accelerate rocks appearing when there are only a few spaces left
        spaces_left = count_spaces()
        if spaces_left <= gridWidth:
            generate_obstacle()
        if spaces_left <= (gridWidth // 2):
            generate_obstacle()


title = r"""======  \\   // //===\\   //=\\   ||    ||   //=\\   ======== ======
||       \\ //  ||       //   \\  ||    ||  //   \\     ||    ||
======    ===   ||      ||=====|| ||    || ||=====||    ||    ======
||       // \\  ||      ||     ||  \\  //  ||     ||    ||    ||
======  //   \\ \\===// ||     ||   \\//   ||     ||    ||    ======
"""

dead = r"""_______________________
| 0 0 0 0 0 0 0 0 0 0 |
| 0 0/‾‾‾‾‾‾‾‾‾‾‾\0 0 |
| 0 /             \ 0 |
| 0|   ()  _   ()  |0 |
| 0 \     / \     / 0 |
| 0 0\    ‾‾‾    /0 0 |
| 0 0 |         | 0 0 |
| 0 0 |_|_|_|_|_| 0 0 |
| 0 0 0 0 0 0 0 0 0 0 |
| 0 0 0 0 0 0 0 0 0 0 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"""


# Introductory text
def intro():
    text = [f"Welcome to \n{title}\n",
            "You're in a remote cave,", "with no-one around for miles.\n",
            "Rocks are falling all around you.\n",
            "You have no choice but to smash your way out,", "with the help of your trusty pickaxe.\n",
            "If the cave fills up with rocks,", "you're not getting out alive.\n",
            "Use WASD to move.\n",
            "Hold I to smash rocks.\n",
            f"Score {winScore} to win.\n"]

    for line in text:
        print(line, end="\n")
        time.sleep(2)

    countdown = ["Starting in 3...\n",
                 "2...\n",
                 "1...\n"]

    for line in countdown:
        print(line, end="\n")
        time.sleep(1)


def play_again():  # Simplified this to get it working. Any user input will reset the programme.
    input("Press enter to play again:")
    reset()

    # print("To play again, press P. To quit, press Q.")
    # while True:
    #     if keyboard.is_pressed("p"):
    #         reset()  # works after win state, does not work after lose state
    #     elif keyboard.is_pressed("q"):
    #         quit()  # works


# Call intro and main functions to initiate programme
intro()
main()
