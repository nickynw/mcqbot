## MCQBOT

#### Description

MCQBOT is a simple practical project that I developed to demonstrate my proficiency in software engineering, with attention to modular design, version control, OOP, automated testing, continuous development and code quality. This project is a website that generates multiple-choice questions (MCQs) from a graph database, making it useful template for educators, trainers, or anyone who needs to create quizzes quickly. This project showcases my skills in problem-solving, algorithm design, programming, and software development methodologies."

### Modular Design

As the project develops I will be ensuring a modular design. This means that the different technologies that make up the stack, such as front-end, the api, and databases logic will be seperate and independently tested.

### Object Orientated Programming

Individual modules will be composed of objects where possible to encapsulate the behaviour of different submodules and classes and objects as required.

### Version Control

The project itself is hosted on github and will adhere to a set of rules to ensure proper control over versioning. The main branch is protected, and any merges will require a pull request to be approved with code review.

### Automated Testing

Each time a push is made to a branch a series of tests will be run in a pytest suite via a github action/workflow. On top of this, whenever a pull request opened a docker container will be spun up to run the tests again in a docker environment based on the production environment, and can only succeed if these tests pass.

### Code Quality

Code will be fully documented, commented where necessary, and all python language classes and functions that I have written are fully typed, ensuring that the code is both robust and easy to understand.

Every time a push is made to any branch, a number of checks will be automatically run using python packages mypy, blue, isort, and pylint. This will perform a series of checks on imports, static typing, overall code formatting and linting and will cause the push to fail if there are any improvements available. This is a stringent measure to ensure that the only way code can make it into the project is if the code has been correctly formatted and reviewed locally.