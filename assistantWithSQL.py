import sqlite3, os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

db = sqlite3.connect("chat.db")
db.execute("""
CREATE TABLE IF NOT EXISTS m(
    id INTEGER PRIMARY KEY,
    role TEXT,
    content TEXT
)
""")
db.commit()

def add(role, txt):
    db.execute("INSERT INTO m(role, content) VALUES(?, ?)", (role, txt))
    db.commit()

def msgs():
    return [{"role": r, "content": c}
            for r, c in db.execute("SELECT role, content FROM m ORDER BY id")]

print("Мини-чат (OpenAI + SQLite). Ctrl+C для выхода.")

while True:
    try:
        q = input("Ты: ").strip()
    except:
        print("\nПока!")
        break

    if not q:
        continue

    add("user", q)

    reply = client.chat.completions.create(
        model=MODEL,
        messages=msgs()
    ).choices[0].message.content

    add("assistant", reply)
    print("Бот:", reply, "\n")