import argparse
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_todos(api_url):
    """
    Fetch TODOs from the specified API URL and handle unexpected JSON structures.
    
    Args:
    api_url (str): URL to fetch the TODOs from.

    Returns:
    list: A list of TODOs if successful, empty list otherwise.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Validate the expected structure of JSON data
        if not isinstance(data, list):  # Assuming the expected type is a list of TODOs
            logging.error(f"Unexpected JSON structure: {data}")
            return []

        # Further checks can be added here if specific fields are expected
        return data

    except requests.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return []
    except ValueError as e:  # Includes JSON decoding errors
        logging.error(f"JSON decoding error: {e}")
        return []
    except TypeError as e:  # Handles errors like iterating over None
        logging.error(f"Type error in processing JSON data: {e}")
        return []


def filter_even_todos(todos, max_count):
    filtered_todos = []
    for todo in todos:
        if 'id' not in todo:
            logging.warning("Skipping TODO without an 'id'.")
            continue
        if not isinstance(todo['id'], int):
            logging.warning(f"Skipping TODO with non-integer 'id': {todo['id']}")
            continue
        if todo['id'] % 2 == 0:
            filtered_todos.append(todo)
        if len(filtered_todos) >= max_count:
            break
    return filtered_todos

def display_todos(todos):
    """Display each TODO's title and completion status."""
    for todo in todos:
        logging.info(f"Title: {todo['title']} - Completed: {'Yes' if todo['completed'] else 'No'}")

def main():
    parser = argparse.ArgumentParser(description="Fetch and display even numbered TODOs from an API.")
    parser.add_argument('--url', type=str, default='https://jsonplaceholder.typicode.com/todos', help='API URL to fetch TODOs from')
    parser.add_argument('--count', type=int, default=20, help='Number of even-numbered TODOs to display')
    
    args = parser.parse_args()

    todos = fetch_todos(args.url)
    even_todos = filter_even_todos(todos, args.count)
    display_todos(even_todos)

if __name__ == "__main__":
    main()
