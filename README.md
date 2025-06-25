# zsh-histdb-converter 🚀

**Convert your entire zsh history to Atuin in minutes!**

> **⚡ One-liner:** `uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin`

Stop settling for partial history imports. This tool solves the mysterious Atuin import problem and gets your **complete** shell history searchable.

## 🤔 The Problem

You have thousands of commands in your history, but Atuin barely imports any:

```bash
$ wc -l ~/.histfile
   51852 /Users/you/.histfile     # 51K+ commands

$ atuin import auto && atuin import zsh
$ atuin stats
Total commands:   15              # Only 15?! 😤
```

**Why?** Atuin's built-in importers fail on:

- Large history files
- Malformed multiline commands
- Complex command structures
- Certain formatting edge cases

## ✅ The Solution

This tool uses Atuin's **zsh-histdb import method** which is much more robust:

```bash
$ zsh-histdb-converter --import-to-atuin
✅ Conversion completed successfully!
✅ Successfully imported to Atuin!

$ atuin stats
Total commands:   49271  🚀       # ALL commands imported!
Unique commands:  25175  🔥
```

**That's a 3,284x improvement!** From 15 to 49,271 commands.

## 🚀 Installation & Usage

### Option 1: uvx (Recommended)

No installation needed - runs directly from GitHub:

```bash
uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin
```

### Option 2: pipx

```bash
# Run once
pipx run zsh-histdb-converter --import-to-atuin

# Or install permanently
pipx install zsh-histdb-converter
zsh-histdb-converter --import-to-atuin
```

### Option 3: Docker 🐳

Perfect for isolated environments or when you don't want to install Python tools:

#### Quick Start with Docker

```bash
# Build the image
docker build -t zsh-histdb-converter https://github.com/e0da/zsh-histdb-converter.git

# Create output directory
mkdir -p ./atuin-import

# Convert your history
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  zsh-histdb-converter

# Import the generated database to Atuin
HISTDB_FILE=./atuin-import/zsh-histdb.db atuin import zsh-hist-db
```

#### Docker Usage Examples

**Convert recent 1000 commands:**

```bash
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  zsh-histdb-converter -n 1000
```

**Custom history file location:**

```bash
docker run --rm \
  -v ~/.zsh_history:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  zsh-histdb-converter
```

**Custom output filename:**

```bash
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  zsh-histdb-converter -o my-history.db
```

**Show help:**

```bash
docker run --rm zsh-histdb-converter --help
```

#### Docker Notes

- 🔒 **Secure**: Your history file is mounted read-only
- 📦 **Isolated**: No Python dependencies on your system
- 🏗️ **Alpine-based**: Small ~150MB image
- 📁 **Output**: Database saved to mounted `/home/app/data` directory
- ⚠️ **Manual Import**: Docker version creates database only - you import it manually with `atuin import zsh-hist-db`

### Option 4: Clone & Run

```bash
git clone https://github.com/e0da/zsh-histdb-converter
cd zsh-histdb-converter
uv run zsh-histdb-converter --import-to-atuin
```

## 🔧 Command Options

```bash
# Convert all history (default)
zsh-histdb-converter --import-to-atuin

# Convert recent N entries only
zsh-histdb-converter -n 1000 --import-to-atuin

# Custom history file
zsh-histdb-converter ~/.zsh_history --import-to-atuin

# Just create database (no auto-import)
zsh-histdb-converter -o my-history.db

# Show all options
zsh-histdb-converter --help
```

## 🛠️ How It Works

1. **Parses** your zsh history file (`~/.histfile` by default)
2. **Converts** entries to zsh-histdb SQLite format with proper schema
3. **Imports** database into Atuin using `atuin import zsh-hist-db`

Handles all the edge cases:

- ✅ Malformed multiline commands
- ✅ Large files (50K+ commands tested)
- ✅ Duplicate deduplication
- ✅ Proper timestamp/duration parsing

## 🚀 Atuin Setup (New Users)

New to Atuin? Here's the complete setup:

### 1. Install Atuin

```bash
# macOS
brew install atuin

# Linux
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
```

