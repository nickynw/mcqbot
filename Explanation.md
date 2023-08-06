# MCQBOT Explained

Follow this [link](https://main.d1vo05ddg5t68j.amplifyapp.com) (Hosted on AWS Amplify) to see this API in action on a basic website. For in depth explanation for the listed concepts or [for a guide to run it yourself](https://github.com/nickynw/mcqbot/tree/main#how-to-run-this-yourself) see the README file.

MCQBOT is a simple practical project developed with attention to the following concepts:
- Modular design, through architecture and design.
- Containerisation, with Docker
- Object-orientated programming
- Automated testing (Unit and Integration Tests) and CI/CD, via Github Actions and Pytest, and version control with branch protections and pull request conventions.
- Code quality, using package management, PEP-8 conventions, code linting and cleaning (blue, mypy, isort, pylint, pydantic)

This project is a site that generates multiple-choice questions (MCQs) from a graph database. Question data is stored as nodes in a graph, fake distractor choices are chosen from nodes that pass a similarity threshold based on their distance in the graph from the real answer. Fake words are also generated from the full distractor list and inserted as an option.

<img src="/images/example_2.png" alt="example screenshot" width="400"/>


## Solution Architecture

- Another repo contains the react front-end TSX code, deployed via AWS Amplify which redeploys automatically when detecting changes to the main branch on github.

- This repo contains the code for the back-end python fastapi app, serving a single endpoint to randomly generate multiple choice questions. The api is hosted on a Google Cloud Run instance which deploys with an image of the application stored in the Google Artifact Registry service.

- Infrastructure is in place for Neo4J database to be used, with tests, however I am not hosting a graph database in 'production' for cost reasons. At the moment a networkx object is stored in local memory instead for free.

<img src="/images/solution.png" alt="solution diagram" width="650"/>

### Automated Testing and CI/CD

- Each time a pull request is made for a new feature, improvement or refactor, it cannot be merged until a series of tests are run successfully in Github Actions.
- Code audit stage check code quality, errors or improvements that can be made.
- Tests are run to check the main app core logic works with dummy data and fixed random seeds.
- Seperate tests are run to check both Neo4J (with a temporary instance/service created using a docker image) and networkx graph database connections.
- Clean up caches which are used to speed up environment creation for each test.

<img src="/images/automation.png" alt="automation diagram" width="650"/>

## Backend Overview

- Pydantic 'MCQ' Object is provided as a json response by the endpoint made available via the main app.
- This is built using MCQ Builder Class which generates answers, choices and topic using the MCQGraph and FakeWordBuilder class.
- MCQGraph is an interface for graph databses, which is a template for specific NXGraph and Neo4JGraph interface classes, providing specific required functions for interacting with the graphs.
- FakeWordBuilder uses generators to build plausible fake word combinations using pyphen and levenstein packages.

<img src="/images/objects.png" alt="objects diagram" width="650"/>

## In-Depth Process Explanation

- In this example we select a random edge, "Which of these is a Greeting Term" is the question, "Hello" is the answer.
- Connected nodes 'Greetings' and 'Hola' are ruled out as possible distractors.
- Nearby related nodes are selected as potential distractors, depending on their similarity in a similarity matrix.
- Fake words are also accepted as a potential distractor, each permutation is accepted or rejected depending on word validity and 'levenstein distance' from existing words, too similar or too distant are rejected.

<img src="/images/association_dag.png" alt="association dag diagram" width="650"/>