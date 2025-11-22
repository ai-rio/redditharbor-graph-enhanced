# RedditHarbor Graph Enhanced - Deployment Guide

## Overview

RedditHarbor Graph Enhanced is an advanced Reddit data collection platform integrated with Deep-Graph-MCP for intelligent code analysis and automated refactoring. This guide covers deployment strategies, configuration, and production considerations.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    RedditHarbor Enhanced                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend/API Layer                                         │
│  ├── REST API (FastAPI)                                    │
│  ├── GraphQL Interface                                      │
│  └── WebSocket Support                                      │
├─────────────────────────────────────────────────────────────┤
│  Core Processing Layer                                      │
│  ├── Reddit API Integration                                │
│  ├── Data Collection Pipeline                                │
│  ├── DLT Activity Validation                                 │
│  ├── Deduplication System                                    │
│  └── Quality Filters                                         │
├─────────────────────────────────────────────────────────────┤
│  Intelligence Layer (NEW)                                    │
│  ├── Deep-Graph-MCP Integration                            │
│  ├── Code Analysis Engine                                   │
│  ├── Dependency Mapping                                     │
│  ├── Automated Refactoring                                   │
│  └── Architecture Analysis                                   │
├─────────────────────────────────────────────────────────────┤
│  Storage Layer                                               │
│  ├── Supabase Database                                      │
│  ├── Vector Store (for embeddings)                          │
│  ├── File Storage                                            │
│  └── Cache Layer                                             │
├─────────────────────────────────────────────────────────────┤
│  External Services                                          │
│  ├── Reddit API                                             │
│  ├── DeepGraph Project                                       │
│  ├── Jina AI Services                                       │
│  └── Monitoring Services                                     │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### System Requirements

- **CPU**: 4+ cores recommended
- **Memory**: 8GB+ RAM minimum, 16GB+ recommended
- **Storage**: 50GB+ free space
- **Network**: Stable internet connection for Reddit API and DeepGraph

### Software Dependencies

- **Python**: 3.8+
- **Node.js**: 16+ (for some tools)
- **PostgreSQL**: 13+ (via Supabase)
- **Redis**: 6+ (for caching)
- **Docker**: 20+ (optional)

### External Services

- **Reddit API Access**: Client ID and Secret
- **Supabase Project**: Database and auth services
- **DeepGraph Project**: AI-powered code analysis
- **Jina AI**: AI services for content analysis (optional)

## Installation

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/ai-rio/redditharbor-graph-enhanced.git
cd redditharbor-graph-enhanced

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
uv sync
# or: pip install -r requirements.txt

# Set up environment
cp .env.example .env
```

### 2. Configuration

#### Environment Variables (.env)

```bash
# Reddit API Configuration
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=RedditHarbor/1.0

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# DeepGraph Configuration
DEEP_GRAPH_PROJECT_ID=your_deepgraph_project_id
DEEP_GRAPH_API_KEY=your_deepgraph_api_key
DEEP_GRAPH_ENDPOINT=https://api.deepgraph.co

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:54322/postgres
REDIS_URL=redis://localhost:6379/0

# Application Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
ENABLE_PII_ANONYMIZATION=true
SECRET_KEY=your_secret_key_here

# Performance
MAX_WORKERS=4
CACHE_TTL=3600
RATE_LIMIT_PER_MINUTE=100
```

#### Database Setup

```bash
# Start Supabase locally (if using local development)
supabase start

# Run migrations
supabase db push

# Verify connection
python -c "from config.settings import DB_CONFIG; print('Database connected')"
```

### 3. DeepGraph Integration

#### Create DeepGraph Project

1. Visit: https://deepgraph.co
2. Create new project: "redditharbor-graph-enhanced"
3. Note project ID and API key
4. Add to environment variables

#### Initialize Graph Integration

```python
# Test DeepGraph connection
python -c "
from core.graph_integration import RedditHarborGraphAnalyzer
analyzer = RedditHarborGraphAnalyzer()
print(f'Deep-Graph-MCP available: {analyzer.graph_available}')
"
```

## Deployment Options

### Option 1: Local Development

```bash
# Start all services
python scripts/start_dev_server.py

