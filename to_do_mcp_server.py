import psycopg2
import psycopg2.extras
import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Todo MCP Server")

def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )



@mcp.tool()
def get_todos(status: str = "") -> str:
    """
    Gibt alle ToDos zurück.
    Optional: Filtere nach Status, z.B. 'Offen', 'In Bearbeitung', 'Abgeschlossen'.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if status:
        cur.execute("SELECT * FROM todo WHERE status = %s ORDER BY id", (status,))
    else:
        cur.execute("SELECT * FROM todo ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return json.dumps([dict(r) for r in rows], ensure_ascii=False, default=str)


@mcp.tool()
def add_todo(todo: str, prioritaet: str = "Mittel", startdatum: str = "", enddatum: str = "", status: str = "Offen") -> str:
    """
    Fügt ein neues ToDo hinzu.
    Datumsformat: YYYY-MM-DD, z.B. '2026-04-10'.
    Priorität: 'Hoch', 'Mittel', 'Niedrig'.
    Status: 'Offen', 'In Bearbeitung', 'Abgeschlossen'.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        INSERT INTO todo (todo, prioritaet, startdatum, enddatum, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
        """,
        (todo, prioritaet, startdatum or None, enddatum or None, status)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps(dict(row), ensure_ascii=False, default=str)


@mcp.tool()
def update_todo(todo_id: int, todo: str = "", prioritaet: str = "", startdatum: str = "", enddatum: str = "", status: str = "") -> str:
    """
    Aktualisiert ein ToDo anhand seiner ID.
    Nur die übergebenen Felder werden geändert.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    felder = []
    werte = []
    if todo:
        felder.append("todo = %s");        werte.append(todo)
    if prioritaet:
        felder.append("prioritaet = %s");  werte.append(prioritaet)
    if startdatum:
        felder.append("startdatum = %s");  werte.append(startdatum)
    if enddatum:
        felder.append("enddatum = %s");    werte.append(enddatum)
    if status:
        felder.append("status = %s");      werte.append(status)
    if not felder:
        return json.dumps({"error": "Keine Felder zum Aktualisieren angegeben."})
    werte.append(todo_id)
    sql = f"UPDATE todo SET {', '.join(felder)} WHERE id = %s RETURNING *"
    cur.execute(sql, werte)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps(dict(row), ensure_ascii=False, default=str)


@mcp.tool()
def delete_todo(todo_id: int) -> str:
    """
    Löscht ein ToDo anhand seiner ID.
    Gibt den gelöschten Datensatz zurück.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("DELETE FROM todo WHERE id = %s RETURNING *", (todo_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps(dict(row), ensure_ascii=False, default=str)


if __name__ == "__main__":
    mcp.run()