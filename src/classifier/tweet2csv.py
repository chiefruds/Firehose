from Dictionary import Encoder
import numpy

encoder = Encoder()
arr = []
labels = []
FILE_DATA = "resources/data.csv"
FILE_LABEL = "resources/labels.csv"
label_types = {
    "unrelated": 0,
    "savings": 1,
    "investment": 2,
    "insurance": 3,
    "health": 4,
    "mortgages": 5,
    "loan": 6,
    "retirement": 7
}

files = {
    "unrelated": label_types["unrelated"],
    "damage": label_types["insurance"],
    "Allianz": label_types["investment"],
    "AXA": label_types["insurance"],
    "bank": label_types["investment"],
    "claim": label_types["insurance"],
    "cost": label_types["savings"],
    "credit": label_types["loan"],
    "dental": label_types["health"],
    "dentist": label_types["health"],
    "deposit": label_types["mortgages"],
    "finance": label_types["loan"],
    "financial": label_types["loan"],
    "health": label_types["health"],
    "hospital": label_types["health"],
    "hsbc": label_types["investment"],
    "icbc": label_types["investment"],
    "insurance": label_types["insurance"],
    "interest": label_types["loan"],
    "invest": label_types["investment"],
    "loan": label_types["loan"],
    "mortgage": label_types["mortgages"],
    "pension": label_types["retirement"],
    "retirement": label_types["retirement"],
    "saving": label_types["savings"],
    "sick": label_types["health"],
    "stock": label_types["investment"],
    "tax": label_types["investment"]}

for filename in files:
    print("Working on filename", filename)

    with open("resources/dataset/" + filename + ".csv") as file:
        while True:
            line = file.readline().strip('\n')
            if line is None or line == "":
                break
            arr.append(encoder.encode(line))
            labels.append(files[filename])

print("Converting to numpy matrix")
nparray = numpy.array(arr)

print("Saving data to", FILE_DATA)
numpy.savetxt(FILE_DATA, nparray, delimiter=',', fmt='%d')

print("Saving labels to", FILE_LABEL)
numpy.savetxt(FILE_LABEL, labels, delimiter=',', fmt='%d')
