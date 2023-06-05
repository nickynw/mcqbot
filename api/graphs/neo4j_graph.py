"""Object for acessing neo4j graph database"""
import random
from collections import Counter
from typing import Any, Callable, Dict, List, Optional, Union

from api.graphs.mcq_graph import MCQGraph
from api.models import MCQNode, MCQRelationship
from api.utils.log_util import create_logger
from neo4j import GraphDatabase, Result, Session

logger = create_logger(__name__)


def log(func: Callable[..., Any]):
    """
    A wrapper that logs the query sent to Neo4j via the driver as logging is not included in the free version.

    Args:
        func (Callable[..., Any]): session run function
    """

    def log_wrapper(
        session: Session, query: str, **kwargs: Dict[str, Any]
    ) -> Callable:
        """
        Logs message at debug level of the query with params and variables replaced as it would be sent to the driver.

        Args:
            session (Session): session to which the query is sent
            query (str): original query string
        """
        output = query[:]
        for arg_name, arg_value in kwargs.items():
            output = output.replace(f'${arg_name}', "'" + str(arg_value) + "'")
        logger.debug(output)
        return func(session, query, **kwargs)

    return log_wrapper


@log
def run(session: Session, query: str, **params: Dict[str, Any]) -> Result:
    """
    Run a query through the python driver neo4j session

    Args:
        session (Session): Session instance
        query (str): query string

    Returns:
        Result: the result of the cypher query run via the driver in the neo4j session
    """
    return session.run(query, params)


