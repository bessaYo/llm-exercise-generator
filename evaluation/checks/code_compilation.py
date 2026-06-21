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


def classify_failure(stderr: str) -> str:
    """
    Classifies a GHC failure as 'incomplete' or 'genuine'.

    'incomplete' means the snippet is a syntactically valid fragment that cannot
    compile only because a definition is missing (e.g. a type signature without
    a body, or a reference to an undeclared name) - typically caused by the model
    truncating its output. 'genuine' means the complete code has a real type or
    semantic error. This distinction lets us report the success rate restricted
    to complete code, separately from truncation artifacts.
    """
    incomplete_markers = (
        "lacks an accompanying binding",   # type signature without a body
        "Variable not in scope",           # references an undefined name
        "Data constructor not in scope",
        "Not in scope:",
    )
    if any(marker in stderr for marker in incomplete_markers):
        return "incomplete"
    return "genuine"


_EXPR_PREAMBLE = (
    # NoMonomorphismRestriction so that a bare polymorphic value such as `length`
    # or `foldr` type-checks as a binding instead of failing with an ambiguous
    # type; ExtendedDefaultRules resolves harmless numeric ambiguity.
    "{-# LANGUAGE NoMonomorphismRestriction #-}\n"
    "{-# LANGUAGE ExtendedDefaultRules #-}\n"
    "import Data.List\n"
    "import Data.Char\n"
    "import Data.Maybe\n"
)


def type_check_expression(expr: str) -> dict:
    """
    Type-checks a single inline Haskell expression (e.g. `head [404, 200]`).

    The expression is bound in a throwaway module and compiled with GHC. The
    outcome is classified as:
      - 'well_typed'      : the expression compiles,
      - 'ill_typed'       : it is a real expression but does not type-check,
      - 'not_expression'  : it is not a self-contained expression at all
                            (a bare type name, a signature, or a syntactic
                            fragment), so a type check does not apply.
    Returns {"verdict": ..., "stderr": ...}.
    """
    source = f"{_EXPR_PREAMBLE}_checkExpr = ({expr})\nmain = return ()\n"
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".hs", mode="w", encoding="utf-8"
    ) as f:
        f.write(source)
        file_path = f.name
    try:
        result = subprocess.run(
            [RUNGHC_PATH, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
            text=True,
        )
    except subprocess.TimeoutExpired:
        os.remove(file_path)
        return {"verdict": "ill_typed", "stderr": "Execution timed out."}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    if result.returncode == 0:
        return {"verdict": "well_typed", "stderr": ""}

    stderr = result.stderr
    non_expression_markers = (
        "parse error",
        "naked expression",
        "Data constructor not in scope",
        "Data constructor out of scope",
        "is not in scope",
        "not in scope: type",
        "lacks an accompanying binding",
        "Illegal type signature",
        "term-level use of the type constructor",  # a bare type name, e.g. `Int`
        "cannot appear in this position",          # a type used in term position
        "cannot parse",
    )
    lowered = stderr.lower()
    if any(m.lower() in lowered for m in non_expression_markers):
        return {"verdict": "not_expression", "stderr": stderr.strip()}
    # A capitalized, value-less name used where a value is expected is a type name
    if "not in scope" in lowered and "data constructor" not in lowered:
        # e.g. `Int` used as a value -> treated as a type/identifier, not an expr
        return {"verdict": "not_expression", "stderr": stderr.strip()}
    return {"verdict": "ill_typed", "stderr": stderr.strip()}


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
                stderr = result.stderr.strip()
                results.append(
                    {
                        "block": i,
                        "status": "Fail",
                        "reason": classify_failure(stderr),
                        "stderr": stderr,
                        "code": code,
                    }
                )
        # If timeout occurs, record th error
        except subprocess.TimeoutExpired:
            results.append(
                {
                    "block": i,
                    "status": "Fail (Timeout)",
                    "reason": "genuine",
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
