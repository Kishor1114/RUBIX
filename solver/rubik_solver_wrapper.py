"""
rubik_solver_wrapper.py

Wrapper that uses the best available solver:

1. Try to use external `rubik_solver` package (preferred when available).
2. If not available or it fails, fall back to local `solver.pure_kociemba` (Python-3.13 compatible).

Exposes:
    solve(facelet_string: str) -> list[str]
"""

import logging

logger = logging.getLogger("rubik_wrapper")
logger.addHandler(logging.NullHandler())

# Try external solver first
try:
    from rubik_solver import utils as external_utils  # type: ignore
    _HAS_EXTERNAL = True
    logger.info("External rubik_solver found; wrapper will use it by default.")
except Exception:
    external_utils = None
    _HAS_EXTERNAL = False
    logger.info("External rubik_solver not available; wrapper will use local fallback.")

# Import local fallback solver
try:
    from . import pure_kociemba as local_solver  # relative import within package
    _HAS_LOCAL = True
    logger.info("Local pure_kociemba solver is available as fallback.")
except Exception as e:
    local_solver = None
    _HAS_LOCAL = False
    logger.exception("Local fallback solver not available: %s", e)


def solve(facelet_string: str, *, use_external_if_available: bool = True):
    """
    Solve the cube and return a list of moves.

    Parameters
    ----------
    facelet_string : str
        54-character facelet string in solver order: U(9), R(9), F(9), D(9), L(9), B(9)
    use_external_if_available : bool
        If True (default) try external `rubik_solver` first when it's installed.

    Returns
    -------
    list[str]
        e.g. ["R", "U", "R'", "U'", "F2", ...]
    """

    if facelet_string is None or len(facelet_string) != 54:
        raise ValueError("facelet_string must be a 54-character string in U,R,F,D,L,B order.")

    # 1) Try external solver if present & allowed
    if use_external_if_available and _HAS_EXTERNAL and external_utils is not None:
        try:
            result = external_utils.solve(facelet_string, "Kociemba")
            # external_utils.solve may return a string or list; normalize:
            if isinstance(result, str):
                moves = result.strip().split()
            elif isinstance(result, (list, tuple)):
                moves = list(result)
            else:
                moves = [str(result)]
            logger.info("Solved using external rubik_solver (moves=%d).", len(moves))
            return _normalize_moves(moves)
        except Exception as e:
            logger.warning("External solver failed; falling back to local solver. Error: %s", e)

    # 2) Use local fallback solver
    if _HAS_LOCAL and local_solver is not None:
        try:
            # Local solver expects only facelet_string; it may accept optional args
            moves = local_solver.solve(facelet_string)
            logger.info("Solved using local pure_kociemba (moves=%d).", len(moves))
            return _normalize_moves(moves)
        except Exception as e:
            logger.exception("Local solver failed: %s", e)
            raise RuntimeError("Both external and local solvers failed.") from e

    # 3) No solver available
    raise RuntimeError(
        "No solver available. Install `rubik-solver` (or `kociemba`) in a compatible Python env "
        "or ensure solver/pure_kociemba.py exists and is importable."
    )


def _normalize_moves(moves):
    """
    Normalize moves into canonical list of strings.
    Accepts various incoming formats and returns e.g. ["R", "U", "R'", "U'"].
    """
    normalized = []
    if moves is None:
        return normalized

    # If moves is a single string with space-separated moves
    if isinstance(moves, str):
        moves = moves.strip().split()

    # Flatten nested lists
    for mv in moves:
        if mv is None:
            continue
        if isinstance(mv, (list, tuple)):
            for sub in mv:
                if sub:
                    normalized.append(str(sub).strip())
        else:
            normalized.append(str(mv).strip())

    # Optional: filter out empty tokens
    normalized = [m for m in normalized if m]

    return normalized
