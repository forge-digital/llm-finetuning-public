import pandas as pd
import neo4j
from neo4j import GraphDatabase
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path

URI = "neo4j://localhost"
AUTH = ("neo4j", "pleaseletmein")

def read_imdb_split(split_dir):
    split_dir = Path(split_dir)
    texts = []
    labels = []
    for label_dir in ["pos", "neg"]:
        for text_file in (split_dir/label_dir).iterdir():
            texts.append(text_file.read_text())
            labels.append(0 if label_dir is "neg" else 1)

    return texts, labels

def create_movie_graph_db():
    #movies_df = pd.read_csv('https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies.csv')
    #movies_df.to_csv("./neo4j/import/movies_with_info.csv", index=False)

    create_movies_db_query = """
    LOAD CSV WITH HEADERS FROM 
    'file:///movies_with_info.csv' AS row
    CALL {
        WITH row
        MERGE (m:Movie {id:row.movieId})
        SET m.released = date(row.released),
            m.title = row.title,
            m.imdbRating = toFloat(row.imdbRating),
            m.info = row.Movie_Info
        FOREACH (director in split(row.director, '|') | 
            MERGE (d:Person {name:trim(director)})
            MERGE (d)-[:DIRECTED]->(m))
        FOREACH (actor in split(row.actors, '|') | 
            MERGE (a:Person {name:trim(actor)})
            MERGE (a)-[:ACTED_IN]->(m))
        FOREACH (genre in split(row.genres, '|') | 
            MERGE (g:Genre {name:trim(genre)})
            MERGE (m)-[:IN_GENRE]->(g))
    } IN TRANSACTIONS OF 1000 ROWS;
    """

    with GraphDatabase.driver(URI, auth=AUTH) as driver:

        driver.execute_query(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (m:Movie) REQUIRE m.id IS UNIQUE;"
        )
        driver.execute_query("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;")
        driver.execute_query("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE;")
        driver.execute_query("CREATE CONSTRAINT IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE;")
        
        with driver.session(database="neo4j") as session:
            session.run(create_movies_db_query)


def query_db(query):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            result = session.run(query)
            return result.data()