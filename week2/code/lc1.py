birds = ( ('Passerculus sandwichensis','Savannah sparrow',18.7),
          ('Delichon urbica','House martin',19),
          ('Junco phaeonotus','Yellow-eyed junco',19.5),
          ('Junco hyemalis','Dark-eyed junco',19.6),
          ('Tachycineata bicolor','Tree swallow',20.2),
         )

#(1) Write three separate list comprehensions that create three different
# lists containing the latin names, common names and mean body masses for
# each species in birds, respectively. 

Latin_names = [i[0] for i in birds]
Common_names = [i[1] for i in birds]
Mean_body_masses = [i[2] for i in birds]

print(Latin_names)
print(Common_names)
print(Mean_body_masses)

# (2) Now do the same using conventional loops (you can choose to do this 
# before 1 !). 

list_birds = list(birds)

latin_names = []
for i in list_birds:
    latin_names.append(i[0])
print(latin_names)

common_names = []
for i in list_birds:
    common_names.append(i[1])
print(common_names)

mean_body_masses = []
for i in list_birds:
    mean_body_masses.append(i[2])
print(mean_body_masses)

# A nice example out out is:
# Step #1:
# Latin names:
# ['Passerculus sandwichensis', 'Delichon urbica', 'Junco phaeonotus', 'Junco hyemalis', 'Tachycineata bicolor']
# ... etc.




