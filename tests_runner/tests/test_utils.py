from tests_runner.utils.locations import create_file_with_path, results_dir
import pytest
import datetime
from unittest.mock import MagicMock


class TestResultDir:
    FAKE_NOW = datetime.datetime(2023, 3, 3, 3)
    FAKE_NOW_STR = datetime.datetime(2023, 3, 3, 3).strftime("%Y-%m-%d_%H:%M")

    @pytest.fixture()
    def mock_datetime_now(self, monkeypatch):
        datetime_mock = MagicMock(wraps=datetime.datetime)
        datetime_mock.now.return_value = self.FAKE_NOW
        monkeypatch.setattr(datetime, "datetime", datetime_mock)


    def test_https(self, mock_datetime_now):
        url = "https://example.pl"
        
        assert results_dir(url=url) == f'results/example.pl_{self.FAKE_NOW_STR}'

    def test_http(self, mock_datetime_now):
        url = "http://example.pl"
        
        assert results_dir(url=url) == f'results/example.pl_{self.FAKE_NOW_STR}'

    
    def test_plain_page(self, mock_datetime_now):
        url = "example.pl"
        
        assert results_dir(url=url) == f'results/example.pl_{self.FAKE_NOW_STR}'

    
    def test_date_cut(self, mock_datetime_now):
        url = "example.pl"
        
        assert not results_dir(url=url) == f'results/example.pl_{self.FAKE_NOW}'


class TestCreateFileWithPath:

    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path / "test_dir"

    def test_creates_file(self, temp_dir):
        filename = "test_file.txt"
        create_file_with_path(temp_dir, filename)

        file_path = temp_dir / filename
        assert file_path.is_file()

    def test_existing_file(self, temp_dir):
        filename = "test_file.txt"
        file_path = temp_dir / filename

        create_file_with_path(temp_dir, filename)
        create_file_with_path(temp_dir, filename)

        assert file_path.is_file()

    def test_path_nested_directory(self, temp_dir):
        nested_dir = "nested"
        filename = "test_file.txt"
        nested_path = temp_dir / nested_dir

        create_file_with_path(nested_path, filename)

        file_path = nested_path / filename
        assert file_path.is_file()
