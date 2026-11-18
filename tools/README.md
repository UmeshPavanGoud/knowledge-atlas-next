# Data tools

Run `python tools/build_catalog.py` after updating the YAML source archive, `python tools/build_pathways.py` after updating the pathway source archive, then run `python tools/validate_data.py` to check resource IDs, URL shape, subject/domain membership, exact duplicate URLs and every resource ID referenced by a pathway.

The JSON files in `data/` are the current application source of truth. `source-archive/catalog-original.yaml` preserves the original YAML snapshot. A future curation importer should be added here when the review workflow is formalized; do not hand-edit the generated SQLite database.
