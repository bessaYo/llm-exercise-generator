import os
import shutil

"""
Configuration for code compilation checks.

The path is used to locate the `runghc` executable, which is needed to
automatically compile and test Haskell code blocks during evaluation.

Resolution order:
  1. The RUNGHC_PATH environment variable, if set.
  2. The `runghc` executable found in the system PATH.
  3. A fallback default (typical ghcup install location).
"""

# Fallback if runghc is neither configured nor on the PATH
DEFAULT_RUNGHC_PATH = os.path.expanduser("~/.ghcup/bin/runghc")

# Prefer an explicit override, then the system PATH, then the default
RUNGHC_PATH = (
    os.getenv("RUNGHC_PATH") or shutil.which("runghc") or DEFAULT_RUNGHC_PATH
)
