# 🔬 Deep Research Co-Scientist AI Agent

An autonomous, zero-cost, neuro-symbolic research agent built using **Pi Agent**, **Moonshot Kimi-K3** (via NVIDIA NIM), **Lean 4 Theorem Prover**, **E2B MicroVM Sandboxes**, and multi-provider web search fallbacks.

This system runs **100% in the cloud without local hardware, subscriptions, or credit cards** using GitHub Codespaces or Actions with zero global configuration required. All configurations are self-contained at the project level.

## 🏗️ System Architecture

```
                                ┌────────────────────────────────────────────────────────┐
                                │                 GitHub Codespaces                      │
                                │            (Master Cloud Environment)                  │
                                └──────────────────────────┬─────────────────────────────┘
                                                           │
                                                           ▼
                                ┌────────────────────────────────────────────────────────┐
                                │                 Pi Agent CLI Runtime                   │
                                └────┬───────────────┬────────────────┬──────────────┬───┘
                                     │               │                │              │
                                     ▼               ▼                ▼              ▼
┌──────────────────────────────────────┐   ┌──────────────────┐  ┌───────────┐  ┌────────────────┐
│            LiteLLM Proxy             │   │  Project MCPs    │  │ Web Search│  │  E2B Sandbox   │
│  (Rate Limiter & Gateway @ 35 RPM)   │   ├──────────────────┤  ├───────────┤  │   (Firecracker │
└──────────────────┬───────────────────┘   │ • ArXiv          │  │ • Tavily  │  │   Isolated     │
                   │                       │ • Lean 4 Prover  │  │ • Brave   │  │   Python/Bash) │
                   ▼                       └──────────────────┘  │           │  └────────────────┘
┌──────────────────────────────────────┐                         │           │
│          NVIDIA NIM API              │                         └───────────┘
│   (Moonshot Kimi-K3, 104B MoE,       │
│    1M Context, Thinking Engine)      │
└──────────────────────────────────────┘

```

## ✨ Features

* **Project-Level Configuration**: Portable repository layout containing `.pi/agent/models.json`, `.pi/mcp.json`, `.pi/web-search.json`, and `.env` setup.

* **Zero-DIY Architecture**: Built entirely on standard open-source packages, official MCP servers, and cloud infrastructure.

* **100% Free & No Credit Card**: Runs on GitHub Codespaces (120 core-hrs/mo free), NVIDIA NIM free credits, and E2B cloud microVMs.

* **Neuro-Symbolic Verification**: Combines LLM research synthesis with formal mathematical verification via **Lean 4** and **Mathlib**.

* **Automated Literature Search**: Direct integration with ArXiv API for downloading and parsing preprints.

* **Resilient Web Search Fallbacks**: Automatic failover from Tavily to Brave when both providers are configured.

* **Safe Code Execution**: Offloads Python data science, simulations, and algorithmic code execution to isolated E2B microVMs.

* **Rate-Limit Gateway**: Uses `litellm` as an API proxy to transparently enforce RPM limits (\~35 RPM) and prevent `429 Too Many Requests` crashes.

---

## 🧮 How Research Proof & Verification Works

To prevent LLM hallucination in mathematical and theoretical proofs, this agent uses a **Neuro-Symbolic Verification Loop**:

```
Informal Hypothesis ──► Auto-Formalization (Lean 4) ──► Compiler Tactic Loop ──► Micro-Kernel Q.E.D.
```

1. **Auto-Formalization**: Kimi-K3 translates an informal mathematical claim into Lean 4 syntax.
2. **Interactive Proof Loop**: The agent applies tactics (`induction`, `simp`, `exact`, `ring`).
3. **Compiler Feedback**: `lean-mcp-server` feeds error messages and open goals back to Kimi-K3.
4. **Kernel Verification**: The Lean kernel independently verifies the proof, ensuring mathematical certainty without hallucination.

---

## 🏃 Running the Agent

### GitHub Actions OpenCode Coder

The [OpenCode Coder workflow](.github/workflows/opencoder.yml) runs on the Blacksmith runner with NVIDIA NIM (`moonshotai/kimi-k3`) and the Tavily MCP web-search server. Add `NVIDIA_API_KEY` and `TAVILY_API_KEY` as Actions secrets, then start a task from the Actions tab. The workflow uses GitHub's built-in token, creates a unique `opencoder/<run-id>` branch, and grants only `contents: write`; it does not handle issue or pull-request comments.

### Codespace

#### Step 1: Populate `.env`

Edit your root `.env` file with your keys:

```bash
nano .env  # Add your NVIDIA_API_KEY and E2B_API_KEY
```

#### Step 2: Start Rate-Limit Gateway

Run LiteLLM in the background to handle rate-limiting and auto-retries for NVIDIA NIM:

```bash
litellm \
  --model nvidia_nim/moonshotai/kimi-k3 \
  --api_key $NVIDIA_API_KEY \
  --port 8080 \
  --rpm 35 > litellm.log 2>&1 &
```

#### Step 3: Execute Deep Research Task

##### Autonomous Command Mode

```bash
pi -p --stream=all "Formulate a hypothesis regarding prime gap distributions, search ArXiv for recent bounds, test the algorithm via Python in the e2b-sandbox microVM, and formally verify algebraic lemmas using lean-prover."
```

##### Interactive Terminal Session

```bash
pi
```

Inside the interactive prompt:

> `"Act as my Lead Co-Scientist. Conduct a deep research investigation into quantum error correction codes, search preprints, run validation scripts in the sandbox, and write a report in research_report.md."`

### Action

1. Navigate to the Actions tab in your GitHub repository.

2. Select Headless Co-Scientist Research (Blacksmith).

3. Click Run workflow, enter your research topic, and launch.

4. The runner will execute, generate the research report, and push research_report.md directly back to your repo branch!

---

## 🛡️ License

MIT License. Free for open scientific research and educational usage.