# Synchronize the local database to PostgreSQL


```
ALTER TABLE auth
ALTER COLUMN active TYPE text USING active::text;

ALTER TABLE chat
ALTER COLUMN archived TYPE text USING archived::text,
ALTER COLUMN created_at TYPE text USING created_at::text,
ALTER COLUMN updated_at TYPE text USING updated_at::text;

ALTER TABLE auth
ALTER COLUMN active TYPE boolean USING active::boolean;

ALTER TABLE chat
ALTER COLUMN archived TYPE boolean USING archived::boolean,
ALTER COLUMN created_at TYPE int8 USING created_at::int8,
ALTER COLUMN updated_at TYPE int8 USING updated_at::int8;
```
