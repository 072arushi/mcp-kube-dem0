FROM python:3.11-slim

WORKDIR /app
COPY mcp_server.py .

RUN pip install --no-cache-dir fastapi uvicorn pydantic

CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "8080"]
