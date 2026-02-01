## Goal
Single entrypoint that routes subcommands to Command objects

## Tasks
- [ ] create src/controller/cli_controller.py
- [ ] build argparse parser with subcommands:
  - [ ] ingest --feeds <n+>
  - [ ] analyze --limit/--source/--since
  - [ ] summarize --report summary|full --article-id
- [ ] instantiate correct Command and call execute()
- [ ] handle exceptions using error formatter

## Verify
python main.py --help and python main.py ingest --help work correctly

## Done when
CLI routes input to the correct command cleanly
