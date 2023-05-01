import json
import random

import faker

"""Creates the fake data for the site & test lists for burp"""
faker = faker.Faker()
with open("rockyou.txt", "r", errors="replace") as ry:
    passwords = ry.readlines()

data = {}
burp_password_list = []
burp_user_name_list = []
for _ in range(5000):
    username = faker.unique.user_name()
    password = random.choice(passwords).rstrip()
    data[username] = password
    burp_password_list.append(password)
    burp_user_name_list.append(username)

with open("creds.json", "w") as out:
    out.write(json.dumps(data, indent=4))

for _ in range(5000):
    burp_user_name_list.append(faker.unique.user_name())
    burp_password_list.append(random.choice(passwords).rstrip())

with open("burp_user_names.txt", "w") as buno:
    random.shuffle(burp_user_name_list)
    buno.write("\n".join(burp_user_name_list))

with open("burp_password_list.txt", "w") as bplo:
    random.shuffle(burp_password_list)
    bplo.write("\n".join(burp_password_list))
