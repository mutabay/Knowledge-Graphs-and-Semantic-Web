"""
Neo4j Property Graph Loader for Movies

Neo4j uses a property graph model where:
- Nodes have labels and properties
- Relationships have types and properties
- Everything is stored as graph structures optimized for traversal
"""

from neo4j import GraphDatabase
import pandas as pd
from typing import Dict, List, Optional, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MovieNeo4jLoader:
    """
    Loads movie data into Neo4j property graph database.

    Key Concepts:
    - Node: An entity (Movie, Director, Genre)
    - Relationship: A connection between nodes (DIRECTED, HAS_GENRE)
    - Property: Attributes stored on nodes/relationships
    - Label: Type/category of a node
    """

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        """
        Initialize connection to Neo4j database.

        Make sure Neo4j is running! Start it with Docker:
        docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
        """