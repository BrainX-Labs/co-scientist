from e2b import Sandbox

# Create a sandbox
sandbox = Sandbox.create()

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

# Close the sandbox
sandbox.close()