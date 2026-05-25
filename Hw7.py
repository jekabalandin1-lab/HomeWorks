import time
import logging
import unittest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Функція '{func.__name__}' виконувалася: {execution_time:.6f} с.")
        return result, execution_time
    return wrapper

@timer_decorator
def sample_function(seconds):
    time.sleep(seconds)
    return "Done"

class TestTimerDecorator(unittest.TestCase):

    def test_timer_duration(self):
        test_delay = 0.1
        result, exec_time = sample_function(test_delay)
        self.assertEqual(result, "Done")
        self.assertGreaterEqual(exec_time, test_delay)

    def test_function_math_logic(self):
        @timer_decorator
        def add(a, b):
            return a + b
        result, exec_time = add(10, 20)
        self.assertEqual(result, 30)
        self.assertGreaterEqual(exec_time, 0)

if __name__ == "__main__":
    sample_function(0.5)
    unittest.main()