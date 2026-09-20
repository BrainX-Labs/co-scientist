from e2b_code_interpreter import Sandbox

# Use context manager
with Sandbox.create() as sandbox:
    # Run Python code
    python_code = """
print("Running Python code in sandbox")
result = 2 + 2
print(f"2 + 2 = {result}")
"""
    exec_result = sandbox.run_code(python_code)
    print(f"Execution result type: {type(exec_result)}")
    print(f"Execution result dir: {dir(exec_result)}")
    print(f"Execution result: {exec_result}")
    # Try to see if there is a logs or text attribute
    if hasattr(exec_result, 'text'):
        print(f"text: {exec_result.text}")
    if hasattr(exec_result, 'logs'):
        print(f"logs: {exec_result.logs}")
    if hasattr(exec_result, 'stdout'):
        print(f"stdout: {exec_result.stdout}")
    if hasattr(exec_result, 'stderr'):
        print(f"stderr: {exec_result.stderr}")
    if hasattr(exec_result, 'result'):
        print(f"result: {exec_result.result}")