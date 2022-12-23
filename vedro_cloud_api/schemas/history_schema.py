from d42 import schema
from district42_exp_types.uuid_str import schema_uuid_str

__all__ = ("HistorySchema", "HistoryListSchema",)

HashSchema = schema.str.regex(r"[a-z0-9]{40}")

StatusSchema = schema.str("PASSED") | schema.str("FAILED") | schema.str("SKIPPED")

TimeStampSchema = schema.int.min(0)

HistorySchema = schema.dict({
    "id": schema_uuid_str,
    "launch_id": schema_uuid_str,
    "report_id": schema.str.len(1, 40) | schema.none,

    "scenario_hash": HashSchema,
    "scenario_rel_path": schema.str.len(1, ...),
    "scenario_subject": schema.str.len(1, ...),
    "scenario_namespace": schema.str.len(0, ...),

    "status": StatusSchema,
    "started_at": TimeStampSchema,
    "ended_at": TimeStampSchema,
})

HistoryListSchema = schema.list(HistorySchema)
