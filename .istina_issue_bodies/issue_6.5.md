## Goal
Prevent accidental quota exhaustion for real providers

## Tasks
- [ ] create src/utils/rate_limiter.py
- [ ] implement a simple RPM limiter (sleep when exceeding)
- [ ] ensure it is injectable/optional (MockProvider doesn’t need it)
- [ ] add basic tests if feasible

## Verify
A loop of N calls respects configured rate limit

## Done when
Provider calls can be throttled consistently
