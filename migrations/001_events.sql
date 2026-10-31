CREATE TABLE IF NOT EXISTS wardspace_events (
 id text PRIMARY KEY,
 session_id text NOT NULL,
 payload jsonb NOT NULL,
 received_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS wardspace_session_time ON wardspace_events(session_id,received_at DESC);
