from e2b_code_interpreter import Sandbox

# Use context manager
with Sandbox.create() as sandbox:
    # Run a shell command
    command_result = sandbox.commands.run('echo "Hello from E2B sandbox"')
    print(f"Command output: {command_result.stdout}")
    
    # Run Python code
    python_code = """
print("Running Python code in sandbox")
result = 2 + 2
print(f"2 + 2 = {result}")
"""
    exec_result = sandbox.run_code(python_code)
    print(f"Python execution output: {exec_result.text}")
    
    # Also try to run code with input? Not needed.
    
    # Check if we can read/write files
    # Write a file
    sandbox.files.write("/tmp/hello.txt", "Hello from file")
    # Read it back
    content = sandbox.files.read("/tmp/hello.txt")
    print(f"File content: {content}")
    
    # List directory
    ls_result = sandbox.commands.run('ls -la /tmp')
    print(f"LS output: {ls_result.stdout}")