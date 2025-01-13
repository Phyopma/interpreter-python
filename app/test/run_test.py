import subprocess
import unittest
import os


class TestLox(unittest.TestCase):
    def setUp(self):
        self.project_root = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        self.program_script = os.path.join(
            self.project_root, 'your_program.sh')
        self.test_lox = os.path.join(self.project_root, 'test.lox')

        # Test root directory
        self.test_root_dir = os.path.join(self.project_root, 'app/test')

    def read_test_cases(self, script_file, expected_file):
        """Read test cases from script.txt and expected.txt"""
        test_cases = {}

        # Read scripts
        with open(script_file, 'r') as f:
            current_test = None
            current_script = []

            for line in f:
                if line.startswith('### TEST:'):
                    if current_test and current_script:
                        test_cases[current_test] = {
                            'script': ''.join(current_script).strip()}
                    current_test = line.strip().split('### TEST:')[1].strip()
                    current_script = []
                elif line.startswith('### END'):
                    if current_test and current_script:
                        test_cases[current_test] = {
                            'script': ''.join(current_script).strip()}
                else:
                    current_script.append(line)

        # Read expected outputs
        with open(expected_file, 'r') as f:
            current_test = None
            current_output = []

            for line in f:
                if line.startswith('### TEST:'):
                    if current_test and current_output and current_test in test_cases:
                        test_cases[current_test]['expected'] = ''.join(
                            current_output).strip()
                    current_test = line.strip().split('### TEST:')[1].strip()
                    current_output = []
                elif line.startswith('### END'):
                    if current_test and current_output and current_test in test_cases:
                        test_cases[current_test]['expected'] = ''.join(
                            current_output).strip()
                else:
                    current_output.append(line)

        return test_cases

    def run_test_case(self, script, expected_output):
        """Run a single test case"""

        # Save the original content of test.lox
        with open(self.test_lox, 'r') as f:
            original_content = f.read()

        try:
            # Write script to test.lox
            with open(self.test_lox, 'w') as f:
                f.write(script)

            # Run interpreter
            result = subprocess.run(
                ['/bin/bash', self.program_script, 'run', self.test_lox],
                capture_output=True,
                text=True
            )

            output = result.stdout.strip(
            ) if result.stderr == "Logs from your program will appear here!\n" else result.stderr.strip()
            # Compare output
            self.assertEqual(

                expected_output.strip(),
                output,
                f"Test failed!\nExpected:\n{
                    expected_output}\nGot:\n{output}"
            )
        finally:
            # Restore the original content of test.lox
            with open(self.test_lox, 'w') as f:
                f.write(original_content)

    def test_all_cases(self):
        """Run all test cases in all subdirectories"""
        for root, dirs, files in os.walk(self.test_root_dir):
            if 'script.txt' in files and 'expected.txt' in files:
                script_file = os.path.join(root, 'script.txt')
                expected_file = os.path.join(root, 'expected.txt')
                test_cases = self.read_test_cases(script_file, expected_file)

                for test_name, test_data in test_cases.items():
                    with self.subTest(test_name):
                        print(f"Running test: {test_name} in {
                              root.split('/')[-1]}")
                        self.run_test_case(
                            test_data['script'],
                            test_data['expected']
                        )


if __name__ == '__main__':
    unittest.main()
