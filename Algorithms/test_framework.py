class TestAlgorithm:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def run(self, test_cases):
        for test_case in test_cases:
            self.run_test_case(test_case)

    def run_test_case(self, test_case):
        result = self.algorithm(test_case.input)
        assert result == test_case.expected, f"Expected {test_case.expected}, but got {result}"