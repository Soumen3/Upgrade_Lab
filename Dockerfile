# Use a lightweight Linux image with gcc
FROM gcc

# Set workdir
WORKDIR /app

# Copy C file into container (we'll override this with volume)
COPY . /app

RUN apt-get update && apt-get install -y g++

# Default command (can be overridden at runtime)
CMD ["/bin/bash"]
