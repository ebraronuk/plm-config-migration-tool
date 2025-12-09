import importlib
import unittest


class TestModuleImports(unittest.TestCase):
    MODULES = [
        "src.excel.reader",
        "src.excel.validator",
        "src.excel.normalizer",
        "src.bom.parser",
        "src.sql.generator",
        "src.utils.logger",
    ]

    def test_imports(self):
        for module_path in self.MODULES:
            with self.subTest(module=module_path):
                importlib.import_module(module_path)

    def test_logger_instance(self):
        logger_module = importlib.import_module("src.utils.logger")
        logger = logger_module.setup_logger()
        self.assertEqual(logger.name, "plmtool")


if __name__ == "__main__":
    unittest.main()
