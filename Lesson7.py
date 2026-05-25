import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info('program started successfully')

try:
    a = 1 / 0
except ZeroDivisionError:
    logging.exception('user tried to divide by zero')
file_path = input('Please enter the file path: ')
try:
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    logging.exception(f'{file_path} file not found')