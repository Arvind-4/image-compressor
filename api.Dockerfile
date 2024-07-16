FROM python:3.10-slim

WORKDIR /backend
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /backend/commands/entrypoint.sh

ENTRYPOINT ["/backend/commands/entrypoint.sh"]
