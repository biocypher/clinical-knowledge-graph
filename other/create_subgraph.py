import neo4j_utils as nu

driver = nu.Driver(
    db_name="neo4j",
    db_uri="bolt://localhost:7687",
    db_user="neo4j",
    db_passwd="your_password_here",
    multi_db=False,
)

# trim graph to include max number of edges for each pattern


def get_labels():
    with open("data/granular_relationships.txt", "r") as f:
        node_labels = f.read().splitlines()

    node_labels = node_labels[1:]
    node_labels = [label.split(",") for label in node_labels]
    return node_labels


def trim_rels() -> None:
    max_patterns_remaining = 100000

    node_labels = get_labels()

    for src, rel, tar in node_labels:
        print(src, rel, tar)

        res, sum = driver.query(
            f"MATCH p=(n:{src})-[r:{rel}]->(m:{tar}) RETURN count(p)"
        )

        n = res[0]["count(p)"]
        print(n)

        if n > max_patterns_remaining:
            # delete all patterns with more than max_patterns_remaining
            res, sum = driver.query(
                "call apoc.periodic.iterate('"
                f"MATCH (n:{src})-[r:{rel}]->(m:{tar}) "
                f"RETURN id(r) AS id LIMIT {n - max_patterns_remaining}', '"
                "MATCH ()-[r]->() WHERE id(r) = id DELETE r', {batchSize: 10000}) "
                "YIELD batches, total RETURN batches, total"
            )
            print(res)


def trim_orphans() -> None:
    max_nodes_remaining = 0

    labels = get_labels()
    labels = [[label[0], label[2]] for label in labels]
    # flatten list of lists to list of values
    labels = [label for sublist in labels for label in sublist]
    # remove duplicates
    labels = list(set(labels))

    for label in labels:
        res, sum = driver.query(
            f"MATCH (n:{label}) " "WHERE NOT (n)--() " "RETURN count(n)"
        )

        n = res[0]["count(n)"]
        print(f"{label}: {n}")

        res, sum = driver.query(
            "call apoc.periodic.iterate('"
            "MATCH (n) WHERE NOT (n)--() "
            f"RETURN id(n) AS id LIMIT {n - max_nodes_remaining}', '"
            "MATCH (n) WHERE id(n) = id DELETE n', {batchSize: 10000}) "
            "YIELD batches, total RETURN batches, total"
        )
        print(res)


if __name__ == "__main__":
    trim_rels()
    trim_orphans()
