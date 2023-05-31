import keyboard
import time
import random

grid = []

gridWidth = 10
gridHeight = gridWidth

for y in range(gridHeight):
    row = []
    for x in range(gridWidth):
        row.append(" ")
    grid.append(row)

# Create score variable
score = 0

winScore = gridWidth * 3


def display():
    space()
    print("_" * ((2 * (gridWidth + 1)) + 1))  # Needs work to allow for different grid sizes
    for line in grid:
        print("| ", end="")
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


def space():
    print(40*"\n", end="")


# For the grid's nested loops, first value is y co-ord, second value is x co-ord
# grid[2][2] = "x"

def is_empty(char):
    if char == " ":
        return True
    else:
        return False


def is_rock(char):
    if char == "0":
        return True
    else:
        return False


def get_current_pos(obj):
    for line in grid:
        for char in line:
            if char == obj:
                line_ind = grid.index(line)
                row_ind = line.index(char)
                return [line_ind, row_ind]


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


def generate_obstacle():
    rand_y = random.randrange(gridHeight)
    rand_x = random.randrange(gridWidth)

    if grid[rand_y][rand_x] != "x":
        grid[rand_y][rand_x] = "0"


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


def count_spaces():
    space_count = 0
    for col in grid:
        for r in col:
            for i in r:
                if i == " ":
                    space_count += 1
    return space_count


def main():
    generate_x()
    for i in range(gridWidth):
        generate_obstacle()
    running = True
    while running:
        move_x()
        if excavate_x():
            global score
            score += 1
        # obstacle_trigger()
        generate_obstacle()
        display()
        time.sleep(0.1)
        spaces_left = count_spaces()  # accelerate rocks appearing when there are only a few spaces left
        if spaces_left <= gridWidth:
            generate_obstacle()
        if spaces_left <= (gridWidth // 2):
            generate_obstacle()
        if you_win():
            print("\n" + f"You smashed {winScore} rocks. You win!")
            time.sleep(5)
            running = False
        if you_lose():
            py, px = get_current_pos("x")
            grid[py][px] = "0"
            display()
            print("\nYou lose. Too bad...")
            time.sleep(5)
            running = False


def intro():
    text = ["Welcome to Excavate.\n",
            "You're in a remote cave,", "with no-one around for miles.\n",
            "Rocks are falling all around you.\n",
            "You have no choice but to smash your way out,", "with your trusty pickaxe.\n",
            "If the cave fills up with rocks,", "you're not getting out alive.\n",
            "Use WASD to move.\n",
            "Press I to smash rocks.\n",
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


# def play_again_or_quit():
#     quit_codes = ["Q", "QUIT"]
#     play_codes = ["P"]
#
#     user_choice = input("To play again, press P. To quit, press Q.")
#
#     if user_choice.upper in quit_codes:
#         quit()
#     elif user_choice.upper in play_codes:
#         main()


intro()
main()
