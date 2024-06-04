#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
gosu neo4j:neo4j mkdir -p /var/lib/neo4j/data/transactions
gosu neo4j:neo4j mkdir -p /var/lib/neo4j/data/databases/graph.db
cmd="neo4j"
export cmd
# do not run init script at each container start but only at the first start
if [ ! -f /var/lib/neo4j/data/neo4j-import-done.flag ]; then
    gosu neo4j:neo4j neo4j-admin load --from=/backups/graph.db/ckg_latest_4.2.3.dump --database=graph.db --force --verbose
    gosu neo4j:neo4j touch /var/lib/neo4j/data/neo4j-import-done.flag
    echo "Import complete"
else
    echo "The import has already been made."
fi
gosu neo4j:neo4j neo4j console
