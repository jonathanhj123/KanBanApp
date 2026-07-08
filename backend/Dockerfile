# Dev image for the FastAPI backend.
# Dependencies bake into the image (rebuilt by `docker compose up --build`);
# the CODE does not need a rebuild — compose bind-mounts ./backend over /app
# and uvicorn --reload picks up every save.
FROM python:3.12-slim

WORKDIR /app

# Copy requirements alone first: Docker caches this layer, so rebuilds are
# instant unless requirements.txt actually changed.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
