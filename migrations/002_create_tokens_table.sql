-- +goose Up
CREATE TABLE tokens (
    "token" UUID NOT NULL,
    "description" varchar(255) NOT NULL,
    "created_at" timestamp NOT NULL,

    PRIMARY KEY ("token")
);

-- +goose Down
DROP TABLE tokens;
