import urllib.request
import json
import time

def get_entity(id):
    url = f"https://cosylab.iiitd.edu.in/flavordb/entities_json?id={id}"
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode())

FRUIT_CATEGORIES = ['Fruit', 'Fruit Citrus', 'Fruit-Berry', 'Berry', 'Fruit Essence']

fruits = []
errors = []

for i in range(1, 979):
    try:
        data = get_entity(i)
        category = data.get('category_readable', '')

        if any(k in category for k in FRUIT_CATEGORIES):
            fruit = {
                'flavordb_id': data['entity_id'],
                'name_en': data['entity_alias_readable'],
                'category': category,
                'molecules': [
                    {
                        'pubchem_id': m['pubchem_id'],
                        'compound_name': m['common_name'],
                        'flavor_profile': m.get('flavor_profile', '')
                    }
                    for m in data.get('molecules', [])
                ]
            }
            fruits.append(fruit)
            print(f"✅ {fruit['name_en']} | {category} | 화합물 {len(fruit['molecules'])}개")

        time.sleep(0.1)

    except Exception as e:
        errors.append(i)

with open('data/fruits.json', 'w', encoding='utf-8') as f:
    json.dump(fruits, f, ensure_ascii=False, indent=2)

print(f"\n완료: 과일 {len(fruits)}개 수집")
print(f"실패 id: {errors}")