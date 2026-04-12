
# ToDo MCP Server – PostgreSQL + Claude Desktop

Ein einfacher MCP-Server (Model Context Protocol), der Claude Desktop ermöglicht,
eine PostgreSQL-Datenbank als persönliche ToDo-Verwaltung zu nutzen.
Dieses Projekt demonstriert, wie Claude über MCP-Tools direkt mit einer Datenbank
kommunizieren kann – ohne REST-API, ohne Framework-Overhead.

---

## 1. Projektbeschreibung

Dieses Projekt verbindet **Claude Desktop** über das **Model Context Protocol (MCP)**
mit einer **PostgreSQL-Datenbank**. Claude kann damit ToDos abfragen, anlegen,
aktualisieren und löschen – einfach per natürlicher Sprache.

> Beispiel: „Füge ein neues ToDo hinzu: Wäsche machen, Priorität Hoch, morgen."

Der Fokus liegt bewusst auf Einfachheit: eine Tabelle, vier Tools, kein Framework.
Ideal als Einstiegsprojekt für eigene MCP-Server-Entwicklungen.

---

## 2. Voraussetzungen

- Python 3.11 oder höher
- PostgreSQL 14 oder höher
- Claude Desktop (Windows, macOS)
- Folgende Python-Pakete:

```bash
pip install psycopg2-binary fastmcp
```

---

## 3. Datenbankeinrichtung

### Datenbank erstellen (UTF-8)

```sql
CREATE DATABASE todo_db
    WITH
    ENCODING     = 'UTF8'
    LC_COLLATE   = 'de_DE.UTF-8'
    LC_CTYPE     = 'de_DE.UTF-8'
    TEMPLATE     = template0;
```

### Tabelle erstellen

```sql
CREATE TABLE todo (
    id         SERIAL PRIMARY KEY,
    todo       VARCHAR(255) NOT NULL,
    prioritaet VARCHAR(20)  NOT NULL DEFAULT 'Mittel',
    startdatum DATE,
    enddatum   DATE,
    status     VARCHAR(20)  NOT NULL DEFAULT 'Offen'
);
```

### Beispieldaten einfügen

```sql
INSERT INTO todo (todo, prioritaet, startdatum, enddatum, status) VALUES
    ('MCP Server aufsetzen',       'Hoch',   '2026-04-02', '2026-04-05', 'In Bearbeitung'),
    ('LinkedIn Artikel schreiben', 'Hoch',   '2026-04-05', '2026-04-10', 'Offen'),
    ('PostgreSQL Backup einrichten','Mittel', '2026-04-07', '2026-04-09', 'Offen');
```

> **Hinweis:** In einer produktiven Anwendung würde man `prioritaet` und `status`
> in eigene Lookup-Tabellen mit Fremdschlüsseln auslagern.

---

## 4. Installation & Setup

```bash
# Repository klonen
git clone https://github.com/havefuntocode/todo-mcp.git
cd todo-mcp

# Abhängigkeiten installieren
pip install psycopg2-binary fastmcp
```

---

## 5. Projektstruktur

```
todo-mcp/
├── todo_mcp_server.py   # MCP-Server mit allen Tools
├── README.md            # Diese Datei
└── .gitignore           # Schützt sensible Dateien
```

---

## 6. Claude Desktop Konfiguration

Die Datenbankzugangsdaten werden **nicht im Code** gespeichert, sondern über
Umgebungsvariablen in der `claude_desktop_config.json` übergeben.

Pfad der Konfigurationsdatei:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "todo-mcp": {
      "command": "python",
      "args": ["C:/Pfad/zu/todo_mcp_server.py"],
      "env": {
        "DB_HOST":     "localhost",
        "DB_PORT":     "5432",
        "DB_NAME":     "todo_db",
        "DB_USER":     "dein_user",
        "DB_PASSWORD": "dein_passwort"
      }
    }
  }
}
```

Nach dem Speichern Claude Desktop neu starten.

---

## 7. Die MCP-Tools im Überblick

| Tool           | Beschreibung                              | Parameter                                              |
|----------------|-------------------------------------------|--------------------------------------------------------|
| `get_todos`    | Alle ToDos abrufen                        | `status` *(optional)*: z.B. `'Offen'`                 |
| `add_todo`     | Neues ToDo anlegen                        | `todo`, `prioritaet`, `startdatum`, `enddatum`, `status` |
| `update_todo`  | Vorhandenes ToDo aktualisieren            | `todo_id` *(Pflicht)*, alle weiteren optional          |
| `delete_todo`  | ToDo anhand der ID löschen               | `todo_id`                                              |

### Beispiel-Interaktion mit Claude

> **Nutzer:** „Füge ein neues ToDo hinzu: Wäsche machen, Priorität Hoch, für morgen."
>
> **Claude** ruft `add_todo` auf mit:
> ```json
> {
>   "todo": "Wäsche machen",
>   "prioritaet": "Hoch",
>   "startdatum": "2026-04-03",
>   "enddatum": "2026-04-03",
>   "status": "Offen"
> }
> ```
>
> **Claude:** „Erledigt! Das ToDo 'Wäsche machen' wurde erfolgreich angelegt."

---

## 8. Sicherheitshinweis & .gitignore

Die Zugangsdaten befinden sich ausschließlich in der `claude_desktop_config.json`
auf deinem lokalen Rechner – **niemals im Code oder im Repository**.

Empfohlene `.gitignore`:

```
# Sensible Dateien
.env
*.env
claude_desktop_config.json

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# Editor
.vscode/
.idea/
```

---

## 9. Lizenz

Dieses Projekt steht unter der [MIT License](https://opensource.org/licenses/MIT).
Du darfst es frei verwenden, anpassen und weitergeben.


