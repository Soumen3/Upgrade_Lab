# Use the official Debian base image from Docker Hub
FROM debian:latest

# Install GCC and G++ compilers
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Default command to run when the container starts
CMD ["/bin/bash"]
