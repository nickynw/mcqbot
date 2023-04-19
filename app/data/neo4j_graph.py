"""Object for acessing neo4j graph database"""
from collections import Counter
from typing import List, Union

from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship
from app.utils.log_util import create_logger, log_query
from neo4j import GraphDatabase

import pandas as pd

logger = create_logger(__name__)


class Neo4JGraph(MCQGraph):
    """
    This object forms an interface via neo4j python driver to the neo4j graph database.
    """

    def __init__(self, uri, user, password):
        super()
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        with self.driver.session() as session:
            session.run(
                'CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;'
            )
        logger.info(
            'New MCQGraph Object created - connection opened. Added constraint.'
        )

    def close(self):
        self.driver.close()
        logger.info('Neo4J Connection closed.')

    def delete_all(self):
        with self.driver.session() as session:
            query = """
                MATCH (node)
                DETACH DELETE node;
            """
            logger.debug(log_query(query))
            session.run(query)
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
            y for y in [self.has_name(x.name) for x in nodes] if y is not None
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
                logger.debug(log_query(query, props=node.dict()))
                session.run(query, props=node.dict())
            logger.info('Created %s nodes.', len(nodes))

    def create_relationships(self, relationships: List[MCQRelationship]):
        with self.driver.session() as session:
            try:
                for relationship in relationships:
                    query = (
                        """
                        MATCH (start:Entity {name: $start_node})
                        MATCH (end:Entity {name: $end_node})
                        CREATE (start)-[relationship:%s]->(end)
                        return relationship;
                    """
                        % relationship.type
                    )
                    logger.debug(log_query(query, **relationship.dict()))
                    success = bool(
                        session.run(query, **relationship.dict()).single()
                    )
                    if not success:
                        logger.warning(
                            'Failed to create relationship: %s',
                            str(relationship),
                            extra={'relationship': relationships},
                        )
                        raise ValueError(
                            'No relationships created due to failed relationships within input.'
                        )
            except Exception:
                session.rollback()  # roll back the transaction if an exception occurred
                raise
        logger.info(
            'Created %s relationships in the database.', len(relationships)
        )

    def has_name(self, name: str) -> Union[MCQNode, None]:
        with self.driver.session() as session:
            query = """
                MATCH (node:Entity {name: $name})
                RETURN node;
            """
            logger.debug(log_query(query=query, params={'name': name}))
            result = session.run(query, name=name)
            record = result.single()
            if record:
                return MCQNode(**dict(record['node'].items()))
        return None

    def has_relationship(self, relationship: MCQRelationship) -> bool:
        with self.driver.session() as session:
            query = (
                """
                MATCH (start_node:Entity {name: $start_node})-[r:%s]-(end_node:Entity {name: $end_node})
                RETURN r
            """
                % relationship.type
            )
            logger.debug(log_query(query, **relationship.dict()))
            result = session.run(query, **relationship.dict())
            return bool(result.single())

    def similarity_matrix(self, relationship: MCQRelationship):
        graph_projection = 'graph_projection'
        end_node = relationship.end_node
        with self.driver.session() as session:
            query_drop_graph = """
                WITH $graph_projection AS graphName
                CALL gds.graph.exists(graphName) YIELD exists
                WITH graphName, exists
                WHERE exists = true
                CALL gds.graph.drop(graphName) YIELD graphName AS droppedGraphName
                RETURN droppedGraphName
            """
            logger.debug(
                log_query(
                    query=query_drop_graph, graph_projection=graph_projection
                )
            )
            session.run(query_drop_graph, graph_projection=graph_projection)
            query_build_graph = """
                MATCH (a:Entity {name:$end_node})--(target:Entity)-[*1..2]-(source:Entity)
                WITH gds.alpha.graph.project($graph_projection, source, target) AS g
                RETURN g.graphName AS graph, g.nodeCount AS nodes, g.relationshipCount AS rels
            """
            result = session.run(
                query_build_graph,
                graph_projection=graph_projection,
                end_node=end_node,
            )
            logger.debug(
                log_query(
                    query=query_build_graph,
                    end_node=end_node,
                    graph_projection=graph_projection,
                )
            )
            query_similarity = """
                CALL gds.nodeSimilarity.stream($graph_projection)
                YIELD node1, node2, similarity
                RETURN gds.util.asNode(node1).name AS Node1, gds.util.asNode(node2).name AS Node2, similarity
                ORDER BY similarity DESCENDING, Node1, Node2
            """
            logger.debug(
                log_query(
                    query=query_similarity,
                    graph_projection=graph_projection,
                )
            )
            result = session.run(
                query_similarity, graph_projection=graph_projection
            )
            return pd.DataFrame([record.data() for record in result])
