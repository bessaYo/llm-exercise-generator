import subprocess
import tempfile
import os
import re
from config import RUNGHC_PATH


def has_main_function(code: str) -> bool:
    """Checks whether the given Haskell code contains a main function."""
    return re.search(r"^\s*main\s*=", code, re.MULTILINE) is not None


def extract_haskell_blocks(markdown_text: str) -> list:
    """Extracts all Haskell code blocks from a markdown string."""
    pattern = r"```haskell\n(.*?)```"
    return [block.strip() for block in re.findall(pattern, markdown_text, re.DOTALL)]


def append_dummy_main(code: str) -> str:
    """Appends a neutral main function to the code if none is present."""
    if not has_main_function(code):
        return code + "\n\nmain = return ()"
    return code


def check_code_compilation(exercise: str) -> dict:
    """Checks the compilation of Haskell code blocks in the given exercise."""
    code_blocks = extract_haskell_blocks(exercise)
    if not code_blocks:
        return {
            "status": "No Haskell code found",
            "compiled_blocks": 0,
            "errors": [],
        }

    results = []

    # Check each code block for compilation
    for i, code in enumerate(code_blocks):
        
        # Append a dummy main function if not present
        code = append_dummy_main(code)
        
        # Create a temporary file to store the Haskell code
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".hs", mode="w", encoding="utf-8"
        ) as f:
            f.write(code)
            file_path = f.name

        # Try to compile the Haskell code using GHC
        try:
            result = subprocess.run(
                [RUNGHC_PATH, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                text=True,
            ) 
            
            # If the return code is not 0, record the error
            if result.returncode != 0:
                results.append(
                    {
                        "block": i,
                        "status": "Fail",
                        "stderr": result.stderr.strip(),
                        "code": code,
                    }
                )
        # If timeout occurs, record th error
        except subprocess.TimeoutExpired:
            results.append(
                {
                    "block": i,
                    "status": "Fail (Timeout)",
                    "stderr": "Execution timed out.",
                    "code": code,
                }
            )
        finally:
            # Remove the temporary file
            os.remove(file_path)
            
    # If no errors were found, return success
    if not results:
        return {"status": "Success", "compiled_blocks": len(code_blocks), "errors": []}
    
    # Else return the list of errors
    else:
        return {
            "status": "Fail",
            "compiled_blocks": len(code_blocks),
            "errors": results,
        }
