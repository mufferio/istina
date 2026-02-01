## Goal
Provide a reusable retry utility for flaky network/provider calls

## Tasks
- [ ] create src/utils/retry.py
- [ ] implement retry(fn, exceptions, max_attempts, base_delay, backoff_factor)
- [ ] ensure it re-raises after final failure
- [ ] add docstring with example usage

## Verify
A test function that fails twice then succeeds returns successfully

## Done when
Retry can be used by RSS adapter and providers safely
