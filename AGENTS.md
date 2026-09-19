# Co-Scientist Research Protocols

When assigned a deep research task, maintain an iterative workflow:

1. **Hypothesis Generation**: Formulate specific sub-hypotheses and core scientific questions.
2. **Literature & Web Search**:
   - Query preprints using `arxiv` MCP.
   - Run broad web searches across Tavily/Brave with automatic fallbacks.
3. **Formal Verification (Lean 4)**:
   - For mathematical theorems or formal proofs, auto-formalize claims into Lean 4 code.
   - Run `lean-prover` MCP tool to verify correctness against the Lean compiler kernel until `[QED]`.
4. **Empirical Code Execution**:
   - Run Python code, data analysis, and simulations inside the `e2b-sandbox` microVM environment.
5. **Synthesis**: Write findings to `./research_report.md` with explicit ArXiv citations and verified Lean 4 proof blocks.
