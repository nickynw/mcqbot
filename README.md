## MCQBOT

#### Description

MCQBOT is a simple practical project that I developed to demonstrate my proficiency in software engineering, with attention to modular design, version control, OOP, automated testing, continuous development and code quality. This project is a website that generates multiple-choice questions (MCQs) from a graph database, making it useful template for educators, trainers, or anyone who needs to create quizzes quickly. This project showcases my skills in problem-solving, algorithm design, programming, and software development methodologies."

### Modular Design

As the project develops I will be ensuring a modular design. This means that the different technologies that make up the stack, such as front-end, the api, and databases logic will be seperate and independently tested.

### Object Orientated Programming

Individual modules will be composed of objects where possible to encapsulate the behaviour of different submodules and classes and objects as required.

### Version Control

The project itself is hosted on github and will adhere to a set of rules to ensure proper control over versioning. The main branch is protected, and any merges will require a pull request to be approved following review, as well as passing code audit and tests (see Automated testing)

### Automated Testing

Each time a push is made to a branch a series of tests will be run in a pytest suite via a github action/workflow. On top of this, whenever a pull request is opened, a docker container will be spun up to run the tests in a docker environment based on the production environment, and the merge will only be able to proceed if these tests pass.

### Code Quality

Code will be fully documented, commented where necessary, and all python language classes and functions that I have written are fully typed, ensuring that the code is both robust and easy to understand.

Every time a push is made to any branch, a number of checks run by various python packages listed below will be automatically run in a github action workflow.  The push will fail if there are any further changes or improvements suggested by these packages. This is a stringent measure to ensure that the only way code can make it into the project is if the code has been correctly formatted and reviewed locally.

#### mypy
A static type checker for Python that helps catch errors and bugs in code by verifying type annotations and detecting type-related issues at compile time.

#### isort
A utility that automatically sorts imports in code to make it more readable and consistent.

#### blue
A formatter that enforces PEP8 conventions, improving code readability and maintainability.

#### pylint
A static code analysis tool for Python that checks for programming errors, enforces coding standards, and provides suggestions for improving code quality and maintainability.