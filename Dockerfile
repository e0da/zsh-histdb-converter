# Use Alpine for minimal image size
FROM python:3.12-alpine

# Install git (required for uvx to clone from GitHub)
RUN apk add --no-cache git

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Create non-root user (Alpine uses adduser instead of useradd)
RUN adduser -D -s /bin/sh app

# Switch to non-root user
USER app
WORKDIR /home/app

# Create data directory for output
RUN mkdir -p /home/app/data

# Set the entrypoint to run zsh-histdb-converter via uvx
ENTRYPOINT ["uvx", "--from", "git+https://github.com/e0da/zsh-histdb-converter", "zsh-histdb-converter"]

# Default command shows help
CMD ["--help"]
