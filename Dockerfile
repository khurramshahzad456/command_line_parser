
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "command_line.py"]
CMD ["--url", "https://jsonplaceholder.typicode.com/todos", "--count", "20"]