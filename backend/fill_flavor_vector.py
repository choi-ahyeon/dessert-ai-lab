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

cursor.execute("SELECT id, name_en FROM fruits WHERE sweetness_score IS NULL")
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
        prompt = f"""You are a food scientist. Rate the fruit '{name_en}' on the following taste dimensions from 1 to 10.
Use these reference points:
- Apple = middle reference (sweetness 5, acidity 5, bitterness 2, creaminess 1, juiciness 6, richness 3, freshness 6)
- Lemon = high acidity reference (sweetness 2, acidity 10, bitterness 3, creaminess 0, juiciness 8, richness 1, freshness 9)
- Banana = high sweetness and creaminess reference (sweetness 8, acidity 2, bitterness 1, creaminess 6, juiciness 4, richness 5, freshness 4)

Rate '{name_en}' compared to these references.
Reply ONLY with valid JSON, no explanation, no markdown:
{{"sweetness": 0, "acidity": 0, "bitterness": 0, "creaminess": 0, "juiciness": 0, "richness": 0, "freshness": 0}}"""

        response_text = ask_ollama(prompt)
        match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            raise ValueError(f"JSON 없음: {response_text}")

        cursor.execute("""
                       UPDATE fruits
                       SET sweetness_score = %s,
                           acidity_score = %s,
                           bitterness_score = %s,
                           creaminess_score = %s,
                           juiciness_score = %s,
                           richness_score = %s,
                           freshness_score = %s,
                           vector_verified = false
                       WHERE id = %s
                       """, (
                           data.get("sweetness"),
                           data.get("acidity"),
                           data.get("bitterness"),
                           data.get("creaminess"),
                           data.get("juiciness"),
                           data.get("richness"),
                           data.get("freshness"),
                           fruit_id
                       ))

        print(f"{name_en} | 단맛:{data.get('sweetness')} 산미:{data.get('acidity')} 신선:{data.get('freshness')}")

    except Exception as e:
        print(f"{name_en} | 에러: {e}")

conn.commit()
cursor.close()
conn.close()
print("\n완료!")