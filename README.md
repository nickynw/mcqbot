## MCQBOT

MCQBOT is a simple practical project that I developed to demonstrate my proficiency in software engineering, with attention to modular design, containerisation, version control, object-orientated programming, automated testing, continuous development and code quality. (Explained in depth below) I also aim to showcase my skills in problem-solving, algorithm design, data and solution architecture. This project itself is a website that generates multiple-choice questions (MCQs) from a graph database, aiming to provide a template for people to produce tests quickly and easily. 

To see this API being used in a basic website to generate real multiple choice questions, please follow this [link](https://main.d1vo05ddg5t68j.amplifyapp.com) (Hosted on AWS Amplify)

For a guide on getting this running yourself, scroll to the bottom of this readme file.

### Modular Design

As the project develops I will be ensuring a modular design. This means that the different technologies that make up the stack, such as front-end, the api, and databases logic will be seperate and independently tested. Pydantic is also utilised for defining data schemas that are shared between different modules.
This means that for each service there are independent commands to run them, and independent ways to install only the required packages for that service, or alternatively methods to run and install everything at once.

### Containerisation / Dockerisation

Dockerfiles are used in this project. Docker compose can be run to spin up an environment to run all tests for the entire app, however for now these are run in the github action/workflow environment. A docker compose file is now used to spin up and run a Neo4J graph database service to be able to run any tests that require Neo4j. This can also be run locally as well.

### Object Orientated Programming

Individual modules will be composed of objects where possible to encapsulate the behaviour of different submodules and classes and objects as required. As an example see the MCQGraph / Neo4JGraph / NXGraph as an example of inheritance in this project.

### Version Control

The project itself is hosted on github and will adhere to a set of rules to ensure proper control over versioning. The main branch is protected, and any merges will require a pull request to be approved following review, as well as passing code audit and tests (see Automated testing)

### Automated Testing

Each time a pull request is made (and subsequently modified) a series of unit tests and integration tests will be run in a pytest suite via a github action/workflow. The first job is a code audit which performs a series of quality checks (see Code Quality) and if this succeeds it is followed by seperate tests for each module using the cached environment. The test-app job performs unit tests related to the internal app logic and the api. The test-neo4j job spins up a docker service for neo4j which tests for the graph database interface can connect to. This is followed up by a job to clean up the caches on success. Once all these jobs pass only then can the branch be merged into main.

### Code Quality

Code will be fully documented, commented where necessary, and all python language classes and functions that I have written are fully typed, ensuring that the code is both robust and easy to understand. Pydantic is also used where appropriate to provide data validation and type checking at runtime.
Poetry is used for dependency management and package organisation. The core required packages are provided, alongside different groups of packages required depending on production/development and which services are going to be run.

Every time a push is made to any branch, a number of checks run by various python packages listed below will be automatically run in a github action workflow.  The push will fail if there are any further changes or improvements suggested by these packages. This is a stringent measure to ensure that the only way code can make it into the project is if the code has been correctly formatted and reviewed locally.

* #### mypy
    A static type checker for Python that helps catch errors and bugs in code by verifying type annotations and detecting type-related issues at compile time. (Uses the mypy.ini file for configuration)

* #### isort
    A utility that automatically sorts imports in code to make it more readable and consistent.

* #### blue
    A formatter that enforces PEP8 conventions, improving code readability and maintainability.

* #### pylint
    A static code analysis tool for Python that checks for programming errors, enforces coding standards, and provides suggestions for improving code quality and maintainability. (Uses the .pylintrc file for configuration)


### Problem Solving and Algorithm Design

One of the problems I have been looking at is how to produce plausible fake words using a list of input words. A huge number of permutations of word mixtures are produced via generators for memory efficiency, which are benchmarked against existing words using 'levenstein' word distance, so any fake words created from mixing existing words must 'resemble' an existing term to a certain extent to be utilised.

Another core feature of this app is that distractor choices in the quiz must be similar enough without being a correct answer. This is achieved by creating a 'similarity matrix' from existing algorithms that uses the similarities of relationships between nodes to determine a similarity score. Nodes within a certain distance of the answer node are then benchmarked and utilised based on this score.

### Data and Solution Architecture

At the moment there are two options for data storage when running locally:

- NX (Networkx) - A variable is used to store the graph database as an object locally (Should not be used on large datasets).
- Neo4j - A graph database that requires an instance to be running.


These are connected to a Fast API Application. In production I only use the Networkx local graph database because it is expensive to run a Neo4J instance and this is literally just a hobby project. There is a basic frontend for this application using React / Typescript / semantic react ui to demonstrate that the API is working in production, I have not made the code public for this as it is out of the scope of this project.

## How to run this yourself:

To run and test locally you can spin up three containers using Docker which will run a neo4j instance (If Neo4J is installed and running), the API itself (which you will be able to visit on https://localhost:8000) and also the entire test suite. First you will need to create your own .env file at the highest project level with the following variables, changing defaults where necessary:
- `NEO4J_URI=bolt://localhost:7687`
- `NEO4J_USERNAME=neo4j`
- `NEO4J_PASSWORD={set your password here}`
- `COMPOSE_PROJECT_NAME=mcqbot`

Then you can use the following command to create an image and run each container:
- `docker-compose -f docker/docker-compose.dev.yml --env-file .env up`

If you want to run locally on your machine without Docker you will need to set up the environment with python 3.9 installed to do so. First make sure you have poetry set up, then install necessary packages to run each service. If you wish to only work with networkx graph db without installing and running neo4j, you can remove the neo4j from the --with flag.
- `pip install poetry==1.4.2`
- `poetry run install --with nx,neo4j,code_audit`

To run the api, which should become available on https://localhost:8000:
- `uvicorn app.main:app --reload --port 8000`

To run tests you can run the following to test the core code / networkx db / neo4j db / etc.:
- `poetry run pytest tests/test_app/.`
- `poetry run pytest tests/test_nx/.`
- `poetry run pytest tests/test_neo4j/.`

If there are any issues feel free to contact me.
