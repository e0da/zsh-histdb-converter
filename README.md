# zsh-histdb-converter

**Convert zsh history to Atuin using the zsh-histdb import method**

> **⚡ Quick start:** `uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin`

This tool addresses import limitations with Atuin's standard zsh importers by using Atuin's [`zsh-histdb` import method](https://docs.atuin.sh/reference/import/#zsh_histdb), which is more robust for large history files and complex command structures.

## The Issue

Atuin's standard import commands (`atuin import auto` and `atuin import zsh`) can have limitations with certain history files:

```bash
$ wc -l ~/.histfile
   51852 /Users/you/.histfile     # Large history file

$ atuin import auto && atuin import zsh
$ atuin stats
Total commands:   15              # Limited import results
```

**Common import limitations:**

- Large history files
- Malformed multiline commands
- Complex command structures
- Certain formatting edge cases

## The Solution

This tool converts your zsh history to the [zsh-histdb format](https://github.com/larkery/zsh-histdb) that Atuin can import via `atuin import zsh-hist-db`. This import method is more robust and handles edge cases better than the standard zsh importer.

```bash
$ zsh-histdb-converter --import-to-atuin
Converting all entries from /Users/you/.histfile
✅ Conversion completed successfully!
✅ Successfully imported to Atuin!

$ atuin stats
Total commands:   49271          # Complete import
Unique commands:  25175
```

## Installation & Usage

### Option 1: uvx (Recommended)

Run directly from GitHub without installation:

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

For isolated environments or when you prefer not to install Python tools:

#### Quick Start with Docker

**One-liner (builds and runs directly from GitHub):**

```bash
# Create output directory and run converter in one command
mkdir -p ./atuin-import && \
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  $(docker build -q https://github.com/e0da/zsh-histdb-converter.git)

# Import the generated database to Atuin
HISTDB_FILE=./atuin-import/zsh-histdb.db atuin import zsh-hist-db
```

**Or step-by-step:**

```bash
# Build the image from GitHub
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
# One-liner (builds from GitHub)
mkdir -p ./atuin-import && \
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  $(docker build -q https://github.com/e0da/zsh-histdb-converter.git) -n 1000

# Or with pre-built image
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  zsh-histdb-converter -n 1000
```

**Custom history file location:**

```bash
# One-liner (builds from GitHub)
mkdir -p ./atuin-import && \
docker run --rm \
  -v ~/.zsh_history:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  $(docker build -q https://github.com/e0da/zsh-histdb-converter.git)

# Or with pre-built image
docker run --rm \
  -v ~/.zsh_history:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  zsh-histdb-converter
```

**Custom output filename:**

```bash
# One-liner (builds from GitHub)
mkdir -p ./atuin-import && \
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  $(docker build -q https://github.com/e0da/zsh-histdb-converter.git) -o my-history.db

# Or with pre-built image
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ./atuin-import:/home/app/data \
  zsh-histdb-converter -o my-history.db
```

**Show help:**

```bash
docker run --rm zsh-histdb-converter --help
```

#### Docker Features

- **Secure**: History file mounted read-only
- **Isolated**: No Python dependencies on your system
- **Alpine-based**: Compact ~150MB image
- **Flexible**: Database saved to mounted `/home/app/data` directory
- **Manual Import**: Creates database file - import manually with `atuin import zsh-hist-db`

### Option 4: Clone & Run

```bash
git clone https://github.com/e0da/zsh-histdb-converter
cd zsh-histdb-converter
uv run zsh-histdb-converter --import-to-atuin
```

## Command Options

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

## How It Works

1. **Parses** your zsh history file (`~/.histfile` by default)
2. **Converts** entries to [zsh-histdb SQLite format](https://github.com/larkery/zsh-histdb) with proper schema
3. **Imports** database into Atuin using [`atuin import zsh-hist-db`](https://docs.atuin.sh/reference/import/#zsh_histdb)

The tool handles common edge cases:

- Malformed multiline commands
- Large files (tested with 50K+ commands)
- Duplicate deduplication
- Proper timestamp/duration parsing

## Prerequisites

This tool assumes you have Atuin installed and configured. If not:

```bash
# Install Atuin
brew install atuin  # macOS
# or: curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh

# Configure shell (add to ~/.zshrc)
eval "$(atuin init zsh)"

# Register account
atuin register -u yourusername -e your@email.com
```

Then use this tool to import your history:

```bash
uvx --from git+https://github.com/e0da/zsh-histdb-converter zsh-histdb-converter --import-to-atuin
```

## Example Results

**Before conversion:**

```bash
$ wc -l ~/.histfile
   51852 /Users/you/.histfile

$ atuin import auto && atuin import zsh
$ atuin stats
Total commands:   15
Unique commands:  12
```

**After conversion:**

```bash
$ zsh-histdb-converter --import-to-atuin
Converting all entries from /Users/you/.histfile
✅ Conversion completed successfully!
✅ Successfully imported to Atuin!

$ atuin stats
Total commands:   49271          # Complete history imported
Unique commands:  25175
[▮▮▮▮▮▮▮▮▮▮] 9959 g            # Command usage patterns
[▮▮▮▮▮     ] 5381 cd
[▮▮        ] 2495 grep
```

## Docker Detailed Usage

### Why Use Docker?

- **Security**: History file mounted read-only
- **Clean Environment**: No Python dependencies on your system
- **Consistency**: Same environment across different systems
- **Portability**: Works anywhere Docker runs

### Docker Workflow

**Option A: One-liner (builds directly from GitHub):**

```bash
# Build and run directly from GitHub
mkdir -p ~/atuin-import && \
docker run --rm \
  -v ~/.histfile:/home/app/.histfile:ro \
  -v ~/atuin-import:/home/app/data \
  $(docker build -q https://github.com/e0da/zsh-histdb-converter.git) && \
HISTDB_FILE=~/atuin-import/zsh-histdb.db atuin import zsh-hist-db
```

**Option B: Step-by-step:**

1. **Build the image:**

   ```bash
   docker build -t zsh-histdb-converter https://github.com/e0da/zsh-histdb-converter.git
   ```

2. **Prepare output directory:**

   ```bash
   mkdir -p ~/atuin-import
   ```

3. **Convert history:**

   ```bash
   docker run --rm \
     -v ~/.histfile:/home/app/.histfile:ro \
     -v ~/atuin-import:/home/app/data \
     zsh-histdb-converter
   ```

4. **Import to Atuin:**
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

## Development

Built with modern Python practices:

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

- **Test-Driven Development**: Comprehensive test coverage
- **Modular Design**: Separate parser, database, converter, and CLI modules
- **Error Handling**: Graceful handling of malformed entries
- **Modern Python**: Type hints, dataclasses, pathlib

## Documentation

- [Atuin Import Reference](https://docs.atuin.sh/reference/import/)
- [zsh-histdb Project](https://github.com/larkery/zsh-histdb) (original SQLite history format)
- [Atuin Documentation](https://docs.atuin.sh/)

## Contributing

This tool addresses a common issue that affects many Atuin users. Contributions are welcome:

- **Bug Reports**: Found an edge case? Open an issue
- **Feature Ideas**: Have suggestions? Let's discuss
- **Code**: PRs welcome - please run tests first
- **Documentation**: Help improve the docs

## License

MIT License - Use freely, modify, distribute, contribute back if helpful!

---

**Made for shell power users**

_Reliable zsh history import for Atuin using the zsh-histdb method._
