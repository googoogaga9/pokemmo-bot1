import pyautogui
import time
import random
from enum import Enum

# Constants
LEFT_KEY = 'a'
RIGHT_KEY = 'd'
UP_KEY = 'w'
DOWN_KEY = 's'
INTERACT_KEY = 'e'
TIME_PER_SPACE = 0.16
TIME_TO_TURN = 0.105

class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

DIRECTION_FACING = Direction.DOWN

def wait(min_wait=0, max_wait=0.1):
    """Wait for a random number of seconds between min_wait and max_wait."""
    time.sleep(random.uniform(min_wait, max_wait))

def turn(direction_enum):
    """Turn to face the specified direction."""
    global DIRECTION_FACING
    if DIRECTION_FACING != direction_enum:
        print(f"Turning from {DIRECTION_FACING} to {direction_enum}")
        DIRECTION_FACING = direction_enum
        time.sleep(TIME_TO_TURN)

def move(direction_key, direction_enum, spaces=1):
    """Move in a specified direction a certain number of spaces."""
    turn(direction_enum)
    print(f"Moving {direction_enum} for {spaces} spaces")
    pyautogui.keyDown(direction_key)
    time.sleep(TIME_PER_SPACE * spaces)
    pyautogui.keyUp(direction_key)
    wait(0.05, 0.1)  # Reduced wait time between actions for smoother movement

def move_left(spaces=1):
    move(LEFT_KEY, Direction.LEFT, spaces)

def move_right(spaces=1):
    move(RIGHT_KEY, Direction.RIGHT, spaces)

def move_up(spaces=1):
    move(UP_KEY, Direction.UP, spaces)

def move_down(spaces=1):
    move(DOWN_KEY, Direction.DOWN, spaces)

def run_from_pc_to_grass():
    move_down(5)
    wait(1, 1.5)
    move_down(1)
    move_left(5)
    move_up(10)
    move_left(25)
    move_down(6)
    move_left(7)
    move_up(1)

def run_from_grass_to_pc():
    move_down(1)
    move_right(7)
    move_up(6)
    move_right(25)
    move_down(10)
    move_right(5)
    move_up(2)
    wait(1, 1.5)
    move_up(4)

def heal_at_pc():
    move_up(1)
    pyautogui.keyDown(INTERACT_KEY)
    time.sleep(5.5)
    pyautogui.keyUp(INTERACT_KEY)
    move_down(1)

def run_1_2():
    move_up(8)
    move_down(8)

def walk_up_down():
    """Walk up 5 steps and then down 5 steps."""
    move_up(5)
    move_down(5)

def run_back_and_forth():
    step_right = 0
    while True:
        step_left = random.choice([0, 1, 2, 3])
        move_left(step_left + step_right)
        step_right = random.choice([0, 1, 2, 3])
        move_right(step_right + step_left)

def follow_path():
    while True:
        run_to_poke_mart()
        run_to_pc()

def run_to_poke_mart():
    dx1 = 0
    dy1 = 0
    move_down(5)
    wait(1, 1.5)
    move_right(5 + dx1)
    move_up(6 + dy1)
    move_right(5 - dx1)
    move_up(2 - dy1)
    wait(1, 1.5)
    move_up(4)

def run_to_pc():
    dx2 = 0
    dy2 = 0
    move_down(5)
    wait(1, 1.5)
    move_left(5 + dx2)
    move_down(8 + dy2)
    move_left(5 - dx2)
    move_up(2 - dy2)
    wait(1, 1.5)
    move_up(4)

def locate_pokemon_on_screen(pokemon_images, confidence=0.99):
    for pokemon, image in pokemon_images.items():
        try:
            if pyautogui.locateOnScreen(image, confidence=confidence, region=(0, 0, 700, 400)):
                return pokemon
        except pyautogui.ImageNotFoundException:
            pass
    return None

def check_for_pokemon(pokemon_images, timeout=2):
    start_time = time.time()
    while time.time() - start_time < timeout:
        pokemon = locate_pokemon_on_screen(pokemon_images)
        if pokemon:
            print(f"You are facing a {pokemon}!")
            return pokemon
        time.sleep(0.1)
    print("No pokemon found.")
    return None

def pokemon_still_alive(pokemon_images, min_alive_time=2):
    start_time = time.time()
    while time.time() - start_time < min_alive_time:
        if locate_pokemon_on_screen(pokemon_images):
            return True
        time.sleep(0.1)
    return False

def fight_pokemon():
    pyautogui.press(INTERACT_KEY)
    wait(0.1, 0.2)
    pyautogui.press(INTERACT_KEY)

def run_through_grass():
    step_right = 0
    for _ in range(1):
        step_left = random.choice([2, 3])
        move_left(step_left + step_right)
        step_right = random.choice([2, 3])
        move_right(step_right + step_left)

def xp_grind():
    pokemon_images = {
        "Ponyta": "screenshots/8.png",
        "Rattata": "screenshots/9.png",
        "Spearow": "screenshots/10.png",
        "Mankey": "screenshots/11.png",
        "Nidoran Male": "screenshots/12.png",
        "Nidoran Female": "screenshots/13.png",
        "Doduo": "screenshots/14.png"
    }
    
    while True:
        run_through_grass()
        found_pokemon = check_for_pokemon(pokemon_images)
        if found_pokemon:
            while pokemon_still_alive(pokemon_images):
                fight_pokemon()
                wait(3, 4)
            print(f"Defeated {found_pokemon}!")

def main_menu():
    options = {
        "0": ("Exit Program", None),
        "1": ("Run back and forth", run_back_and_forth),
        "2": ("Follow path", follow_path),
        "3": ("XP Grind", xp_grind),
        "4": ("Run from PC to Grass", run_from_pc_to_grass),
        "5": ("Run from Grass to PC", run_from_grass_to_pc),
        "6": ("Heal at PC", heal_at_pc),
        "7": ("Run 1 2", run_1_2),
        "8": ("Walk Up 5 Then Down 5", walk_up_down)
    }

    while True:
        print("Select an option:")
        for key, (description, _) in options.items():
            print(f"{key}. {description}")

        choice = input("Enter your choice: ")

        if choice in options:
            if choice == "0":
                print("Exiting the program.")
                break

            print(f"Starting '{options[choice][0]}' in 5 seconds. Press Ctrl+C to stop.")
            time.sleep(5)
            try:
                options[choice][1]()
            except KeyboardInterrupt:
                print(f"{options[choice][0]} stopped by user.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()



