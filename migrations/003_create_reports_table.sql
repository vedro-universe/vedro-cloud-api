CREATE TABLE IF NOT EXISTS reports (
    "id" UUID NOT NULL,

    "report_id" varchar(40) NOT NULL,
    "project_id" varchar(40) NOT NULL,
    "snapshot" integer NOT NULL, -- serial ref (4 bytes)

    "created_at" timestamp NOT NULL,
    "updated_at" timestamp NOT NULL,

     PRIMARY KEY ("id"),
     UNIQUE ("report_id", "project_id"),

    CONSTRAINT "reports_project_id_fkey" FOREIGN KEY ("project_id") REFERENCES projects ("id")
        ON DELETE CASCADE ON UPDATE CASCADE
);
