# Question B — Level 3

## Objective

Evaluate the reliability and safety of the health-risk application under failure conditions and concurrent usage.

## Planned Break/Fix Experiments

Two deliberate application failures will be introduced, reproduced, diagnosed, and fixed.

### Break/Fix 1

Status: Pending

### Break/Fix 2

Status: Pending

## Concurrent Usage

The application will also be evaluated for approximately 100 concurrent users.

The evaluation will consider:

- API response behavior
- Database connection handling
- Model inference
- Request failures
- Resource usage
- Database connection limits
- Appropriate safeguards for concurrent access

Results will be documented after testing.

## Safety Considerations

The application should:

- Validate all incoming data server-side.
- Avoid hardcoded database credentials.
- Use parameterized SQL.
- Restrict CORS origins.
- Avoid exposing internal server errors to users.
- Handle database/API failures gracefully.
- Avoid collecting unnecessary personal information.
- Use appropriate database connection management for concurrent requests.

Final break/fix and concurrency results will be added after testing.