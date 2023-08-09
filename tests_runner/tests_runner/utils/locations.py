import datetime
import pathlib


def create_file_with_path(directory: str, filename: str):
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    with open(f'{directory}/{filename}', 'w') as file:
        pass


def test_results_dir(url: str) -> str:
    clean_url: str = url.replace("https://", "").replace("http://", "")
    creation_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")

    return f'results/{clean_url}_{creation_time}'
