import sys

print(f'Hello, {sys.argv[1] if len(sys.argv) > 1 else "world"}!')
