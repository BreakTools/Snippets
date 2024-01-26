"""Super simple script to remove that weird vaccine Maya 'virus' from Maya ASCII files.
If your computer is still infected you must also remove all references to the virus
from your \documents\maya\scripts folder. Otherwise it'll come back. Oh dear god.

Essentially this script just goes through all nodes in your file and removes the
ones that reference the 'virus'."""

PATH_TO_INFECTED_FILE = "D:/infected_file.ma"
PATH_TO_NEW_FILE = "D:/fixed_file.ma"

with open(PATH_TO_INFECTED_FILE, "r") as f:
    file = f.read()

lines_in_file = file.split("\n")
lines_to_keep = []

print("Starting removal of all malicious script nodes...")

references_to_virus = 0
remove_line = False
for line in lines_in_file:
    if "vaccine_gene" in line or "breed_gene" in line:
        references_to_virus += 1
        remove_line = True
    elif line.strip().startswith("createNode") and remove_line:
        remove_line = False
    elif not remove_line:
        lines_to_keep.append(line)

fixed_file = "\n".join(lines_to_keep)

new_file = open(PATH_TO_NEW_FILE, "w")
new_file.write(fixed_file)
new_file.close()
print(f"Done! Removed {references_to_virus} instances of the malicious script node.")
