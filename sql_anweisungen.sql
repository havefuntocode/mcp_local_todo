CREATE DATABASE todo_db
    WITH
    ENCODING     = 'UTF8'
    LC_COLLATE   = 'de_DE.UTF-8'
    LC_CTYPE     = 'de_DE.UTF-8'
    TEMPLATE     = template0;

-- Tabelle: todo
CREATE TABLE todo (
    id         SERIAL PRIMARY KEY,
    todo       VARCHAR(255) NOT NULL,
    prioritaet VARCHAR(20)  NOT NULL DEFAULT 'Mittel',
    startdatum DATE,
    enddatum   DATE,
    status     VARCHAR(20)  NOT NULL DEFAULT 'Offen'
);

-- Ein paar Beispieldaten
INSERT INTO todo (todo, prioritaet, startdatum, enddatum, status) VALUES
    ('MCP Server aufsetzen',  'Hoch',    '2026-04-06', '2026-04-06', 'In Bearbeitung'),
    ('LinkedIn Artikel schreiben', 'Hoch', '2026-04-07', '2026-04-08', 'Offen'),
    ('PostgreSQL Backup einrichten', 'Mittel', '2026-04-09', '2026-04-10', 'Offen');