## Goal
Ensure CLI prints readable errors and exits with correct codes

## Tasks
- [ ] centralize exception handling in controller or main.py
- [ ] use format_exception(e) for user output
- [ ] optionally support debug mode for stack traces
- [ ] ensure non-zero exit codes on failure

## Verify
Trigger ConfigError and ensure CLI prints friendly message (no stack trace in normal mode)

## Done when
CLI failure modes are predictable and user-friendly
