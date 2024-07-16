FROM python:3.10-slim

WORKDIR /backend
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /backend/commands/background-task.sh

ENTRYPOINT ["/backend/commands/background-task.sh"]
