## MCQBOT

#### Description

MCQBOT is a simple practical project that I developed to demonstrate my proficiency in software engineering, with attention to modular design, version control, object-orientated programming (OOP), automated testing, continuous development and code quality. I also aim to showcase my skills in problem-solving, algorithm design, data and solution architecture. This project itself is a website that generates multiple-choice questions (MCQs) from a graph database, aiming to provide a template for people to produce tests quickly and easily. 

### Modular Design

As the project develops I will be ensuring a modular design. This means that the different technologies that make up the stack, such as front-end, the api, and databases logic will be seperate and independently tested. Modular and reusable pydantic models are also used.

### Object Orientated Programming

Individual modules will be composed of objects where possible to encapsulate the behaviour of different submodules and classes and objects as required.

### Version Control

The project itself is hosted on github and will adhere to a set of rules to ensure proper control over versioning. The main branch is protected, and any merges will require a pull request to be approved following review, as well as passing code audit and tests (see Automated testing)

### Automated Testing

Each time a pull request is made (and subsequently modified) a series of unit tests and integration tests will be run in a pytest suite via a github action/workflow. The first job is a code audit which performs a series of quality checks (see Code Quality) and if this succeeds it is followed by seperate tests for each module using the cached environment. The test-app job performs unit tests related to the internal app logic and the api. The test-neo4j job spins up a docker service for neo4j which tests for the graph database interface can connect to. Once all these jobs pass only then can the branch be merged into main.

### Code Quality

Code will be fully documented, commented where necessary, and all python language classes and functions that I have written are fully typed, ensuring that the code is both robust and easy to understand. Pydantic is also used where appropriate to provide data validation and type checking at runtime.

Every time a push is made to any branch, a number of checks run by various python packages listed below will be automatically run in a github action workflow.  The push will fail if there are any further changes or improvements suggested by these packages. This is a stringent measure to ensure that the only way code can make it into the project is if the code has been correctly formatted and reviewed locally.

* #### mypy
    A static type checker for Python that helps catch errors and bugs in code by verifying type annotations and detecting type-related issues at compile time.

* #### isort
    A utility that automatically sorts imports in code to make it more readable and consistent.

* #### blue
    A formatter that enforces PEP8 conventions, improving code readability and maintainability.

* #### pylint
    A static code analysis tool for Python that checks for programming errors, enforces coding standards, and provides suggestions for improving code quality and maintainability.


### Problem Solving and Algorithm Design

One of the problems I have been looking at is how to produce plausible fake words using a list of input words. A huge number of permutations are produced via generators for memory efficiency, which are benchmarked against existing words using levenstein word distance to maintain plausability.

### Data and Solution Architecture

At the moment there is a graph object used to represent the data, hopefully I will update this to have a graph database involved as well as another database to store information on test results. A lot more to come here as the project progresses.
I'm thinking python API / Front-end / Graph Database / SQL Database at the moment.
