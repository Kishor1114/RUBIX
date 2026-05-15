import time
import logging

logger = logging.getLogger("display_solution")


def show_solution(moves):
    """
    Display the solution moves to the user.

    Input:
        moves → list of strings, e.g. ["R", "U", "R'", "U'", "F2"]

    This function:
      - prints total move count
      - prints step-by-step instructions
      - optional small delay between steps (off by default)
    """

    if not moves or len(moves) == 0:
        print("\nThe cube is already solved!\n")
        return

    print("\n==================== SOLUTION ====================\n")

    print(f"Total moves: {len(moves)}\n")
    print("Moves sequence:")
    print(" ".join(moves))
    print("\nStep-by-step:")

    # Smooth readable delay (you can turn it off if needed)
    delay = 0.3

    for i, move in enumerate(moves, start=1):
        line = f"{i:02d}. {move}"
        print(line)
        time.sleep(delay)

    print("\n===================================================")
    print("Cube solved. Follow the steps above.")
