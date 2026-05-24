import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(f"{__file__}"))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(f"{__file__}/.."))))

def load_tests(loader, tests, pattern):
    """自动发现并加载所有测试模块"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in os.listdir(test_dir):
        if filename.startswith('test_') and filename.endswith('.py'):
            module_name = filename[:-3]
            try:
                module = __import__(f'tests.{module_name}', fromlist=[''])
                
                for name in dir(module):
                    if name.startswith('Test'):
                        test_class = getattr(module, name)
                        if isinstance(test_class, type) and issubclass(test_class, unittest.TestCase):
                            tests.addTests(loader.loadTestsFromTestCase(test_class))
            except Exception as e:
                print(f"Warning: Failed to load {module_name}: {e}")
    
    return tests

unittest.main(module='tests', verbosity=2)
