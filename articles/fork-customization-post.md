# I Forked a 140k+ Star AI Project and Customized It for Android — Here's Everything I Changed

*Published on dev.to / Medium / LinkedIn*
*Author: Spider-Verse (Alaa Mohanad)*

---

## Why I Forked NousResearch/hermes-agent

If you've been following the open-source AI agent space, you've probably heard of **Hermes Agent** by NousResearch. With **140k+ stars on GitHub**, it's one of the most popular open-source AI agent frameworks out there — and for good reason. It's modular, extensible, and runs a full AI agent loop with tool calling, memory, multi-provider support, and gateway integrations across 20+ platforms.

But here's the thing — **it's built for standard Linux and macOS environments**. If you're running on an Android device using Termux (like I am), you're going to hit walls. Specifically:

1. **ELF binary incompatibility** — prebuilt binaries target glibc-based distros, not Android's bionic libc
2. **Filesystem path conflicts** — the project expects `.venv` (with dot), Termux uses `venv` (without dot)
3. **Python 3.12 deprecation issues** — `pkg_resources` and certain import patterns break silently
4. **Dependency installation failures** — `pip install --only-binary :all:` fails on ARM64 for several key packages

So I forked it. And I made it **actually work on a phone**.

---

## What I Changed (The Technical Breakdown)

### 1. ARM64 / Termux Compatibility Layer

The biggest hurdle: Hermes Agent's dependencies include packages with prebuilt ELF binaries compiled for x86_64 Linux with glibc. These **cannot run on Android** — not even with `patchelf`. The dynamic linker paths are fundamentally different (Android uses `/system/bin/linker` via bionic libc, not `/lib64/ld-linux-x86-64.so.2` via glibc).

**Solution:**
- Switched to system packages via `pkg install` wherever possible (ruff, binutils, patchelf)
- Updated dependency resolution to compile from source when no compatible binary exists
- Added a `TERMUX_COMPAT` environment variable check in the install script
- Documented the bionic/glibc boundary so future users don't waste hours debugging

### 2. Virtual Environment Path Resolution

Simple but critical. The codebase hardcoded `.venv` everywhere:

```python
# Before
VENV_PATH = Path(".venv")
```

Termux (and many other setups) use `venv` without the leading dot.

**Solution:**
```python
# After
def resolve_venv():
    candidates = [Path(".venv"), Path("venv"), Path(os.path.expanduser("~/.hermes/hermes-agent/venv"))]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]  # fallback
```

Added symlink creation during setup so both paths work interchangeably.

### 3. Python 3.12 & Modern Python Fixes

Several imports were breaking on Python 3.12:
- `pkg_resources` was removed from setuptools in newer versions
- Certain `asyncio` patterns deprecated
- `typing` imports needed updating

**Solution:** Added compatibility shims and updated all deprecated patterns while maintaining backward compatibility with Python 3.10+.

### 4. Dependency Installation Overhaul

`pip install --only-binary :all:` silently fails on ARM64 for some packages. Rather than letting users stare at cryptic error messages:
- Added fallback to source compilation with clear error messages
- Created a `requirements-termux.txt` with pre-verified working versions
- Switched several packages to system-installable alternatives

### 5. Git Identity & Fork Hygiene

I used **surgical rebase** (not `filter-branch` — that times out on large repos on ARM hardware) to rewrite my personal commits under the "Spider-Verse" identity:

```bash
GIT_SEQUENCE_EDITOR="sed -i 's/^pick/edit/'" git rebase -i HEAD~N
# For each commit:
git commit --amend --author="Spider-Verse <alaamohanad169-ship-it@users.noreply.github.com>"
git rebase --continue
```

**Critical:** I only amended my own commits. Upstream commits are untouched — the fork relationship is preserved, and I can still `git pull` from NousResearch/hermes-agent to get future updates.

---

## Why This Matters

### For Users
You can now run a **production-grade AI agent** on a $200 Android phone. No cloud costs, no API subscriptions (if you use local models), no laptop required. The barrier to entry for AI automation just dropped to almost zero.

### For Developers
This fork demonstrates a pattern that's becoming increasingly important: **adapting powerful desktop/server AI tools for mobile and ARM environments**. The mobile-first markets (South Asia, Africa, Southeast Asia) need this.

### For My Career
This project is my **portfolio piece**. It shows I can:
- Understand and modify complex Python codebases (50k+ lines)
- Solve cross-platform compatibility problems
- Work with AI/ML tooling at a deep level
- Document and explain technical decisions clearly

---

## What's Next

1. **PR back upstream** — Several of my fixes (venv path resolution, Python 3.12 compat) are applicable to the main repo. I'm preparing pull requests.
2. **Docker image** — Building an ARM64 Docker image for reproducible deployment
3. **Telegram gateway** — Integrating Hermes Agent with a Telegram bot for mobile-first AI automation
4. **Performance benchmarking** — Running Hermes on Termux vs. cloud instances to compare cost/performance

---

## Try It Yourself

```bash
git clone https://github.com/alaamohanad169-ship-it/hermes-agent
cd hermes-agent
bash setup-termux.sh  # Termux-specific setup script
```

Full instructions in the README.

---

*Spider-Verse is an AI automation engineer based in Egypt, specializing in making powerful AI tools accessible on any device. Follow on GitHub: [@alaamohanad169-ship-it](https://github.com/alaamohanad169-ship-it)*