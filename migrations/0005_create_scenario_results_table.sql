CREATE TABLE scenario_results (
    "id" UUID PRIMARY KEY,
    "launch_id" VARCHAR(64) NOT NULL,

    "status" scenario_status NOT NULL,
    "started_at" TIMESTAMP,
    "ended_at" TIMESTAMP,
    "scenario" JSONB NOT NULL,
    "step_results" JSONB NOT NULL,

    "created_at" TIMESTAMP NOT NULL
);
