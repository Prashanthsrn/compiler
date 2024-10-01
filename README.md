# Simple Compiler

A basic compiler implementation in Python that handles arithmetic operations, variables, and if-else statements.

## Features

- Lexical analysis
- Syntax parsing
- Semantic analysis
- Intermediate code generation
- Support for:
  - Arithmetic operations (+, -, *, /)
  - Variable assignments
  - If-else statements
  - Comparison operators (==, >, <)

## Usage

1. Create an input file (e.g., `input.txt`) with your source code
2. Run the compiler:
   ```
   python main.py input.txt
   ```

## Example Input

```
x = 10
y = 5
if x > y {
    result = x - y
}   
else {
    result = y - x
}
```

## Example Output

```
Generated Intermediate Code:
x = 10
y = 5
t1 = x > y
if not (t1):
    goto L2
t4 = x - y
result = t4
# goto L3
# L2:
t5 = y - x
result = t5
# L3:
```

## Requirements

- Python 3.7 or higher
