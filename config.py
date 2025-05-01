import shutil

"""
Configuration for code compilation checks.

The path is used to locate the `runghc` executable, which is needed to 
automatically compile and test Haskell code blocks during evaluation.

If `runghc` is not available in your system PATH, set the local path here manually.
"""

# Local path to the runghc executable
DEFAULT_RUNGHC_PATH = "/Users/marcbessa/.ghcup/bin/runghc"

# Try to find the runghc executable in the system PATH, use the default if not found
RUNGHC_PATH = shutil.which("runghc") or DEFAULT_RUNGHC_PATH
