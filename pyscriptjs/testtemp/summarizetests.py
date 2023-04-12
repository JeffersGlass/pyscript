import re
from subprocess import run
from typing import Iterable

from termcolor import colored


from testsummary import TestSummary, TestResult

times = ['745a', '755a', '810a', '932a', '1024a', '1050a', '229p']

def findResults(text:str) -> Iterable[re.Match]:
    resultExp = re.compile("\[gw\d\] \[\s+\d+%\] (?P<result>\w+) (?P<test_specifier>.+)")
    return re.finditer(resultExp, text)

def parseResult(result: re.Match) -> tuple[str, TestResult]:
    name = result.group('test_specifier').strip()
    resultText = result.group('result')
    passed = True if resultText in ['PASSED', 'XFAIL', 'SKIPPED'] else False
    errorText = '' #To be implemented
    return name, TestResult(
        name=name,
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
        
        results = findResults(contents)        
        data.append(TestSummary(time=t, raw_results=contents, test_results={parseResult(result)[0]: parseResult(result)[1] for result in results}))
    

    allTests = set(s for ts in data for s in ts.test_names) | set(collectedTests)
    allTests = sorted(list(allTests), )
    for test_name in allTests:
        print(f"{test_name: <130}", end='')
        for summary in data:
            if test_name in summary.test_results:
                result_text = summary.test_results[test_name].resultText
                if result_text == 'PASSED':
                    print(colored('O', color='green'), end='')
                elif result_text in ('XFAIL', 'SKIPPED'):
                    print(colored('O', color='yellow'), end='')
                else:
                    print(colored('X', color='red'), end='')
            else:
                print(colored('X', color='yellow', on_color='on_magenta'), end='')
                #print(colored('█', color='BLUE'), end='')
                
             

        print("")
