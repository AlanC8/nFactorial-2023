lines_seen = set()
outfile = open("record.txt", "w")
for line in open("reduced_record.txt", "r"):
    if line not in lines_seen:
        outfile.write(line)
        lines_seen.add(line)
outfile.close()