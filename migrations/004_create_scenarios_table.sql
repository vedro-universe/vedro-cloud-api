-- +goose Up
CREATE TABLE scenarios (
    "id" UUID NOT NULL,

    "scenario_id" varchar(40) NOT NULL,
    "project_id" varchar(40) NOT NULL,

    "subject" varchar(255) NOT NULL,
    "namespace" varchar(255) NOT NULL,
    "rel_path" varchar(255) NOT NULL,

    "created_at" timestamp NOT NULL,
    "updated_at" timestamp NOT NULL,

    PRIMARY KEY ("id"),
    UNIQUE ("scenario_id", "project_id"),

    CONSTRAINT "scenarios_project_id_fkey" FOREIGN KEY ("project_id") REFERENCES projects ("id")
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- +goose Down
DROP TABLE scenarios;
