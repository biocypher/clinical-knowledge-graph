#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BioCypher - CKG prototype
"""

import neo4j_utils as nu
from biocypher._logger import logger

logger.debug(f"Loading module {__name__}.")


class CKGAdapter:
    def __init__(
        self,
        dirname: str = None,
        biocypher_driver = None,
        id_batch_size: int = int(1e6),
        limit_import_count: int = 0,
        node_file: str = "data/all_nodes.csv",
        edge_file: str = "data/all_granular_relationships.csv",
    ):

        self.biocypher_driver = biocypher_driver
        self.id_batch_size = id_batch_size
        self.limit_import_count = limit_import_count
        self.output_dir = dirname
        self.node_file = node_file
        self.edge_file = edge_file

        # read driver
        self.driver = nu.Driver(
            db_name="neo4j",
            db_uri="bolt://localhost:7687",
            db_user="neo4j",
            db_passwd="your_password_here",
            multi_db=False,
            max_connection_lifetime=7200,
        )

    def write_nodes(self):
        """
        Write nodes to admin import csv files.
        """

        # get node labels from csv
        with open(self.node_file, "r") as f:
            node_labels = f.read().splitlines()

        # node_labels = ["Disease", "Tissue"]

        for label in node_labels:

            with self.driver.session() as session:
                # writing of one type needs to be completed inside
                # this session
                session.read_transaction(
                    self._get_node_ids_and_write_batches_tx, label
                )

    def write_edges(self) -> None:
        """
        Write edges to admin import csv files.
        """

        # get node labels from csv
        with open(self.edge_file, "r") as f:
            rel_labels = f.read().splitlines()

        rel_labels = rel_labels[1:]
        rel_labels = [label.split(",") for label in rel_labels]

        # rel_labels = [
        #     ("Clinically_relevant_variant", "ASSOCIATED_WITH", "Disease"),
        #     ("Protein", "MENTIONED_IN_PUBLICATION", "Publication"),
        #     ("Tissue", "MENTIONED_IN_PUBLICATION", "Publication"),
        # ]
        # rel_labels = []

        for src, typ, tar in rel_labels:

            concat = f"{typ}_{src}_{tar}"

            # skip some types
            if typ in [
                "VARIANT_FOUND_IN_CHROMOSOME",
                "LOCATED_IN",
                "HAS_STRUCTURE",
                "IS_SUBSTRATE_OF",
                "IS_QCMARKER_IN_TISSUE",
                "VARIANT_IS_CLINICALLY_RELEVANT",
                "IS_A_KNOWN_VARIANT",
            ]:
                continue

            with self.driver.session() as session:
                # writing of one type needs to be completed inside
                # this session
                session.read_transaction(
                    self._get_rel_ids_and_write_batches_tx,
                    src,
                    typ,
                    tar,
                )

    def _get_node_ids_and_write_batches_tx(
        self,
        tx,
        label,
    ):
        """
        Write nodes to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        query = f"MATCH (n:{label}) RETURN id(n) as id"

        if self.limit_import_count > 0:
            query += f" LIMIT {self.limit_import_count}"

        result = tx.run(query)

        id_batch = []
        for record in result:
            # collect in batches
            id_batch.append(record["id"])
            if len(id_batch) == self.id_batch_size:

                # if full batch, trigger write process
                self._write_nodes(id_batch, label)
                id_batch = []

            # check if result depleted
            elif result.peek() is None:

                # write last batch
                self._write_nodes(id_batch, label)

    def _get_rel_ids_and_write_batches_tx(
        self,
        tx,
        src,
        typ,
        tar,
    ):
        """
        Write edges to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        query = f"MATCH (n:{src})-[r:{typ}]->(m:{tar}) RETURN id(r) as id"

        if self.limit_import_count > 0:
            query += f" LIMIT {self.limit_import_count}"

        result = tx.run(query)

        id_batch = []
        for record in result:
            # collect in batches
            if len(id_batch) < self.id_batch_size:
                id_batch.append(record["id"])

                # check if result depleted
                if result.peek() is None:
                    # write last batch
                    self._write_edges(id_batch, src, typ, tar)

            # if full batch, trigger write process
            else:
                self._write_edges(id_batch, src, typ, tar)
                id_batch = []

    def _write_nodes(self, id_batch, label):
        """
        Write edges to admin import csv files. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of edge ids to write

            label: label of the node type
        """

        def node_gen():
            with self.driver.session() as session:
                results = session.read_transaction(get_nodes_tx, id_batch)

                for res in results:

                    _id = _process_node_id(res["n"]["id"], label)
                    _type = label
                    _props = res["n"]

                    # add strict mode properties
                    if not _props.get("source"):
                        _props["source"] = "CKG"
                    if not _props.get("version"):
                        _props["version"] = "v3"
                    _props["licence"] = "None"

                    yield (_id, _type, _props)

        self.biocypher_driver.write_nodes(
            nodes=node_gen(),
        )

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

        def edge_gen():
            with self.driver.session() as session:
                results = session.read_transaction(get_rels_tx, id_batch)

                for res in results:

                    # extract relevant id
                    _src = _process_node_id(res["n"]["id"], src)
                    _tar = _process_node_id(res["m"]["id"], tar)

                    # split some relationship types
                    _type = self._split_type(typ, src, tar)
                    _props = {}

                    # add properties
                    if typ in [
                        "ACTS_ON",
                        "COMPILED_INTERACTS_WITH",
                        "CURATED_INTERACTS_WITH",
                    ]:
                        _props = {"type": typ}
                    elif typ == "IS_BIOMARKER_OF_DISEASE":
                        # TODO decide on granularity of multiple relationships
                        # between nodes: do we want multiple age ranges?
                        # TODO also for other types of relationships
                        _props = res["PROPERTIES(r)"]

                    # add strict mode properties
                    if not _props.get("source"):
                        _props["source"] = "CKG"
                    if not _props.get("version"):
                        _props["version"] = "v3"
                    _props["licence"] = "None"

                    yield (_src, _tar, _type, _props)

        self.biocypher_driver.write_edges(
            edges=edge_gen(),
        )

    def _split_type(self, typ, src, tar):
        if typ in [
                    "MENTIONED_IN_PUBLICATION",
                    "ASSOCIATED_WITH",
                    "ANNOTATED_IN_PATHWAY",
                    "MAPS_TO",
                    "VARIANT_FOUND_IN_GENE",
                    "TRANSLATED_INTO",
                    "HAS_MODIFIED_SITE",
                ]:
            _type = "_".join([typ, src, tar])
        else:
            _type = typ
        return _type


def get_nodes_tx(tx, ids):
    result = tx.run(
        "MATCH (n) " "WHERE id(n) IN $ids " "RETURN n",
        ids=ids,
    )
    return result.data()


def get_rels_tx(tx, ids):
    result = tx.run(
        "MATCH (n)-[r]->(m) "
        "WHERE id(r) IN $ids "
        "RETURN n, PROPERTIES(r), m",
        ids=ids,
    )
    return result.data()


def _process_node_id(_id, _type):
    """
    Add prefixes to avoid multiple assignment.
    """
    if _type == "Food":
        _id = "foodb:" + _id
    elif _type == "Chromosome":
        _id = "chr:" + _id
    elif _type == "Complex":
        _id = "corum:" + _id
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
    elif _type == "Gene":
        _id = "hgnc.symbol:" + _id
    elif _type == "Analytical_sample":
        _id = "sample:" + _id

    return _id
