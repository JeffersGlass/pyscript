import re
from subprocess import run
from typing import Iterable

from termcolor import colored


from testsummary import TestSummary, TestResult

times = ['745a', '755a', '810a', '932a', '1024a', '1050a', '229p', '1157a2', '1223p2', '126p2_2']

def findStartedTests(text:str) -> Iterable[re.Match]:
    """ Find all tests in a log that were started """
    startedExp = re.compile("^tests/integration/(?P<module_name>[\w\.]+)::(?P<class_name>[\w_]+)::(?P<test_name>[\w_]+)\[chromium\]", flags=re.MULTILINE)
    return re.finditer(startedExp, text)

def parseStartedResult(result: re.Match) -> TestResult:
    name = f"tests/integration/{result.group('module_name')}::{result.group('class_name')}::{result.group('test_name')}[chromium]"
    return name, TestResult(
        name = name,
        completed=False,
        resultText="NEVERFINISHED",
        passed=False,
        errorText=''
    )

def findCompletedTests(text:str) -> Iterable[re.Match]:
    """ Find all tests in a log that were completed """
    resultExp = re.compile("\[gw\d\] \[\s+\d+%\] (?P<result>\w+) (?P<test_specifier>.+)")
    return re.finditer(resultExp, text)

def parseCompletedResult(result: re.Match) -> tuple[str, TestResult]:
    """ Parse a single match from findCompletedResults to get the remaining data """
    name = result.group('test_specifier').strip()
    resultText = result.group('result')
    passed = True if resultText in ['PASSED', 'XFAIL', 'SKIPPED'] else False
    errorText = '' #To be implemented
    return name, TestResult(
        name=name,
        completed=True,
        resultText=resultText,
        passed=passed,
        errorText=errorText,
    )

def allPytestTests() -> list[str]:
    cmd = 'pytest ../tests/integration --collect-only'
    data = run(cmd, capture_output=True, shell=True)
    lines = [str(d) for d in data.stdout.splitlines()]

    modulePattern = re.compile("b'\s+<Module (?P<modulename>(\w)+.py)>'")
    currentModule = ''

    classPattern = re.compile("b'\s+<Class (?P<classname>(\w)+.)>'")
    currentClass = ''
    
    testPattern = re.compile("b'\s+<Function (?P<functionname>.+)>'")

    tests = []
    
    for line in lines:
        if m:= re.match(modulePattern, line): 
            currentModule = m.group('modulename')
        elif m:= re.match(classPattern, line):
            currentClass = m.group('classname')
        elif m:= re.match(testPattern, line):
            testName = f"tests/integration/{currentModule}::{currentClass}::{m.group('functionname')}".strip()
            tests.append(testName)
    return tests


if __name__ =='__main__':

    collectedTests = allPytestTests()
        
    data: list[TestSummary] = []

    for t in times:
        with open(f'{t}.txt', 'r', encoding='utf-8') as f:
            contents = f.read()
        
        startedTests = list(findStartedTests(contents))
        completedTests = list(findCompletedTests(contents))
        
        startedNotCompleted = set(c.group().strip() for c in startedTests) - set(c.group('test_specifier').strip() for c in completedTests)

        '''print(f"{len(startedTests)=   }")
        print(f"{len(completedTests)= }\n")
        for pair in zip(sorted([c.group('test_specifier') for c in completedTests]), sorted([c.group() for c in startedTests])):
            print(f">>{pair[0]}<<\n>>{pair[1]}<<\n")
        continue'''

        new_summary = TestSummary(time=t, raw_results=contents, test_results={parseCompletedResult(result)[0]: parseCompletedResult(result)[1] for result in completedTests})     
        new_summary.test_results.update({test: TestResult(name=test, completed=False, resultText="NEVERFINISHED", passed=False, errorText='') for test in startedNotCompleted})
        data.append(new_summary)

    allTests = set(s for ts in data for s in ts.test_names) | set(collectedTests)
    allTests = sorted(list(allTests), )

    # _ => Passed
    # F => Failed
    # E => Error
    # U => Never Completed
    # . => Never Started

    for test_name in allTests:
        output = ""
        
        for summary in data:
            if test_name in summary.test_results:
                result_text = summary.test_results[test_name].resultText
                if result_text == 'PASSED':
                    output += colored('_', color='green')
                elif result_text == 'NEVERFINISHED':
                    output += colored('U', color='white')
                elif result_text == 'FAILED':
                    output += colored('F', color='red') 
                elif result_text == 'ERROR':
                    output += colored('E', color='white', on_color='on_red')
                elif result_text in ('XFAIL', 'SKIPPED', 'XPASS'): #Not usually displayed
                    output += colored('@', color='yellow')
                else:
                    raise ValueError(f"Unknown result: {result_text}")
            else:
                output += colored(':', color='yellow')
        if any(char in ('F', '?', 'X') for char in output): print(f"{test_name: <130}{output}")
