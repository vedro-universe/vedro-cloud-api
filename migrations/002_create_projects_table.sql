-- +goose Up
CREATE TABLE projects (
    "id" varchar(40) NOT NULL,
    "created_at" timestamp NOT NULL,

    PRIMARY KEY ("id")
);

-- +goose Down
DROP TABLE projects;
