from urllib.request import Request, urlopen
import psycopg2
import bs4 as soup
import matplotlib.pyplot as plt
import time



# Parser logic with usage of BS4
# We need to specify "User-Agent" and change our code a little bit to avoid 403 forbiden error
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}

url = (input('Provide URL Scraper Will Work With: '))

req = Request(url, headers=headers)
req_url = urlopen(req).read()
bs = soup.BeautifulSoup(req_url, features="lxml")
table = bs.find('table')
table_rows = table.findAll('tr')

Encrypt_data_trigger = ''
Insert_to_db_trigger = input('Upload Scraped Data To Your PostgreSQL data base? [y/n]: ')
if Insert_to_db_trigger == 'y' or Insert_to_db_trigger == 'n':
    pass
else:
    print("\n\nYou Didn't Choose Anything From Offered Options [Data Won't Be Stored] In PostgreSQL db\n"
          "If You Need To Upload Data To PostgreSQL Rerun Program and Choose 'y'\n\n")
    time.sleep(9)

#PostgreSQL
if Insert_to_db_trigger == 'y':
    Encrypt_data_trigger = (input('Do You Want To Encrypt Data? [y/n]: '))
    if Encrypt_data_trigger != 'y' and Encrypt_data_trigger != 'n':
        print("\n\nYou Didn't Choose Anything From Offered Options Data [Won't Be Encrypted] In PostgreSQL db\n"
              "If You Need To Encrypt Data To PostgreSQL Rerun Program and Choose 'y'\n\n")
        time.sleep(9)
    """ CHANGE host dbname user password to YOURS"""
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=admin") #[!!!]
    cur = conn.cursor()
else:
    pass


#Prepare Pie chart Variables
x = 0           # X - empty strings, people without degree
z = 0           # Sum of people with and without degree


print_row_trigger = input("do you want me to print output? [y/n]: ")


#For loop
for tr in table_rows:
    td = tr.findAll('td')
    row = [i.text for i in td]

    #Skip not needed data to fetch in db data we need without header data
    if row == [] or row == ['Full Name', 'Email', 'Gender', 'Highest Degree Earned', 'University/ School'] or row == ['', '', '', '', '']:
        continue
    #Logic for pie chart
    if row[3] == '':
        x = x + 1
    if row[3] is not None:
        z = z + 1

    #Insert parsed data to PostgreSQL (our db)
    if Insert_to_db_trigger == 'y' and Encrypt_data_trigger == 'y':
        cur.execute("INSERT INTO parser VALUES\
                (PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text)", row)                    #[!!!]
    if Insert_to_db_trigger == 'y' and Encrypt_data_trigger != 'y':
        cur.execute("INSERT INTO parser VALUES (%s, %s, %s, %s, %s)", row)   #[!!!]
    else:
        pass



    if print_row_trigger == 'y':
        print(row)
    else:
        pass

if Insert_to_db_trigger == 'y':
    conn.commit()
else:
    pass



""" Pie chart that will be automatically created and opened after we run our program """

y = z - x    # Z is all inputs into system, when x is people without degree. Simple mathematics. Z - X = Y
labels = 'People Without Degree', 'People With Degree'
sizes = [x, y]
colors = ['orange', 'brown']
explode = (0.3, 0)


plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct=lambda p : '{:.2f}%  ({:,.0f})'.format(p,p * sum(sizes)/100), shadow=True, startangle=140) #From % to numbers
plt.axis('equal')
plt.show()


if Insert_to_db_trigger == 'y':
    print("\nData is [Stored] In PostgreSQL db")
else:
    print("\nData is [Not Stored] In PostgreSQL db")
    time.sleep(2)
if Encrypt_data_trigger == 'y':
    print("Data is [Encrypted] In PostgreSQL db")
else:
    print("Data is [Not Encrypted] In PostgreSQL db")
    time.sleep(2)
