import re
from evaluation.checks.code_compilation import check_code_compilation


def extract_haskell_blocks(markdown_text: str) -> list:
    """
    Extracts all Haskell code blocks from a Markdown string and returns them as a list.
    """
    pattern = r"```haskell\n(.*?)```"
    return [block.strip() for block in re.findall(pattern, markdown_text, re.DOTALL)]


exercise = """
Quicksort is a popular sorting algorithm that works by partitioning an array into smaller sub-arrays based on a chosen pivot element. The goal is to sort the elements in ascending order.

Consider the Haskell implementation of quicksort below:

```haskell
qsort [] = []
qsort (x : xs) = qsort ys ++ [x] ++ qsort zs
where
  ys = [a | a < x]
  zs = [b | b > x]
```

Explain how this implementation works. What are the steps involved in sorting a list using quicksort? Provide an example of a list and demonstrate how it would be sorted using this algorithm. a) Describe the role of the pivot element in the quicksort algorithm. b) Explain the purpose of the `where` clause in Haskell and how it is used to define the sub-arrays `ys` and `zs`.
"""

compilation_result = check_code_compilation(exercise)
print(compilation_result)
