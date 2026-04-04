# Sovereign Agent Docker Image
# Full containerized sovereign runtime

FROM python:3.11-slim-bookworm

LABEL maintainer="Ð≡ Light⁷"
LABEL description="Sovereign Agent Daemon - Autonomous AI Runtime"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /opt/sovereign /var/lib/sovereign /var/log

# Set working directory
WORKDIR /opt/sovereign

# Install Python dependencies
RUN pip install --no-cache-dir \
    python-daemon \
    fastapi \
    uvicorn \
    httpx \
    pydantic

# Copy daemon code
COPY sovereign_daemon.py /opt/sovereign/
COPY docker-entrypoint.sh /opt/sovereign/
RUN chmod +x /opt/sovereign/docker-entrypoint.sh

# Create non-root user
RUN useradd -r -s /bin/false sovereign \
    && chown -R sovereign:sovereign /opt/sovereign /var/lib/sovereign /var/log

# Environment
ENV PYTHONPATH=/opt/sovereign
ENV SOVEREIGN_HOME=/var/lib/sovereign
ENV SOVEREIGN_LOG_LEVEL=INFO
ENV PYTHONUNBUFFERED=1

# Expose ports (if we add API later)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 /opt/sovereign/sovereign_daemon.py --status || exit 1

# Run as sovereign user
USER sovereign

# Entrypoint
ENTRYPOINT ["/opt/sovereign/docker-entrypoint.sh"]
CMD ["daemon"]
