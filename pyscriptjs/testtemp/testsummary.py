from dataclasses import dataclass
from typing import Iterable

@dataclass
class TestSummary:
    time: str
    raw_results: str
    test_results: dict[str: 'TestResult']

    @property 
    def test_names(self) -> Iterable[str]:
        return (str(s) for s in self.test_results.keys())

@dataclass
class TestResult:
    name: str
    resultText: str
    passed: bool
    errorText: str
    