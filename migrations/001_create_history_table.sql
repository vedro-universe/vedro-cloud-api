DROP TABLE IF EXISTS history;
DROP TYPE IF EXISTS status;

CREATE TYPE status AS ENUM ('PASSED', 'FAILED', 'SKIPPED');

CREATE TABLE history (
    "id" UUID NOT NULL,

    "scenario_id" varchar(255) NOT NULL,
    "scenario_hash" varchar(40) NOT NULL,
    "scenario_path" varchar(255) NOT NULL,
    "scenario_subject" varchar(255) NOT NULL,
    "status" status NOT NULL,
    "started_at" timestamp NOT NULL,
    "ended_at" timestamp NOT NULL,
    "duration" interval NOT NULL,

    PRIMARY KEY ("id")
);

CREATE INDEX ON history ("scenario_hash");
