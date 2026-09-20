from e2b_code_interpreter import Sandbox

# Use context manager
with Sandbox.create() as sandbox:
    print("Sandbox attributes and methods:")
    print([attr for attr in dir(sandbox) if not attr.startswith('_')])
    # Check if there is a run_code method
    if hasattr(sandbox, 'run_code'):
        print("Found run_code method")
    else:
        print("No run_code method")
        # Maybe it's under a different attribute?
        # Look for code or executor
        for attr in dir(sandbox):
            if 'code' in attr.lower():
                print(f"Found attribute with code: {attr}")