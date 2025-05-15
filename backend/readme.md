# Database initialization

CREATE DATABASE dss;
CREATE USER dss WITH PASSWORD 'dss';
GRANT ALL PRIVILEGES ON DATABASE dss TO dss;
ALTER ROLE dss SET timezone TO 'UTC';

