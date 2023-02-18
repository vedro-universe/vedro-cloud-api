-- +goose Up
CREATE TABLE projects (
    "_id" UUID NOT NULL,
    "id" varchar(40) NOT NULL,
    "name" varchar(40) NOT NULL,
    "created_at" timestamp NOT NULL,

    PRIMARY KEY ("_id")
);

-- +goose Down
DROP TABLE projects;
