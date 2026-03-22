FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY vmware_storage/ vmware_storage/
COPY mcp_server/ mcp_server/

RUN uv pip install --system .

CMD ["python", "-m", "mcp_server"]
