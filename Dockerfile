FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN apt-get update && apt-get install -y curl build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

COPY . .

RUN uv sync --frozen

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "main.py"]