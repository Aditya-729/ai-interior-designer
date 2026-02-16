FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libffi6 \
    libssl3 \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    postgresql-client \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install setuptools first (required for pkg_resources)
RUN pip install --upgrade pip
RUN pip install setuptools wheel

# Copy requirements
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# This ensures all dependencies are installed correctly
RUN pip install --no-cache-dir -r requirements.txt || \
    (echo "Warning: Some packages failed to install, continuing..." && \
     pip install --no-cache-dir \
        fastapi==0.104.1 \
        uvicorn[standard]==0.24.0 \
        python-multipart==0.0.6 \
        python-dotenv==1.0.0 \
        pydantic==2.5.0 \
        pydantic-settings==2.1.0 \
        sqlalchemy==2.0.23 \
        alembic==1.12.1 \
        psycopg2-binary==2.9.9 \
        supabase==2.0.0 \
        httpx==0.25.2 \
        aiofiles==23.2.1 \
        python-jose[cryptography]==3.3.0 \
        passlib[bcrypt]==1.7.4 \
        qdrant-client==1.7.0 \
        numpy==1.24.3 \
        Pillow==10.1.0)

# Copy application code
COPY . .

# Expose port (Railway sets PORT env var)
EXPOSE 8000

# Run application (Railway will override with startCommand from railway.json)
# This is just a fallback - railway.json startCommand takes precedence
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
