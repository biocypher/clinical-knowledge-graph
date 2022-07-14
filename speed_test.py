import biocypher
import neo4j_utils as nu

from biocypher._logger import logger

logger.debug(f"Loading module {__name__}.")


class SpeedTest:
    def __init__(self) -> None:

        # write driver
        self.bcy = biocypher.Driver(
            offline=True,  # set offline to true,
            # connect to running DB for input data via the neo4j driver
            user_schema_config_path="config/schema_config.yaml",
            delimiter="¦",
        )
        # start writer, takes a while
        self.bcy.start_batch_writer(dirname="speed_test", db_name="neo4j")
        self.bcy.start_bl_adapter()

        # read driver
        self.driver = nu.Driver(
            db_name="neo4j",
            db_uri="bolt://localhost:7687",
            db_user="neo4j",
            db_passwd="your_password_here",
            multi_db=False,
        )

    def get_rel_ids_tx(self, tx, src, typ, tar, id_batch_size: int = 10000):
        result = tx.run(
            f"MATCH (n:{src})-[r:{typ}]->(m:{tar}) "
            "RETURN id(r) as id LIMIT 2000000"
        )

        id_batch = []
        for record in result:
            # collect in batches
            if len(id_batch) < id_batch_size:
                id_batch.append(record["id"])
            # if full batch, trigger write process
            else:
                self._write_edges(id_batch, src, typ, tar)
                id_batch = []

    def get_rels_tx(self, tx, ids):
        result = tx.run(
            "MATCH (n)-[r]->(m) "
            "WHERE id(r) IN {ids} "
            "RETURN n, PROPERTIES(r), m",
            ids=ids,
        )
        return result.data()

    def _write_edges(self, id_batch, src, typ, tar):
        """
        Write edges to admin import csv files. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of edge ids to write

            src: source node label

            typ: relationship type

            tar: target node label
        """

        with self.driver.session() as session:
            rels = session.read_transaction(self.get_rels_tx, id_batch)

            edges = []
            for rel in rels:

                # extract relevant id
                _src = _process_node_id(rel["n"]["id"], src)
                _tar = _process_node_id(rel["m"]["id"], tar)

                # split relationship types
                _type = "_".join([typ, src, tar])
                _props = {}
                edges.append((_src, _tar, _type, _props))

            self.bcy.write_edges(
                edges,
                "neo4j",
            )

    def write_edges(
        self,
        id_batch_size: int = 10000,
    ) -> None:
        """
        Write edges to admin import csv files.

        Args:
            id_batch_size: number of edges to write per batch
        """

        with self.driver.session() as session:
            session.read_transaction(
                self.get_rel_ids_tx,
                "Tissue",
                "MENTIONED_IN_PUBLICATION",
                "Publication",
                id_batch_size,
            )


def _process_node_id(_id, _type):
    """
    Add prefixes to avoid multiple assignment.
    """
    if _type == "Food":
        _id = "FooDB:" + _id
    elif _type == "Chromosome":
        _id = "chr:" + _id
    elif _type == "Complex":
        _id = "CORUM:" + _id
    elif _type == "Timepoint":
        _id = "timepoint:" + _id
    elif _type == "Amino_acid_sequence":
        _id = "aas:" + _id
    elif _type == "Clinical_variable":
        _id = "snomedct:" + _id
    elif _type == "Publication":
        _id = "pmid:" + _id
    elif _type == "Somatic_mutation":
        _id = "somatic:" + _id
    elif _type == "Protein":
        _id = "uniprot:" + _id

    return _id
