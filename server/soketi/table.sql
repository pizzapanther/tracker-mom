CREATE TABLE IF NOT EXISTS apps (
    id varchar(255) PRIMARY KEY,
    "key" varchar(255) NOT NULL,
    secret varchar(255) NOT NULL,
    max_connections integer NOT NULL,
    enable_client_messages smallint NOT NULL,
    "enabled" smallint NOT NULL,
    max_backend_events_per_sec integer NOT NULL,
    max_client_events_per_sec integer NOT NULL,
    max_read_req_per_sec integer NOT NULL,
    max_presence_members_per_channel integer DEFAULT NULL,
    max_presence_member_size_in_kb integer DEFAULT NULL,
    max_channel_name_length integer DEFAULT NULL,
    max_event_channels_at_once integer DEFAULT NULL,
    max_event_name_length integer DEFAULT NULL,
    max_event_payload_in_kb integer DEFAULT NULL,
    max_event_batch_size integer DEFAULT NULL,
    webhooks json,
    enable_user_authentication smallint NOT NULL
);
