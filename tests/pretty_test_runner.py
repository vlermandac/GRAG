import time
import unittest
from rich.console import Console
from rich.traceback import install

# Install rich traceback globally so that it formats all exceptions
install(show_locals=True)


class RichTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console()

    def startTest(self, test):
        super().startTest(test)
        self.console.print(f"[bold blue]Starting[/bold blue] {test}")

    def addSuccess(self, test):
        super().addSuccess(test)
        self.console.print(f"[green]PASS[/green]: {test}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.console.print(f"[red]FAIL[/red]: {test}")

    def addError(self, test, err):
        super().addError(test, err)
        self.console.print(f"[red]ERROR[/red]: {test}")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.console.print(f"[yellow]SKIPPED[/yellow]: {test} - {reason}")


class RichTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.testResultClass = RichTestResult
        self.console = Console()

    def run(self, test):
        start_time = time.time()
        result = super().run(test)
        end_time = time.time()

        total_time = end_time - start_time

        # Count the number of successes, failures, errors, and skips
        num_successes = len(result.successes) if hasattr(result, 'successes') else "unknown"
        num_failures = len(result.failures)
        num_errors = len(result.errors)
        num_skips = len(result.skipped)

        self.console.print(f"Ran {result.testsRun} tests in {total_time:.3f}s")
        self.console.print(f"Passed: {num_successes}, "
                           f"Failures: {num_failures}, "
                           f"Errors: {num_errors}, "
                           f"Skipped: {num_skips}")

        return result