class Neo4JGraph(MCQGraph):
    """
    This object forms an interface via neo4j python driver to the neo4j graph database.
    """

    def __init__(self, uri, user, password):
        super()
        self.driver = self.create_driver(uri, user, password)
        with self.driver.session() as session:
            run(
                session,
                query='CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;',
            )

    def close(self):
        self.driver.close()
        logger.info('Neo4J Connection closed.')

    def create_driver(self, uri, user, password):
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as session:
                result = session.run('RETURN 1')
                record = result.single()
                logger.info(
                    'Successfully created driver for connection %s' % uri
                )
                if record[0] == 1:
                    return driver
        except Exception as e:
            logger.info('Unable to create neo4j connection: %s' % e.args[0])
            raise e

    def delete_all(self):
        with self.driver.session() as session:
            query = """
                MATCH (node)
                DETACH DELETE node;
            """
            run(session=session, query=query)
            logger.info('All nodes removed from graph database.')

    def create_nodes(self, nodes: List[MCQNode]):
        # Check for duplicates within the input
        counter = Counter([x.name for x in nodes])
        duplicates = [x for x in nodes if counter[x.name] > 1]
        if duplicates:
            logger.error(
                'Duplicate name inputs detected: %s',
                {x.name for x in nodes},
                extra={'nodes': duplicates},
            )
            raise ValueError(
                f'Duplication Error: {len(duplicates)} node duplicates within input.'
            )

        # Check for duplicates within the database
        matches = [
            y for y in [self.get_node(x.name) for x in nodes] if y is not None
        ]
        if matches:
            logger.error(
                'Nodes already exist with these names: %s',
                {x.name for x in matches},
                extra={'nodes': matches},
            )
            raise ValueError(
                f'Duplication Error: {len(matches)} nodes already have names in database.'
            )

        # Create nodes in session batches
        query = 'CREATE (:Entity $props);'
        with self.driver.session() as session:
            for node in nodes:
                session.run(query, props=node.dict())
            logger.info('Created %s nodes.', len(nodes))

    def create_relationships(self, relationships: List[MCQRelationship]):
        with self.driver.session() as session:
            for relationship in relationships:
                query = (
                    """
                    MATCH (answer_node:Entity {name: $answer_node})
                    MATCH (topic_node:Entity {name: $topic_node})
                    CREATE (answer_node)-[relationship:%s]->(topic_node)
                    return relationship;
                """
                    % relationship.type
                )
                # log_query(logger, query, **relationship.dict())
                success = bool(
                    session.run(query, **relationship.dict()).single()
                )
                if not success:
                    logger.warning(
                        'Failed to create relationship: %s',
                        str(relationship),
                        extra={'relationship': relationships},
                    )
        logger.info(
            'Created %s relationships in the database.', len(relationships)
        )

    def get_node(self, name: str) -> Union[MCQNode, None]:
        with self.driver.session() as session:
            query = """
                MATCH (node:Entity {name: $name})
                RETURN node;
            """
            result = session.run(query, name=name)
            record = result.single()
            if record:
                return MCQNode(**dict(record['node'].items()))
        return None

    def has_relationship(self, relationship: MCQRelationship) -> bool:
        with self.driver.session() as session:
            query = (
                """
                MATCH (answer_node:Entity {name: $answer_node})-[r:%s]->(topic_node:Entity {name: $topic_node})
                RETURN r
            """
                % relationship.type
            )
            result = run(session, query, **relationship.dict())
            return bool(result.single())

    def random_relationship(
        self, seed: Optional[int] = None
    ) -> MCQRelationship:
        with self.driver.session() as session:
            query_count = """
            MATCH ()-[relationship]->()
            RETURN COUNT(relationship) AS num_rels
            """
            num_rels = session.run(query_count).single()['num_rels']
            if num_rels < 1:
                raise ValueError('Empty Database.')
            random.seed(seed)
            random_index = random.randint(1, num_rels)
            query = """
                MATCH (answer_node)-[relationship]->(topic_node)
                RETURN answer_node, relationship, topic_node
                ORDER BY answer_node.name
                SKIP $n - 1
                LIMIT 1
            """
            result = run(session, query, n=random_index).single()
            relationship = MCQRelationship(
                answer_node=result['answer_node']['name'],
                topic_node=result['topic_node']['name'],
                type=result['relationship'].type,
            )
            return relationship

    def related_nodes(self, relationship: MCQRelationship) -> List[MCQNode]:
        with self.driver.session() as session:
            query = """
            MATCH (answer_node:Entity {name: $answer_node})-[r:%s]->(b:Entity {name: $topic_node})<-[r2:%s]-(related_node:Entity)
            RETURN related_node
            """ % (
                relationship.type,
                relationship.type,
            )
            result = run(
                session,
                query,
                topic_node=relationship.topic_node,
                answer_node=relationship.answer_node,
            )
            nodes = [
                MCQNode(**dict(record['related_node'].items()))
                for record in result
            ]
            return nodes

    def connected_nodes(self, node: MCQNode) -> List[MCQNode]:
        with self.driver.session() as session:
            query = """
                MATCH (node:Entity {name: $node})--(connected_node:Entity)
                RETURN COLLECT(DISTINCT connected_node) AS connected_nodes
            """
            result = run(session, query, node=node.name)
            nodes = [
                MCQNode(**dict(x.items()))
                for x in result.single()['connected_nodes']
            ]
            return nodes

    def similarity_matrix(self, node: MCQNode) -> Dict[str, float]:
        graph_projection = 'graph_projection'
        with self.driver.session() as session:
            query_drop_graph = """
                WITH $graph_projection AS graphName
                CALL gds.graph.exists(graphName) YIELD exists
                WITH graphName, exists
                WHERE exists = true
                CALL gds.graph.drop(graphName) YIELD graphName AS droppedGraphName
                RETURN droppedGraphName
            """
            run(
                session=session,
                query=query_drop_graph,
                graph_projection=graph_projection,
            )
            query_build_graph = """
                CALL gds.graph.project(
                    $graph_projection,
                    '*',
                    '*'
                );
            """
            run(
                session,
                query_build_graph,
                graph_projection=graph_projection,
            )
            query_similarity = """
                MATCH (n:Entity) where n.name = $node
                CALL gds.alpha.nodeSimilarity.filtered.stream($graph_projection, {sourceNodeFilter: n, topK: 20})
                YIELD node1, node2, similarity
                RETURN gds.util.asNode(node2).name AS key, similarity AS value
                ORDER BY similarity DESCENDING, key
            """
            result = run(
                session,
                query_similarity,
                graph_projection=graph_projection,
                node=node.name,
            )
            return {x['key']: x['value'] for x in result}