### 2. Configure Shell

Add to your `~/.zshrc`:

```bash
eval "$(atuin init zsh)"
```

### 3. Register Account

```bash
atuin register -u yourusername -e your@email.com
```

### 4. Import History

```bash
uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin
```

### 5. Sync (Optional)

```bash
atuin sync
```

### Key Bindings

- **Ctrl+R** - Smart history search (replaces default)
- **Ctrl+↑** - Search by command prefix
- **Esc** then **Ctrl+R** - Browse full history

## 📊 Real Results

**Before: Standard Atuin Import**

```bash
$ wc -l ~/.histfile
   51852 /Users/you/.histfile

$ atuin import auto && atuin import zsh
$ atuin stats
Total commands:   15             # 😡 Basically nothing
Unique commands:  12
```

**After: zsh-histdb-converter**

```bash
$ zsh-histdb-converter --import-to-atuin
Converting all entries from /Users/you/.histfile
✅ Conversion completed successfully!
✅ Successfully imported to Atuin!

$ atuin stats
Total commands:   49271  🚀      # Complete history!
Unique commands:  25175  🔥
[▮▮▮▮▮▮▮▮▮▮] 9959 g            # Top commands
[▮▮▮▮▮     ] 5381 cd
[▮▮        ] 2495 grep
```

## 🐳 Docker Deep Dive

### Why Use Docker?

- **🔒 Security**: Your history file is mounted read-only
- **🧹 Clean**: No Python dependencies cluttering your system
- **🏗️ Consistent**: Same environment regardless of your OS
- **📦 Portable**: Works anywhere Docker runs

### Docker Workflow

1. **Build** (or pull when available):

   ```bash
   docker build -t zsh-histdb-converter https://github.com/e0da/zsh-histdb-converter.git
   ```

2. **Prepare output directory**:

   ```bash
   mkdir -p ~/atuin-import
   ```

3. **Convert history**:

   ```bash
   docker run --rm \
     -v ~/.histfile:/home/app/.histfile:ro \
     -v ~/atuin-import:/home/app/data \
     zsh-histdb-converter
   ```

4. **Import to Atuin**:
   ```bash
   HISTDB_FILE=~/atuin-import/zsh-histdb.db atuin import zsh-hist-db
   ```

### Docker Troubleshooting

**History file not found?**

```bash
# Check your history file location
echo $HISTFILE
ls -la ~/.histfile ~/.zsh_history

# Mount the correct file
docker run --rm \
  -v ~/.zsh_history:/home/app/.histfile:ro \
  -v ./output:/home/app/data \
  zsh-histdb-converter
```

**Permission issues?**

```bash
# Ensure output directory is writable
mkdir -p ./output
chmod 755 ./output
```

**Want to see what's happening?**

```bash
# Run with verbose output
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./output:/home/app/data \
  zsh-histdb-converter --help
```

## 🧪 Development

Built with modern Python practices and comprehensive testing:

```bash
git clone https://github.com/e0da/zsh-histdb-converter
cd zsh-histdb-converter

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run locally
uv run zsh-histdb-converter --help

# Build Docker image
docker build -t zsh-histdb-converter .
```

### Architecture

- **TDD Approach**: Built with test-driven development
- **Modular Design**: Separate parser, database, converter, and CLI modules
- **Error Handling**: Graceful handling of malformed entries
- **Modern Python**: Type hints, dataclasses, pathlib

## 🤝 Contributing

This tool solves a real problem that affects many Atuin users. Contributions welcome!

- 🐛 **Bug Reports**: Found an edge case? Open an issue
- 💡 **Feature Ideas**: Have suggestions? Let's discuss
- 🔧 **Code**: PRs welcome - just run the tests first
- 📖 **Documentation**: Help make the docs even better

The Atuin team could totally incorporate this functionality - that would be amazing and very welcome!

## 📝 License

MIT License - Use freely, modify, distribute, contribute back if helpful!

---

**Made with ❤️ for shell power users**

_Stop settling for partial history imports. Get your complete shell history in Atuin today!_

🌟 **Star the repo if this helped you!** It helps others discover the solution.
