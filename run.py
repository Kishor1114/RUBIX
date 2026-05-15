import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import cv2
import yaml
import logging
from pathlib import Path

from scanner.scan_cube import scan_entire_cube
from solver.rubik_solver_wrapper import solve
from cube.validate import validate_facelet_string
from ui.display_solution import show_solution

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("run_script")

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_configs():
    base = Path(__file__).resolve().parent
    camera_cfg = load_yaml(base / "config" / "camera.yaml")
    colors_cfg = load_yaml(base / "config" / "colors.yaml")
    return camera_cfg, colors_cfg

def main():
    print("\n================ RUBIK'S CUBE SOLVER ================\n")
    print("Make sure you are in good lighting.")
    print("You will scan 6 faces of the cube in this order:")
    print("   F, R, B, L, U, D")
    print("Press SPACE to capture a face.\n")

    camera_cfg, colors_cfg = load_configs()

    facelet_string = scan_entire_cube(camera_cfg, colors_cfg)

    print("\nScanned facelet string:")
    print(facelet_string)

    print("\nValidating cube...")
    if not validate_facelet_string(facelet_string):
        print("\n❌ Validation failed: scanned cube is not a valid configuration.")
        print("Please rescan the cube.")
        return

    print("✔ Cube validated successfully!\n")
    print("Solving cube... please wait.\n")

    moves = solve(facelet_string)

    print("\n================== SOLUTION ==================\n")
    show_solution(moves)
    print("\n🎉 Done! Follow the moves to solve your cube.\n")

if __name__ == "__main__":
    main()
