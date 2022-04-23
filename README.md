## Finding Replacement APIs for API Deprecations in Python

### Project Outline and Motivations
---
Python is a popular programming language that is widely used nowadays, with much of its current popularity attributed to the rich set of libraries and frameworks that its users can tap on. However, Python libraries often face the same problems that libraries in other programming languages face - that of missing APIs. APIs go missing when libraries are upgraded through different versions, and developers of client programs often have to manually search for replacements to the missing APIs when updating library versions.This is a difficult and time-consuming process, and there is currently no existing method to automatically find replacement APIs in Python.

We propose a data mining based approach to automatically find and extract possible replacement APIs. This is done through implementing a set heuristics to search three different sources - source code, release notes and the online Q\&A site StackOverflow. An evaluation of our method shows that our solution can find replacement APIs accurately, with results matching the accuracy of state-of-the-art methods implemented in other languages. With our heuristic-based mining for official documentation and source code, we have managed to attain a combined F1 score of 83.83\% of finding replacement APIs in Python, a score similar to that of state-of-the-art methods implemented in other languages.

### Project Structure
---
In the StackOverflowAPI folder, you can find relevant functions that helps to extract possible candidate replacement APIs form Stack Overflow in the <code>stack_replacement.py</code> file such as <code>getStackQuestionsV2</code>.

In the ReleaseNotes folder, you can find recommended heuristics that allows for extracting replacement APIs in <code>search_rst_files.py</code>.

In the CodeScrapping folder, the notebook <code>Parsing from code.ipynb</code> contains relevant functions that helps to extract the replacement APIs from the source code of general Python libraries such as Pandas and Numpy.