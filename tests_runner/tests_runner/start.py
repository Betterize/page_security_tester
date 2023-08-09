def start():
    import os
    file = os.path.join('tests_runner', 'main.py')
    os.system(f'poetry run python {file}')