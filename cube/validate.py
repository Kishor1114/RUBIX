import logging

logger = logging.getLogger("cube_validator")

VALID_FACES = ["U", "R", "F", "D", "L", "B"]


def validate_facelet_string(s: str) -> bool:
    """
    Validates a 54-character Rubik’s Cube facelet string.
    """

    if s is None:
        logger.error("Facelet string is None.")
        return False

    if len(s) != 54:
        logger.error(f"Invalid length: {len(s)} (expected 54)")
        return False

    # Check allowed characters
    for ch in s:
        if ch not in VALID_FACES:
            logger.error(f"Invalid facelet character detected: '{ch}'")
            return False

    # Count occurrences
    counts = {f: 0 for f in VALID_FACES}
    for ch in s:
        counts[ch] += 1

    # Ensure each color appears exactly 9 times
    for face, count in counts.items():
        if count != 9:
            logger.error(f"Color '{face}' count invalid: {count} (expected 9)")
            return False

    # Validate centers
    center_positions = {
        "U": s[4],
        "R": s[13],
        "F": s[22],
        "D": s[31],
        "L": s[40],
        "B": s[49],
    }

    if len(set(center_positions.values())) != 6:
        logger.error("Center colors conflict — cube physically impossible.")
        logger.error(f"Centers detected: {center_positions}")
        return False

    logger.info("Cube validation successful.")
    return True


# ✅ NEW: wrapper expected by backend
def validate_cube(cube):
    """
    Backend-friendly validator.
    Accepts Cube object and validates its facelet string.
    """

    if not hasattr(cube, "facelets"):
        raise ValueError("Invalid Cube object: missing 'facelets'")

    is_valid = validate_facelet_string(cube.facelets)

    if not is_valid:
        raise RuntimeError("Cube validation failed")

    return True
