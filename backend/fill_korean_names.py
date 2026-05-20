import psycopg2
import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("@db:", "@localhost:")

url = DATABASE_URL.replace("postgresql://", "")
user_pass, host_db = url.split("@")
user, password = user_pass.split(":")
host_port, dbname = host_db.split("/")
host, port = host_port.split(":")

conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
cursor = conn.cursor()

cursor.execute("SELECT id, name_en FROM fruits WHERE name_ko IS NULL")
fruits = cursor.fetchall()

def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:12b",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

for fruit_id, name_en in fruits:
    try:
        prompt = f"""Translate the fruit name '{name_en}' to Korean.
Reply ONLY with valid JSON, no explanation, no markdown:
{{"name_ko": "한글이름"}}"""

        response_text = ask_ollama(prompt)
        match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            raise ValueError(f"JSON 없음: {response_text}")

        name_ko = data.get("name_ko")

        cursor.execute("""
                       UPDATE fruits
                       SET name_ko = %s
                       WHERE id = %s
                       """, (name_ko, fruit_id))

        conn.commit()
        print(f"✅ {name_en} → {name_ko}")

    except Exception as e:
        print(f"❌ {name_en} | 에러: {e}")

cursor.close()
conn.close()
print("\n완료!")