-- +goose Up
CREATE TYPE status AS ENUM ('PASSED', 'FAILED', 'SKIPPED');

-- +goose Down
DROP TYPE status;
