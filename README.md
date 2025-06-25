# zsh-histdb-converter

🚀 **Convert your entire zsh history to Atuin in minutes!**

> **⚡ One-liner solution:** `uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin`

Tired of Atuin only importing a tiny fraction of your shell history? This tool solves the mysterious import problem that affects many users and converts your complete zsh history to a format that Atuin can fully import.

## 🤔 The Problem

Many users experience this frustrating issue:

```bash
# You have a massive history file
$ wc -l ~/.histfile
   51852 /Users/you/.histfile

# But Atuin's import barely works
$ atuin import auto
$ atuin import zsh
$ atuin stats
Total commands:   15      # WTF?! 😤
Unique commands:  12
```

**Why does this happen?** Atuin's built-in zsh importer has undocumented limitations and often fails on:

- Malformed multiline commands
- Large history files
- Certain formatting edge cases
- Complex command structures

## ✅ The Solution

This tool uses Atuin's **zsh-histdb import method** which is much more robust and imports **everything**.

## ✨ Features

- 🔄 **Complete History Import** - Import ALL your zsh history entries, not just recent ones
- 🎯 **Perfect Compatibility** - Creates zsh-histdb format that Atuin imports flawlessly
- ⚡ **Fast & Reliable** - Processes thousands of commands in minutes
- 🛠️ **Easy to Use** - One command does everything
- 🧪 **Battle Tested** - Built with TDD, fully tested

## 🚀 Quick Start

### Prerequisites

1. **Install Atuin** (if you haven't already):

   ```bash
   # macOS
   brew install atuin

   # Linux
   curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
   ```

2. **Register with Atuin**:
   ```bash
   atuin register -u <USERNAME> -e <EMAIL>
   atuin import auto  # Import what you can normally
   atuin sync
   ```

### Convert & Import Your History

**Option 1: Run directly from GitHub with uvx (Easiest!)**

```bash
# No installation needed - runs directly from GitHub!
uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin
```

**Option 2: Use pipx**

```bash
# Install and run in one go
pipx run zsh-histdb-converter --import-to-atuin

# Or install permanently
pipx install zsh-histdb-converter
zsh-histdb-converter --import-to-atuin
```

**Option 3: Clone and run with uv**

```bash
git clone https://github.com/e0da/zsh-histdb-converter
cd zsh-histdb-converter
uv run zsh-histdb-converter --import-to-atuin
```

That's it! 🎉 Your complete shell history is now searchable in Atuin.

## 📊 Real Results

**Before:** The mysterious import failure

```bash
$ wc -l ~/.histfile
   51852 /Users/you/.histfile    # 51K+ commands in history file

$ atuin import auto
$ atuin import zsh
$ atuin stats
Total commands:   15             # Only 15 imported! 😡
Unique commands:  12
```

**After:** Using zsh-histdb-converter

```bash
$ zsh-histdb-converter --import-to-atuin
Converting all entries
✅ Conversion completed successfully!
✅ Successfully imported to Atuin!

$ atuin stats
Total commands:   49271  🚀      # ALL commands imported!
Unique commands:  25175  🔥
[▮▮▮▮▮▮▮▮▮▮] 9959 g
[▮▮▮▮▮     ] 5381 cd
[▮▮        ] 2495 grep
```

**That's a 3,284x improvement!** From 15 to 49,271 commands. 🤯

## 🔧 Usage Options

```bash
# Convert recent entries only
zsh-histdb-converter -n 1000 --import-to-atuin

# Convert all history (default)
zsh-histdb-converter --import-to-atuin

# Just create database without importing
zsh-histdb-converter -o my-history.db

# Custom history file location
zsh-histdb-converter ~/.zsh_history --import-to-atuin

# See all options
zsh-histdb-converter --help
```

## 🛠️ How It Works

1. **Parses** your zsh history file (`~/.histfile` by default)
2. **Converts** entries to zsh-histdb SQLite format
3. **Imports** the database into Atuin using `atuin import zsh-hist-db`

The tool handles:

- ✅ Malformed multiline commands
- ✅ Duplicate command deduplication
- ✅ Proper timestamp and duration parsing
- ✅ Large history files (tested with 50K+ commands)

## 🔍 Why This Tool?

Atuin's built-in zsh import is limited and often only imports a small fraction of your history. This tool:

- Uses the **zsh-histdb import method** which works much better
- Processes **all entries** in your history file
- Handles **edge cases** that break other importers
- Gives you **complete history access** in Atuin

## 🚀 Atuin Setup Guide

### First Time Setup

1. **Install Atuin**:

   ```bash
   # macOS
   brew install atuin

   # Linux
   curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
   ```

2. **Configure your shell** (add to `~/.zshrc`):

   ```bash
   eval "$(atuin init zsh)"
   ```

3. **Register account**:

   ```bash
   atuin register -u yourusername -e your@email.com
   ```

4. **Import your history**:

   ```bash
   uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin
   ```

5. **Sync to cloud** (optional):
   ```bash
   atuin sync
   ```

### Key Bindings

- **Ctrl+R** - Search history (replaces default reverse search)
- **Ctrl+↑** - Search by prefix
- **Esc** then **Ctrl+R** - Browse full history

### Pro Tips

- Use `atuin search <term>` for command-line searching
- Run `atuin sync` regularly to backup your history
- Check `atuin stats` to see your command usage patterns

## 🧪 Development

Built with modern Python practices:

```bash
git clone https://github.com/e0da/zsh-histdb-converter
cd zsh-histdb-converter
uv sync
uv run pytest  # Run tests
uv run zsh-histdb-converter --help
```

## 📝 License

MIT License - feel free to use, modify, and distribute!

## 🤝 Contributing

Issues and PRs welcome! This tool was built to solve a real problem - help us make it even better.

---

**Made with ❤️ for the shell power user community**

_Stop settling for partial history imports. Get your complete shell history in Atuin today!_
