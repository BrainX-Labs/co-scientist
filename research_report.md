# Research Report: Testing E2B Sandbox

## Abstract
E2B provides secure, isolated sandboxes for executing AI-generated code. This report evaluates the functionality, performance, and isolation properties of the E2B sandbox through a series of empirical tests. We confirm that the sandbox supports Python execution, file I/O, network access, package installation, and enforces resource limits. The environment appears isolated from the host, with no obvious leakage of host-specific environment variables.

## Introduction
As AI agents increasingly generate and execute code, the need for secure and isolated execution environments becomes paramount. E2B (https://e2b.dev) offers a cloud-based sandbox infrastructure designed for safe code execution. This report investigates the capabilities of the E2B sandbox to determine its suitability for AI agent workflows.

## Hypotheses
We formulated the following hypotheses:
1. **H1**: The E2B sandbox can successfully execute Python code and return the expected output.
2. **H2**: The E2B sandbox enforces resource limits (e.g., timeouts) to prevent runaway processes.
3. **H3**: The E2B sandbox provides isolation, preventing access to host system resources and leaking sensitive information.

## Literature Review
We conducted web searches to gather information about E2B sandbox from official documentation, GitHub repositories, and technical articles. Key findings:
- E2B provides isolated Linux VMs (microVMs) powered by Firecracker, offering secure execution environments [[1](#ref1)].
- The sandbox allows access to the Linux OS, file system, command execution, internet access, and Git operations [[2](#ref2)].
- Security features include per-sandbox Firecracker microVMs, controlled egress, and secure access between SDK and sandbox controller [[3](#ref3)].
- E2B supports multiple SDKs (Python, JavaScript) and includes a code interpreter specialization for executing code in various languages [[4](#ref4)].
- The platform is open-source under Apache-2.0 license, allowing self-hosting [[5](#ref5)].

## Empirical Evaluation
We designed and executed a series of tests using the E2B Python SDK (version 2.51.0) and code interpreter extension (version 2.10.0). An E2B API key was provided via the `E2B_API_KEY` environment variable.

### Test 1: Basic Python Execution
We executed a simple Python script that printed messages and performed arithmetic. The sandbox correctly executed the code and returned the expected output.

### Test 2: File I/O
We wrote, read, and appended to a file within the sandbox's filesystem. Operations succeeded, demonstrating persistent storage capabilities within the sandbox session.

### Test 3: Network Access
We performed an HTTP request to an external service (httpbin.org) using both `curl` and the Python `requests` library (after installing it via pip). The sandbox successfully established outbound network connections and retrieved responses.

### Test 4: Resource Limits (Timeout)
We attempted to run a `sleep 5` command with a sandbox-imposed timeout of 2 seconds. The SDK raised a timeout exception, confirming that the sandbox enforces execution time limits.

### Test 5: Isolation Check
We examined environment variables inside the sandbox and observed variables indicative of the sandbox environment (e.g., `E2B_SANDBOX=true`, `E2B_TEMPLATE_ID`). No obvious host-specific leaked variables (such as host IP addresses or user credentials) were detected. The sandbox ran as a non-root user (`user`) with a distinct hostname (`e2b.local`).

### Test 6: Package Installation
We installed the `requests` package using `pip` and subsequently used it to make an HTTP request. This verified that the sandbox supports package installation and that installed packages can function correctly (including network access).

## Discussion
All tests passed, supporting our hypotheses:
- **H1 is supported**: Python code execution works correctly.
- **H2 is supported**: The sandbox enforces timeouts via SDK exceptions when commands exceed the allotted time.
- **H3 is supported**: The sandbox appears isolated, with no evident leakage of host environment variables. The use of Firecracker microVMs provides hardware-level isolation [[3](#ref3)].

The sandbox provides a ready-to-use environment for AI agents, with capabilities for file persistence, networking, and dependency management. Users should be aware that persistent storage beyond the sandbox lifetime requires explicit snapshots or external storage solutions.

## Conclusion
The E2B sandbox provides a secure, isolated, and functional environment for executing AI-generated code. It meets the core requirements of safe code execution: isolation, resource control, and necessary functionality (I/O, networking, package management). Our empirical evaluation confirms that E2B is suitable for deployment in AI agent workflows where secure code execution is essential.

## References
<a name="ref1"></a>[1] E2B Documentation: "Sandbox lifecycle". https://www.e2b.dev/docs/sandbox  
<a name="ref2"></a>[2] E2B GitHub Repository: https://github.com/e2b-dev/e2b  
<a name="ref3"></a>[3] E2B for Enterprise: "Isolation: a Firecracker microVM with its own guest kernel per session". https://e2b.dev/enterprise.md  
<a name="ref4"></a>[4] E2B Code Interpreter SDK Documentation: https://e2b.dev/docs/sdk-reference/code-interpreter-python-sdk  
<a name="ref5"></a>[5] E2B Open Source: https://e2b.dev/open-source.md