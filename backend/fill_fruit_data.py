import psycopg2
import os
import json
import re
import anthropic
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

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

cursor.execute("SELECT id, name_en FROM fruits WHERE ph IS NULL OR sugar_per_100g IS NULL")
fruits = cursor.fetchall()

for fruit_id, name_en in fruits:
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": f"""과일 '{name_en}'의 평균적인 당도와 산도를 알려줘.
반드시 아래 JSON 형식으로만 답해줘. 다른 텍스트 없이 JSON만.
{{
  "sugar_per_100g": 숫자,
  "ph": 숫자
}}"""
                }
            ]
        )

        response_text = message.content[0].text
        match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            raise ValueError(f"JSON 없음: {response_text}")

        sugar = data.get("sugar_per_100g")
        ph = data.get("ph")

        cursor.execute("""
                       UPDATE fruits
                       SET sugar_per_100g = %s, ph = %s, ph_verified = false
                       WHERE id = %s
                       """, (sugar, ph, fruit_id))

        print(f"✅ {name_en} | 당도: {sugar} | pH: {ph}")

    except Exception as e:
        print(f"❌ {name_en} | 에러: {e}")

conn.commit()
cursor.close()
conn.close()
print("\n완료!")