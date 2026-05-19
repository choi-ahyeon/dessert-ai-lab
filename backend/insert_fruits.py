import json
import uuid
from datetime import datetime, timezone
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

url = DATABASE_URL.replace("postgresql://", "")
user_pass, host_db = url.split("@")
user, password = user_pass.split(":")
host_port, dbname = host_db.split("/")
host, port = host_port.split(":")

conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=dbname,
    user=user,
    password=password
)

cursor = conn.cursor()

with open("/data/fruits.json", "r", encoding="utf-8") as f:
    fruits = json.load(f)

now = datetime.now(timezone.utc)
success = 0
fail = 0

for fruit in fruits:
    try:
        fruit_id = str(uuid.uuid4())

        cursor.execute("""
                       INSERT INTO fruits (id, name_en, flavordb_id, category, created_at)
                       VALUES (%s, %s, %s, %s, %s)
                       """, (fruit_id, fruit['name_en'], fruit['flavordb_id'], fruit['category'], now))

        for molecule in fruit.get('molecules', []):
            compound_id = str(uuid.uuid4())
            cursor.execute("""
                           INSERT INTO fruit_compounds (id, fruit_id, pubchem_id, compound_name, flavor_profile, created_at)
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """, (
                               compound_id,
                               fruit_id,
                               molecule['pubchem_id'],
                               molecule['compound_name'],
                               molecule['flavor_profile'],
                               now
                           ))

        print(f"✅ {fruit['name_en']} | 화합물 {len(fruit['molecules'])}개")
        success += 1

    except Exception as e:
        print(f"❌ {fruit['name_en']} | 에러: {e}")
        fail += 1

conn.commit()
cursor.close()
conn.close()

print(f"\n완료: 성공 {success}개, 실패 {fail}개")