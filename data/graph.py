import csv
import json

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")


def read_out(file):
    data_out = []
    with open(file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader, None)  # Skip headers
        for row in reader:
            data_out.append((row[0], int(row[1])))

    return data_out


with open("../creds.json", "r") as vut:
    valid_usernames: set = set(json.loads(vut.read()).keys())

data_raw = read_out("login_2.csv")

# Remove outliers
data = [d for d in data_raw if d[1] < 340]
valid_users = [i[1] for i in data if i[0] in valid_usernames]
invalid_users = [i[1] for i in data if i[0] not in valid_usernames]


ax = sns.histplot(
    {"Valid users": valid_users, "Invalid users": invalid_users},
    # {"Possible users": all_data},
    stat="percent",
    # element="step"
)
# plt.grid()
ax.set_xlabel("Response time (MS)")
plt.savefig("./mapped_histo.png")
plt.show()
