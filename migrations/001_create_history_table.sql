CREATE TYPE status AS ENUM ('PASSED', 'FAILED', 'SKIPPED');

CREATE TABLE history (
    "serial" SERIAL,

    "id" UUID NOT NULL,
    "launch_id" UUID NOT NULL,
    "report_id" varchar(255) NOT NULL,
    "report_hash" varchar(40) NOT NULL,

    "scenario_hash" varchar(40) NOT NULL,
    "scenario_path" varchar(255) NOT NULL,
    "scenario_subject" varchar(255) NOT NULL,

    "status" status NOT NULL,
    "started_at" timestamp NOT NULL,
    "ended_at" timestamp NOT NULL,
    "duration" interval NOT NULL,

    PRIMARY KEY ("serial")
);

CREATE INDEX ON history ("scenario_hash");
