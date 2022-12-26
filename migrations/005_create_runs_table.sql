-- +goose Up
CREATE TABLE runs (
    "serial" SERIAL,

    "id" UUID NOT NULL,
    "launch_id" UUID NOT NULL,
    "report_id" UUID NOT NULL,
    "project_id" varchar(40) NOT NULL,
    "scenario_id" UUID NOT NULL,

    "status" status NOT NULL,
    "started_at" timestamp NOT NULL,
    "ended_at" timestamp NOT NULL,
    "duration" interval NOT NULL,

    "created_at" timestamp NOT NULL,
    "updated_at" timestamp NOT NULL,

    PRIMARY KEY ("id"),

    CONSTRAINT "runs_scenario_id_fkey" FOREIGN KEY ("scenario_id") REFERENCES scenarios ("id")
        ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT "runs_project_id_fkey" FOREIGN KEY ("project_id") REFERENCES projects ("id")
        ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT "runs_report_id_fkey" FOREIGN KEY ("report_id") REFERENCES reports ("id")
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- +goose Down
DROP TABLE runs;
