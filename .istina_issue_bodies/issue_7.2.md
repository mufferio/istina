## Goal
Encapsulate scoring operation as a visitor

## Tasks
- [ ] create src/model/visitors/scoring_visitor.py
- [ ] constructor takes BaseProvider
- [ ] visit(article) returns BiasScore by calling provider

## Verify
Visiting an Article returns same BiasScore as provider directly

## Done when
Scoring can be treated as a modular operation
