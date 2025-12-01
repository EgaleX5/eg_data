# Backup Extractor – Advanced Secure Automation Tool

A lightweight, modular, security‑focused automation tool designed for advanced users, penetration testers, researchers, and power‑users who want a fully encrypted, self‑contained backup system for Android (Termux) or Linux environments.

This tool creates a secure workflow where:
- Sensitive configuration files remain encrypted
- The main script runs backups safely
- A dedicated stop controller halts long tasks instantly
- Setup scripts auto‑create required folders & permissions

## ⚡ Features
- Encrypted configuration using strong key‑based protection
- Auto-backup engine to securely send files to remote endpoints
- Stop process module to abort running backups safely
- Smart logging system that avoids duplicate processing
- Modular file structure (backup script, setup script, encryption script, stop script)
- Works on Termux / Linux
- Lightweight, minimal dependencies, fast execution

## 🧩 Project Structure

---

## 🚀 Installation
```bash
git clone https://github.com/EgaleX5/eg_data.git
cd eg_data
bash setup.sh
backup
