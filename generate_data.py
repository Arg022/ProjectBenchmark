import csv
import json
from faker import Faker

fake = Faker()

# Set per tenere traccia dei valori unici per ogni campo
emails = set()
names = set()
addresses = set()

insert_data = []
update_data = []

# Genera 5000 record per il CSV e JSON di insert
with open('insert_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'nome', 'email', 'indirizzo'])
    for i in range(5000):
        # Assicurati che ogni campo sia unico
        name = fake.name()
        while name in names:
            name = fake.name()
        names.add(name)
        
        email = fake.email()
        while email in emails:
            email = fake.email()
        emails.add(email)
        
        address = fake.address()
        while address in addresses:
            address = fake.address()
        addresses.add(address)
        
        row = {"id": i+1, "nome": name, "email": email, "indirizzo": address}
        insert_data.append(row)
        writer.writerow([i+1, name, email, address])

# Scrivi i dati insert in un file JSON
with open('insert_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(insert_data, json_file, indent=4)

# Genera 5000 record per il CSV e JSON di update (solo l'indirizzo)
with open('update_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'indirizzo'])
    for i in range(5000):
        address = fake.address()
        while address in addresses:
            address = fake.address()
        addresses.add(address)
        
        update_data.append({"id": i, "indirizzo": address})
        writer.writerow([i, address])

# Scrivi i dati update in un file JSON
with open('update_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(update_data, json_file, indent=4)
