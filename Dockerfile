# ----------------------
# Builder stage
# ----------------------
FROM python:3.12-slim-bookworm AS builder

# Install system dependencies for Tkinter + build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk \
    build-essential \
    libx11-6 libxext6 libxrender1 libxrandr2 \
    libxinerama1 libxcursor1 libxcomposite1 libasound2 \
    libglib2.0-0 libsm6 libxcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend .
COPY frontend .

RUN pip install --no-cache-dir -r ./backend/requirements.txt pyinstaller

RUN pyinstaller --onefile bot.py --name bot

FROM python:3.12-slim-bookworm

# Install Tkinter + GUI libs required by the binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk \
    libx11-6 libxext6 libxrender1 libxrandr2 \
    libxinerama1 libxcursor1 libxcomposite1 libasound2 \
    libglib2.0-0 libsm6 libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the binary from builder
COPY --from=builder /app/dist/bot /usr/local/bin/bot

# Set entrypoint
# ENTRYPOINT ["/usr/local/bin/bot"]
# CMD ["cli"]