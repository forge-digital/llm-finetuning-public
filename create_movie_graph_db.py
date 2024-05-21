from neo4j import GraphDatabase
from utils import AUTH, URI

print("Creating movie graph database...")
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

print("DONE!")