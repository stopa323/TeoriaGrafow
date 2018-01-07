import sqlite3
from random import randint

# l:admin1 h:kamil123
db_names_list = ['db — kopia.sqlite3']
conn = sqlite3.connect(db_names_list[0])
c = conn.cursor()
file_object = open("data.dat", "w")


c.execute('select first_name from auth_user WHERE is_staff = 1 and is_superuser = 0 ORDER BY id;')
teachers = [x[0] for x in c]
file_object.write('Teachers = {\n')

for teacher in teachers:
    file_object.write('\t<"' +teacher + '">\n')
file_object.write('};')
file_object.close()

c.execute('select nazwa_zajecia from camup_zajecia ORDER BY id;')
teachers = [x[0] for x in c]
file_object.write('Classes = {\n')

for teacher in teachers:
    file_object.write('\t<"' +teacher + '">\n')
file_object.write('};')
file_object.close()


#########################33
a = '[['
for i in range(0,28):
    a = a + '0 '
for i in range(0,28):
    a = a + '1 '


a = a +']]'