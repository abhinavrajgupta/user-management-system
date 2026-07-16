# Dockerfile for FastAPI Backend
#
# A Dockerfile is a recipe for building a Docker image.
# Each instruction creates a new layer in the image.
# Layers are cached, so unchanged layers don't rebuild (faster builds).
#
# To build manually: docker build -t user-mgmt-backend .
# To run manually:  docker run -p 8000:8000 user-mgmt-backend

# ---- Base Image ----
# We use Python 3.11 slim (minimal OS) to keep the image small
FROM python:3.11-slim

# ---- Working Directory ----
# All subsequent commands run from /app inside the container
WORKDIR /app

# ---- Install System Dependencies ----
# gcc is needed to compile some Python packages (e.g., cryptography)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python Dependencies ----
# Copy requirements first so Docker can cache this layer
# (only rebuilds if requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy Application Code ----
# Copy all backend code into the container
COPY . .

# ---- Expose Port ----
# Documents that the container uses port 8000 (doesn't actually open it)
EXPOSE 8000

# ---- Start Command ----
# This is the command Docker runs when the container starts
# --host 0.0.0.0 makes FastAPI accessible from outside the container
# --reload enables auto-reload on code changes (dev only)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
