# --- build: resolve dependencies into an isolated venv -------------------------
FROM public.ecr.aws/docker/library/python:3.13-slim AS builder

ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN python -m venv /opt/venv
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

# --- runtime -------------------------------------------------------------------
FROM public.ecr.aws/docker/library/python:3.13-slim

# Lambda Web Adapter runs as an extension and proxies Lambda events to the HTTP server on :8080.
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY app/ ./app/
# Lambda's filesystem is read-only, so precompile bytecode at build time for faster cold starts.
RUN python -m compileall -q app

USER 1000
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
