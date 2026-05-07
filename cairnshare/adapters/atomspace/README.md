# AtomSpace adapter plan

AtomSpace is the first CairnShare target because it is a semantic hypergraph with typed atoms, predicates, values, and optional reasoning.

The safe default adapter should support:
- seeded expansion
- atom type allowlists
- predicate allowlists
- depth, frontier, result, and timeout bounds
- projection filtering before results leave the adapter
- reasoning disabled by default unless both the Analysis Bundle and Share Policy allow a bounded reasoning profile

The v0 adapter should implement `capabilities`, `dry_run`, `execute`, and `explain`, emitting CairnShare Dry-Run Reports and Execution Receipts.
