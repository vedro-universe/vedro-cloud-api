CREATE TABLE scenario_results (
    "id" UUID PRIMARY KEY,
    "status" scenario_status NOT NULL,
    "started_at" TIMESTAMP,
    "ended_at" TIMESTAMP,
    "scenario" JSONB NOT NULL,
    "step_results" JSONB NOT NULL
);
