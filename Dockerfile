FROM debian:bullseye

# Install build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    openjdk-11-jdk \
    ca-certificates \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source files
COPY . /app

# Default command
CMD ["/bin/bash"]
