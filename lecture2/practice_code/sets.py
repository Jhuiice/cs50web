# Why use a set? Are they faster than using a search and sorting algorithm? 
# I think it depends on the context of what you are sorting or searching.
# REASON:
# Sets self sort

s = set()

s.add(1)
s.add(2)
s.add(1)
s.add(3)


# shows that sets have no duplicates
for item in s:
    print(item)