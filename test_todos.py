import pytest
from command_line import *



class TestFetchTodos:

    def test_incorrect_api_url(self, mocker):
        mocker.patch('requests.get', side_effect=requests.RequestException("Invalid URL"))

        result = fetch_todos('https://invalid-url.com')

        assert result == [], "The function should return an empty list on failure"

    
    def test_handles_http_error_statuses_gracefully(self, mocker):
        mocker.patch('requests.get', side_effect=requests.RequestException("HTTP Error"))

        result = fetch_todos('https://jsonplaceholder.typicode.com/todos')

        
        assert result == [], "The function should return an empty list on HTTP error"

    
    def test_empty_list_on_http_error(self, mocker):
        mocker.patch('requests.get', side_effect=requests.RequestException("HTTP Error"))

        result = fetch_todos('https://jsonplaceholder.typicode.com/todos')

        assert result == [], "The function should return an empty list on HTTP error"

    
    def test_empty_json_response(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch('requests.get', return_value=mock_response)

        result = fetch_todos('https://jsonplaceholder.typicode.com/todos')

        assert result == [], "The function should return an empty list when API returns an empty JSON object"


    def test_handles_unexpected_json_structure(self, mocker):
        mock_response = mocker.Mock()
        unexpected_json = "This is not a valid JSON"
        mock_response.json.side_effect = ValueError("Expecting value")
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch('requests.get', return_value=mock_response)

        result = fetch_todos('https://jsonplaceholder.typicode.com/todos')

        assert result == [], "The function should handle unexpected JSON structure without crashing"


class TestFilterEvenTodos:

    def test_filters_only_even_todos(self):
        todos = [{'id': 1, 'title': 'Todo 1'}, {'id': 2, 'title': 'Todo 2'}, {'id': 3, 'title': 'Todo 3'}, {'id': 4, 'title': 'Todo 4'}]
        expected = [{'id': 2, 'title': 'Todo 2'}, {'id': 4, 'title': 'Todo 4'}]
        result = filter_even_todos(todos, 10)
        assert result == expected, "Should only contain even-numbered TODOs"

    def test_empty_input_list(self):
        todos = []
        expected = []
        result = filter_even_todos(todos, 10)
        assert result == expected, "Should return an empty list for empty input"

    def test_max_count_zero(self):
        todos = [{'id': 1, 'title': 'Todo 1'}, {'id': 2, 'title': 'Todo 2'}, {'id': 3, 'title': 'Todo 3'}, {'id': 4, 'title': 'Todo 4'}]
        expected = []
        result = filter_even_todos(todos, 0)
        assert result == expected, "Should return an empty list when max_count is zero"

    def test_all_odd_ids(self):
        todos = [{'id': 1, 'title': 'Todo 1'}, {'id': 3, 'title': 'Todo 3'}, {'id': 5, 'title': 'Todo 5'}]
        expected = []
        result = filter_even_todos(todos, 10)
        assert result == expected, "Should not contain any even-numbered TODOs"

    def test_max_count_larger_than_available(self):
        todos = [{'id': 1, 'title': 'Todo 1'}, {'id': 3, 'title': 'Todo 3'}, {'id': 5, 'title': 'Todo 5'}]
        expected = []
        result = filter_even_todos(todos, 5)
        assert result == expected, "Should return an empty list when max_count is larger than available even-numbered TODOs"

    def test_max_count_negative(self):
        todos = [{'id': 1, 'title': 'Todo 1'}, {'id': 2, 'title': 'Todo 2'}, {'id': 3, 'title': 'Todo 3'}, {'id': 4, 'title': 'Todo 4'}]
        expected = []
        result = filter_even_todos(todos, -5)
        assert result == expected, "Should return an empty list when max_count is negative"

    def test_handle_missing_id_key(self):
        todos = [{'title': 'Todo 1'}, {'id': 2, 'title': 'Todo 2'}, {'title': 'Todo 3'}, {'id': 4, 'title': 'Todo 4'}]
        expected = [{'id': 2, 'title': 'Todo 2'}, {'id': 4, 'title': 'Todo 4'}]
        result = filter_even_todos(todos, 10)
        assert result == expected, "Should handle cases where 'id' key is missing"

    def test_handle_non_integer_ids(self):
        todos = [{'id': 1.5, 'title': 'Todo 1'}, {'id': 2, 'title': 'Todo 2'}, {'id': '3', 'title': 'Todo 3'}, {'id': 4, 'title': 'Todo 4'}]
        expected = [{'id': 2, 'title': 'Todo 2'}, {'id': 4, 'title': 'Todo 4'}]
        result = filter_even_todos(todos, 10)
        assert result == expected, "Should gracefully handle non-integer 'id' values"
        