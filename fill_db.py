import sqlite3
from random import randint

# l:admin1 h:kamil123
db_names_list = ['db — kopia.sqlite3']
conn = sqlite3.connect(db_names_list[0])
c = conn.cursor()
alphabet = 'abcdefghijklmnoprtsquwrtsxyz'
lata_studiow = 5
kursy = []

for wydzial in alphabet[0:2]:
    for rok in range(2012, lata_studiow + 2012):
        kursy.append(wydzial + str(rok))


### Studenci
liczba_studentow = 0;
for kurs in kursy:
    for student in range (500, 550):
        liczba_studentow=liczba_studentow+1
        c.execute("INSERT INTO auth_user (password,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,username) VALUES(?,?,?,?,?,?,?,?,?)",
                  ('pbkdf2_sha256$24000$PdqkzVZvW6mx$L2BLUJp8ZVgN+/R1zSOz0J9+pzpEBZklsxFlsX+9jBQ=',
                   0, 'student'+str(student)+kurs, kurs," ", 0, 1,'2017-11-22 11:21:28.771991', 'student'+str(student)+kurs))
        #c.execute("INSERT INTO auth_user_groups(user_id,group_id) VALUES(?,?)")
        conn.commit()
        c.execute('select last_insert_rowid() from auth_user LIMIT 1;')
        id = [x[0] for x in c][0]
        c.execute("INSERT INTO auth_user_groups (user_id,group_id) VALUES(?,?)",
                  (id, 2))
        c.execute('select id from camup_kurs;')

### Preferencje Studenta
        kursy_id = [x[0] for x in c]
        c.execute("INSERT INTO camup_macierz_preferncji DEFAULT VALUES ")
        conn.commit()
        c.execute('select last_insert_rowid() from camup_macierz_preferncji LIMIT 1;')
        matrix_id = [x[0] for x in c][0]
        for dzien in range(0, 5):
            for godzina in range(8, 22):
                c.execute("INSERT INTO camup_cell (row,col,val,matrix_id) VALUES(?,?,?,?) ",
                          (godzina, dzien, 1, matrix_id))
        conn.commit()
        c.execute("INSERT INTO camup_prefernecje_studenta (kurs_id,macierz_preferencji_id,student_id) VALUES (?,?,?)",
                  (kursy_id[randint(0, len(kursy_id)-1)], matrix_id, id))
        conn.commit()


### Prowadzacy
for prowadzacy in range (102, 150):
    c.execute("INSERT INTO auth_user (password,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,username) VALUES(?,?,?,?,?,?,?,?,?)",
              ('pbkdf2_sha256$24000$PdqkzVZvW6mx$L2BLUJp8ZVgN+/R1zSOz0J9+pzpEBZklsxFlsX+9jBQ=',
               0, 'prowadzacy'+str(prowadzacy), " "," ", 1, 1,'2017-11-22 11:21:28.771991', 'prwoadzacy'+str(prowadzacy)))
    #c.execute("INSERT INTO auth_user_groups(user_id,group_id) VALUES(?,?)")
    conn.commit()
    c.execute('select last_insert_rowid() from auth_user LIMIT 1;')
    id = [x[0] for x in c][0]
    c.execute("INSERT INTO auth_user_groups (user_id,group_id) VALUES(?,?)",
              (id, 1))
### Preferencje Prowadzacych

    c.execute("INSERT INTO camup_macierz_preferncji DEFAULT VALUES ")
    conn.commit()

    c.execute('select last_insert_rowid() from camup_macierz_preferncji LIMIT 1;')
    matrix_id = [x[0] for x in c][0]
    for dzien in range(0, 5):

        for godzina in range(8,22):
            c.execute("INSERT INTO camup_cell (row,col,val,matrix_id) VALUES (?,?,?,?)",
                      (godzina, dzien, 1, matrix_id))
    conn.commit()
    odstepy_miedzy_zajeciami=[5,10,15,20]
    boolean_value = [True,False]
    c.execute("INSERT INTO camup_prefernecje_prowadzacego (maksymalna_ilosc_zajec_pod_rzad,maksymalna_ilosc_cwiczen_pod_rzad,przerwa_obiadowa_tag,wolny_dzien_tag,prowadzacy_id,minut_przerw_miedzy_zajeciami,macierz_preferencji_id) VALUES (?,?,?,?,?,?,?)",
              (randint(1,5),randint(1,5),boolean_value[randint(0,1)],boolean_value[randint(0,1)],id,odstepy_miedzy_zajeciami[randint(0, len(odstepy_miedzy_zajeciami)-1)],matrix_id))
    conn.commit()

### Kursy
for char in alphabet[0:5]:
    for rok in range(2012, lata_studiow+2012):
        curs_name =  char + str(rok)
        c.execute("INSERT INTO camup_kurs (kod_kursu,rok) VALUES(?,?)",
                  (curs_name, rok))
    conn.commit()

### Budynki
c.execute("INSERT INTO camup_budynek (kod_budynku, latitude, longitude) VALUES(?,?,?)",
            ('budynek5',"50.067052","19.915187"))
c.execute("INSERT INTO camup_budynek (kod_budynku, latitude, longitude) VALUES(?,?,?)",
            ('budynek6',"50.067054","19.914921"))
c.execute("INSERT INTO camup_budynek (kod_budynku, latitude, longitude) VALUES(?,?,?)",
            ('budynek7',"50.070957","19.906825"))
conn.commit()


### Sale
c.execute("SELECT id FROM camup_budynek ORDER BY RANDOM() LIMIT 1;")
budynek_id = [x[0] for x in c]
wielosc_sal = [18,30,30,100]
for char in alphabet:
    c.execute("INSERT INTO camup_sala (kod_sali,ilosc_miejsc, budynek_id, rzutnik_tag, komputer_tag, tablica_tag) VALUES(?,?,?,?,?,?)",
              ('sala_'+char, wielosc_sal[randint(0, 3)],  budynek_id[0] ,randint(0, 1),randint(0, 1),randint(0, 1)))
conn.commit()


### Zajecia
dlugosc_zajec = [90,90,90,90,90,90,120,180]
for kurs in kursy:
    for char in alphabet[0:8]:
        c.execute("SELECT id FROM camup_kurs ORDER BY RANDOM() LIMIT 1;")
        kurs_id = [x[0] for x in c][0]
        c.execute("SELECT id FROM auth_user WHERE is_staff =1 and is_superuser = 0 ORDER BY RANDOM() LIMIT 1;")
        prowadzacy_id = [x[0] for x in c][0]
        c.execute("INSERT INTO camup_zajecia (nazwa_zajec,liczba_minut_w_tygodniu, mozliwe_sale, Kurs_id, odpowiedzialny_nauczyciel_id) VALUES(?,?,?,?,?)",
                  ('kurs_'+kurs+'zajecia_'+char, dlugosc_zajec[randint(0, 7)], " ", kurs_id, prowadzacy_id))
    conn.commit()