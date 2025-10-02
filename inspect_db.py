import sqlite3
import json

conn = sqlite3.connect("jarvis_dev.db")
cur = conn.cursor()

print("=== Tasks ===")
for row in cur.execute("SELECT id, goal, status, created_at FROM tasks LIMIT 5"):
    print(row)

print("\n=== Task Logs ===")
for row in cur.execute("SELECT id, task_id, step_id, status, output, created_at FROM task_logs ORDER BY created_at DESC LIMIT 5"):
    # pretty print JSON output if possible
    try:
        output = json.loads(row[4]) if row[4] else None
    except:
        output = row[4]
    print(dict(id=row[0], task_id=row[1], step_id=row[2], status=row[3], output=output, created_at=row[5]))

conn.close()