# Or use individual components
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
python scripts/collection_runner.py
python scripts/graph_analyzer.py
```

### Option 2: Docker Deployment

#### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  redditharbor:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDDIT_CLIENT_ID=${REDDIT_CLIENT_ID}
      - REDDIT_CLIENT_SECRET=${REDDIT_CLIENT_SECRET}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - DEEP_GRAPH_PROJECT_ID=${DEEP_GRAPH_PROJECT_ID}
      - DEEP_GRAPH_API_KEY=${DEEP_GRAPH_API_KEY}
    volumes:
      - ./logs:/app/logs
      - ./backups:/app/backups
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=redditharbor
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - redditharbor
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

#### Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f redditharbor

# Scale services
docker-compose up -d --scale redditharbor=3
```

### Option 3: Cloud Deployment

#### AWS ECS

```yaml
# ecs-task-definition.json
{
  "family": "redditharbor-graph-enhanced",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "redditharbor",
      "image": "your-account.dkr.ecr.region.amazonaws.com/redditharbor:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "REDDIT_CLIENT_ID",
          "value": "${REDDIT_CLIENT_ID}"
        },
        {
          "name": "SUPABASE_URL",
          "value": "${SUPABASE_URL}"
        },
        {
          "name": "DEEP_GRAPH_PROJECT_ID",
          "value": "${DEEP_GRAPH_PROJECT_ID}"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/redditharbor",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Google Cloud Run

```bash
# Build and deploy to Google Cloud Run
gcloud builds submit --tag gcr.io/your-project/redditharbor:latest

gcloud run deploy redditharbor \
  --image gcr.io/your-project/redditharbor:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --set-env-vars REDDIT_CLIENT_ID=your_client_id,SUPABASE_URL=your_supabase_url
```

## Production Configuration

### Performance Tuning

#### Application Settings

```python
# config/production.py
import os

