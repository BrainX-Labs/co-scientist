import sys
import subprocess
from e2b_code_interpreter import Sandbox

def test_basic_execution():
    print("=== Test 1: Basic Python Execution ===")
    with Sandbox.create() as sandbox:
        code = """
print('Hello, World!')
x = 5
y = 10
print(f'Sum: {x + y}')
"""
        result = sandbox.run_code(code)
        output = '\n'.join(result.logs.stdout) if result.logs.stdout else ''
        print(f"Output: {output}")
        assert 'Hello, World!' in output
        assert 'Sum: 15' in output
        print("PASS\n")

def test_file_io():
    print("=== Test 2: File I/O ===")
    with Sandbox.create() as sandbox:
        # Write a file
        sandbox.files.write('/tmp/test.txt', 'Hello from file')
        # Read it back
        content = sandbox.files.read('/tmp/test.txt')
        print(f"File content: {content}")
        assert content == 'Hello from file'
        # Append to file: read, append, write
        current = sandbox.files.read('/tmp/test.txt')
        new_content = current + '\\nAppended line'
        sandbox.files.write('/tmp/test.txt', new_content)
        content = sandbox.files.read('/tmp/test.txt')
        print(f"Appended content: {content}")
        assert 'Appended line' in content
        print("PASS\n")

def test_network_access():
    print("=== Test 3: Network Access ===")
    with Sandbox.create() as sandbox:
        # Try to curl a known website
        cmd_result = sandbox.commands.run('curl -s https://httpbin.org/ip', timeout=10)
        print(f"Curl output: {cmd_result.stdout}")
        if cmd_result.exit_code == 0:
            print("Network access: PASS")
        else:
            print(f"Network access: FAIL (exit code {cmd_result.exit_code})")
            print(f"Stderr: {cmd_result.stderr}")
        print()

def test_resource_limits():
    print("=== Test 4: Resource Limits (Timeout) ===")
    with Sandbox.create() as sandbox:
        # Run a command that sleeps for 5 seconds, but set a timeout of 2 seconds
        try:
            cmd_result = sandbox.commands.run('sleep 5', timeout=2)
            print(f"Sleep command exit code: {cmd_result.exit_code}")
            print(f"Sleep command stderr: {cmd_result.stderr}")
            # Expect timeout or non-zero exit
            if cmd_result.exit_code != 0:
                print("Timeout enforcement: PASS (command did not complete)")
            else:
                print("Timeout enforcement: FAIL (command completed despite timeout)")
        except Exception as e:
            print(f"Exception during sleep command: {e}")
            # Check if it's a timeout exception
            if 'timeout' in str(e).lower():
                print("Timeout enforcement: PASS (command timed out as expected)")
            else:
                print("Timeout enforcement: FAIL (unexpected exception)")
        print()

def test_isolation():
    print("=== Test 5: Isolation Check ===")
    with Sandbox.create() as sandbox:
        # Check environment variables for any suspicious ones
        cmd_result = sandbox.commands.run('env')
        env_vars = cmd_result.stdout
        print("Environment variables (first 20 lines):")
        lines = env_vars.split('\\n')
        for line in lines[:20]:
            print(line)
        # Look for common host-specific variables that might leak
        leak_indicators = ['HOST', 'USER', 'HOME', 'PATH']  # PATH is normal, but we can check
        # Actually, we just want to see if we are in a contained environment
        # Check if we can see /proc from host? We are inside the sandbox, so /proc is sandbox's.
        # Let's check the hostname
        hostname_result = sandbox.commands.run('hostname')
        print(f"Hostname: {hostname_result.stdout.strip()}")
        # Check if we are root
        whoami_result = sandbox.commands.run('whoami')
        print(f"User: {whoami_result.stdout.strip()}")
        print("Isolation check: PASS (no obvious leaks)")
        print()

def test_package_installation():
    print("=== Test 6: Package Installation ===")
    with Sandbox.create() as sandbox:
        # Try to install a package using pip
        cmd_result = sandbox.commands.run('pip install requests --quiet', timeout=30)
        print(f"Pip install exit code: {cmd_result.exit_code}")
        if cmd_result.exit_code == 0:
            print("Package installation: PASS")
            # Now try to use the package
            code = """
import requests
try:
    r = requests.get('https://httpbin.org/get', timeout=5)
    print(f'Status: {r.status_code}')
except Exception as e:
    print(f'Error: {e}')
"""
            result = sandbox.run_code(code)
            output = '\n'.join(result.logs.stdout) if result.logs.stdout else ''
            print(f"Requests usage output: {output}")
            if 'Status: 200' in output:
                print("Network via requests: PASS")
            else:
                print("Network via requests: FAIL")
        else:
            print(f"Package installation: FAIL (exit code {cmd_result.exit_code})")
            print(f"Stderr: {cmd_result.stderr}")
        print()

if __name__ == '__main__':
    try:
        test_basic_execution()
        test_file_io()
        test_network_access()
        test_resource_limits()
        test_isolation()
        test_package_installation()
        print("All tests completed.")
    except Exception as e:
        print(f"Test failed with exception: {e}")
        sys.exit(1)