# Python TODO Application with Docker

This repository contains a Python script that fetches and displays even-numbered TODO items from a JSON API. It includes a Dockerfile for building a Docker image that runs the script in an isolated environment.

## Files

- `command_line.py`: The main Python script.
- `Dockerfile`: Dockerfile to build the container image.
- `requirements.txt`: File containing all necessary Python packages.

## Python Script (`command_line.py`)

The Python script fetches TODOs from a specified API URL, filters for even-numbered TODOs, and displays their titles and completion statuses. The script uses `argparse` for command-line argument parsing, `requests` for HTTP requests, and `logging` for basic logging.

### Features

- **Fetch Data**: Connects to any provided API endpoint and retrieves TODO data.
- **Filter Data**: Filters the retrieved data to show only even-numbered TODOs.
- **Display Data**: Prints the TODOs' title and whether they have been completed.

### Usage
Build The Docker Image

```bash
docker build -t my-python-app .
```

Run the script using the following command:

```bash
docker run my-python-app --url "https://jsonplaceholder.typicode.com/todos" --count "20"
```

Run the tests using the following command:

```bash
docker run --entrypoint pytest my-python-app /app/test_todos.py