class ProductionConfig:
    # Database
    DATABASE_POOL_SIZE = 20
    DATABASE_MAX_OVERFLOW = 30
    DATABASE_POOL_TIMEOUT = 30
    DATABASE_POOL_RECYCLE = 3600

    # Caching
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.getenv("REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = "redditharbor:"

    # Workers
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    WORKER_TIMEOUT = 300
    WORKER_KEEPALIVE = 2

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = 100
    RATE_LIMIT_PER_HOUR = 1000

    # Security
    ENABLE_CORS = False
    ENABLE_HTTPS = True
    SESSION_TIMEOUT = 3600

    # Monitoring
    ENABLE_METRICS = True
    METRICS_PORT = 9090
    HEALTH_CHECK_INTERVAL = 30

    # Deep-Graph-MCP
    DEEP_GRAPH_CACHE_TTL = 1800
    DEEP_GRAPH_BATCH_SIZE = 50
    DEEP_GRAPH_TIMEOUT = 30
```

#### Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream redditharbor {
        server redditharbor:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # API rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://redditharbor;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Health check
        location /health {
            proxy_pass http://redditharbor/health;
            access_log off;
        }
    }
}
```

### Monitoring and Logging

#### Application Monitoring

```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import logging
import time

# Metrics
REQUEST_COUNT = Counter('redditharbor_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('redditharbor_request_duration_seconds', 'Request duration')
ACTIVE_CONNECTIONS = Gauge('redditharbor_active_connections', 'Active connections')
COLLECTION_ERRORS = Counter('redditharbor_collection_errors_total', 'Collection errors', ['error_type'])
GRAPH_ANALYSIS_TIME = Histogram('redditharbor_graph_analysis_duration_seconds', 'Graph analysis time')

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()

        # Increment request counter
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        REQUEST_COUNT.labels(method=method, endpoint=path).inc()

        # Process request
        def custom_start_response(status, headers):
            # Record request duration
            REQUEST_DURATION.observe(time.time() - start_time)
            return start_response(status, headers)

        return self.app(environ, custom_start_response)

# Start metrics server
start_http_server(8001)
```

#### Logging Configuration

```python
# config/logging.py
import logging
import sys
from pathlib import Path

def setup_logging(log_level="INFO"):
    """Configure structured logging."""

    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Configure formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler for application logs
    file_handler = logging.FileHandler(logs_dir / "app.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # File handler for error logs
    error_handler = logging.FileHandler(logs_dir / "errors.log")
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if log_level == "DEBUG" else logging.INFO)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    # Suppress noisy loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
```

## Security Considerations

### API Security

```python
# security/auth.py
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

class SecurityManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.algorithm = "HS256"

    def generate_token(self, user_id, expires_in=3600):
        """Generate JWT token."""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=expires_in),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token):
        """Verify JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def require_auth(f):
    """Authentication decorator."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "No token provided"}), 401

        try:
            token = token.replace("Bearer ", "")
            payload = security_manager.verify_token(token)
            if not payload:
                return jsonify({"error": "Invalid token"}), 401

            request.current_user_id = payload["user_id"]
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": "Authentication failed"}), 401

    return decorated
```

### Data Privacy

```python
# privacy/pii_anonymizer.py
import spacy
import re
from typing import Dict, Any, List

class PIIAnonymizer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            self.nlp = None
            logger.warning("spaCy model not available, using basic PII detection")

    def anonymize_text(self, text: str) -> str:
        """Anonymize PII from text."""
        if self.nlp:
            return self._spaCy_anonymize(text)
        else:
            return self._basic_anonymize(text)

    def _spaCy_anonymize(self, text: str) -> str:
        """Anonymize using spaCy NER."""
        doc = self.nlp(text)
        anonymized = text

        # Replace detected entities
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "EMAIL"]:
                anonymized = anonymized.replace(ent.text, f"[{ent.label_}]")

        return anonymized

    def _basic_anonymize(self, text: str) -> str:
        """Basic regex-based PII detection."""
        # Email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = re.sub(email_pattern, "[EMAIL]", text)

        # Phone patterns
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        text = re.sub(phone_pattern, "[PHONE]", text)

        # Username patterns
        username_pattern = r'\b/u/[A-Za-z0-9_-]+\b'
        text = re.sub(username_pattern, "[USERNAME]", text)

        return text

    def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize PII from structured data."""
        anonymized = data.copy()

        for key, value in anonymized.items():
            if isinstance(value, str):
                anonymized[key] = self.anonymize_text(value)

        return anonymized
```

## Maintenance

### Automated Updates

```bash
# scripts/update_dependencies.sh
#!/bin/bash

echo "Updating dependencies..."

# Update Python dependencies
pip install --upgrade -r requirements.txt

# Update Deep-Graph-MCP tools
pip install --upgrade mcp-tools

# Run tests
python tests/test_graph_integration.py

# Update documentation
python scripts/generate_docs.py

echo "Update complete!"
```

### Backup Strategy

```python
# scripts/backup.py
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

class BackupManager:
    def __init__(self, backup_dir="backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_database_backup(self):
        """Create database backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"database_backup_{timestamp}.sql"

        cmd = f"pg_dump $DATABASE_URL > {backup_file}"
        subprocess.run(cmd, shell=True, check=True)

        return backup_file

    def create_code_backup(self):
        """Create code backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"code_backup_{timestamp}.tar.gz"

        # Create archive excluding node_modules and __pycache__
        cmd = f"tar -czf {backup_file} --exclude='node_modules' --exclude='__pycache__' --exclude='.git' ."
        subprocess.run(cmd, shell=True, check=True)

        return backup_file

    def cleanup_old_backups(self, keep_count=10):
        """Remove old backups, keeping only the most recent."""
        db_backups = sorted(self.backup_dir.glob("database_backup_*.sql"))
        code_backups = sorted(self.backup_dir.glob("code_backup_*.tar.gz"))

        for backup in db_backups[:-keep_count]:
            backup.unlink()

        for backup in code_backups[:-keep_count]:
            backup.unlink()
```

This comprehensive deployment guide provides all the necessary information for deploying RedditHarbor Graph Enhanced in various environments, from local development to cloud production deployments.