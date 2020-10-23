drawing = []
maxx, maxy = 0, 0
with open("points10.txt") as f:
    for line in f.readlines():
        if line != "":
            x, y = line.rstrip("\n").split(",")
            maxx, maxy = max(maxx, float(x)), max(maxy, float(y))
            drawing.append([float(x), float(y)])

for i, d in enumerate(drawing):
    drawing[i] = [d[0] / maxx, d[1] / maxy]

print(drawing)
