def readtolist(l, path):
    try:
        with open(path, "r") as f:
            while True:
                line = f.readline()
                if not line:
                     break
                num = [int(float(s)) if float(s).is_integer() else float(s) for s in line.split()]
                l.append(num)
    except MemoryError:
            print("READING ERROR!")
            print("OUT OF MEMORY")