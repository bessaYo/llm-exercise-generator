import subprocess
import tempfile
import os
import shutil
import re


def has_main_function(code: str) -> bool:
    """Checks whether the given Haskell code contains a main function."""
    return re.search(r"^\s*main\s*=", code, re.MULTILINE) is not None


def append_dummy_main(code: str) -> str:
    """Appends a neutral main function to the code if none is present."""
    if not has_main_function(code):
        return code + "\n\nmain = return ()"
    return code


def check_haskell_code(code: str) -> str:
    """Writes Haskell code to a temporary file, ensures it has a main function, and checks if it compiles using runghc."""
    code = append_dummy_main(code)

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".hs", mode="w", encoding="utf-8"
    ) as f:
        f.write(code)
        file_path = f.name

    runghc_path = shutil.which("runghc")
    if not runghc_path:
        runghc_path = "/Users/marcbessa/.ghcup/bin/runghc"

    try:
        result = subprocess.run(
            [runghc_path, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            text=True,
        )

        if result.returncode == 0:
            return "Success"
        else:
            return f"Fail"

    except subprocess.TimeoutExpired:
        return "Fail (Timeout)"

    finally:
        os.remove(file_path)
