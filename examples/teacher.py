from __future__ import annotations

from textwrap import dedent
from typing import List

import js
from pyscript import Plugin, display, HTML

global repl_quizes
repl_quizes: List[PyReplQuiz] = []

class Teacher(Plugin):
    def configure(self, config):
        pass

    def afterPyReplExec(self, runtime, src, outEl, pyReplTag, result):
        js.console.log(result)

        global repl_quizes
        #print(f"{len(repl_quizes)= }")
        for repl_quiz in repl_quizes:
            #print(f"id: {repl_quiz.element.getAttribute('id')}")
            if pyReplTag.getAttribute("id") == repl_quiz.element.getAttribute('id') + "-repl":
                repl_quiz.process_repl_eval(result)

    def afterStartup(self, runtime):
        global repl_quizes
        repl_quizes[0].element.style.display = "block"

plugin = Teacher("teacher")

@plugin.register_custom_element("py-replquiz")
class PyReplQuiz:
    def __init__(self, element):
        self.element = element
        self.element.style.display = "none"

    @property
    def repl_id(self):
        return f"{self.element.getAttribute('id')}-repl"

    @property
    def results_id(self):
        return f"{self.element.getAttribute('id')}-output"

    def connect(self):
        global repl_quizes
        repl_quizes.append(self)

        self.question = self.element.querySelectorAll("py-question")[0].innerHTML
        self.answer_statement = dedent(self.element.querySelectorAll("py-answer")[0].innerHTML)

        #Create Question:
        self.question_div = js.document.createElement("div")
        self.question_div.innerHTML = self.question
        self.question_div.classList.add("question-text")
        self.element.appendChild(self.question_div)

        #Create Repl
        self.repl = js.document.createElement("py-repl")
        self.repl.setAttribute("id", self.repl_id)
        self.repl.setAttribute("output", self.results_id)
        self.element.appendChild(self.repl)

        #create result holder
        self.results = js.document.createElement("div")
        self.results.setAttribute("id", self.results_id)
        self.results.classList.add("result-holder")
        
        self.element.appendChild(self.results)

    def process_repl_eval(self, result):
        js.console.log(f"Got relevant result from repl: {result}")
        if result == None:
            self.results.style.backgroundColor = "#e2e29c"
            display("You didn't actually output the results from the REPL", append=False)
        else:
            success = eval(self.answer_statement)
            if success:
                self.results.style.backgroundColor = "#bddaa4"
                display("You got it right!", target=self.results_id, append = False)

                global repl_quizes
                current_index = repl_quizes.index(self)
                if current_index < len(repl_quizes) - 1:
                    repl_quizes[current_index+1].element.style.display = "block"
            else:
                self.results.style.backgroundColor = "#daa4b5"
                display(HTML(f"That's not quite right - you output <b>{result}</b>"), target=self.results_id, append=False)
