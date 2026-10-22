FROM python:3.11-slim

WORKDIR /FS ASS3

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .

ENV HOST="host.docker.internal" 
ENV PORT="3306"
ENV USERNAME="root"
ENV PASSWORD=""

EXPOSE 9000

# Use Uvicorn to run the app properly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]