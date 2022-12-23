DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status') THEN
        CREATE TYPE status AS ENUM ('PASSED', 'FAILED', 'SKIPPED');
    END IF;
END
$$;
