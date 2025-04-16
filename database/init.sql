-- Create roles for PostgREST
CREATE ROLE anon NOINHERIT;
CREATE ROLE authenticator NOINHERIT;

-- Grant necessary permissions to anon (for unauthenticated access)
GRANT USAGE ON SCHEMA public TO anon;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;
-- Optionally, allow anon to insert/update/delete (adjust as needed)
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO anon;

-- Grant authenticator access to switch to anon
GRANT anon TO authenticator;

-- Create a sample table (optional, for testing)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Grant permissions on the table to anon
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO anon;
