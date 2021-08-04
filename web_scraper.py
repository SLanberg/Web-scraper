from urllib.request import Request, urlopen
import bs4 as soup
import matplotlib.pyplot as plt
import psycopg2
import time


"""
Parser logic with usage of BS4
We need to specify "User-Agent" and change our code
a little bit to avoid 403 forbiden error
so we will imitate user request from browser.
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}


# example: url = 'file:///home/sun/Desktop/Project/web_scraper/Sheet1.html'
url = (input('Provide URL Scraper Will Work With: '))


request_with_parameters = Request(url, headers=headers)
read_url = urlopen(request_with_parameters).read()
bs = soup.BeautifulSoup(read_url, features="lxml")
table = bs.find('table')
table_rows = table.findAll('tr')


Insert_to_db_trigger = input(
    'Upload Scraped Data To Your PostgreSQL data base? [y/n]: ')
if Insert_to_db_trigger != 'y' and Insert_to_db_trigger != 'n':
    print("""
    You Didn't Choose Anything From Offered Options
    [Data Won't Be Stored] In PostgreSQL db
    If You Need To Upload Data To PostgreSQL Rerun
    Program and Choose 'y'
    """)
    time.sleep(9)


# PostgreSQL
if Insert_to_db_trigger == 'y':
    Encrypt_data_trigger = (input('Do You Want To Encrypt Data? [y/n]: '))
    if Encrypt_data_trigger != 'y' and Encrypt_data_trigger != 'n':
        print("""
        You Didn't Choose Anything From Offered Options Data
        [Won't Be Encrypted] In PostgreSQL db\n
        If You Need To Encrypt Data To PostgreSQL Rerun
        Program and Choose 'y'
        """)
        time.sleep(9)

    """ CHANGE host dbname user password to YOURS"""
    conn = psycopg2.connect(
        "host=localhost dbname=development user=postgres password=postgres")
    cur = conn.cursor()
else:
    pass


def create_db_if_not_exists():
    cur.execute("CREATE TABLE IF NOT EXISTS parser  ( \
                name text,                            \
                email text,                           \
                gender text,                          \
                degree text,                          \
                university text)")
    cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")


print_row_trigger = input("do you want me to print output? [y/n]: ")

# Prepare Pie chart Variables
contendant_without_degree = 0       # Empty strings - people without degree
overall_number_of_contendants = 0   # Sum of people with and without degree

# For loop
for tr in table_rows:
    td = tr.findAll('td')
    row = [i.text for i in td]

    # Skip not needed data to fetch in db data we need without header data
    if row == [] or row == ['Full Name', 'Email', 'Gender', 'Highest Degree Earned', 'University/ School'] or row == ['', '', '', '', '']:
        continue
    # Logic for pie chart
    if row[3] == '':
        contendant_without_degree += 1
    if row[3] is not None:
        overall_number_of_contendants += 1

    # Insert parsed data to PostgreSQL (our db)
    if Encrypt_data_trigger == 'y':
        create_db_if_not_exists()

        cur.execute("INSERT INTO parser VALUES\
                (PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text,\
                 PGP_SYM_ENCRYPT(%s, 'key')::text)", row)  # [!!!]
    if Insert_to_db_trigger == 'y' and Encrypt_data_trigger != 'y':
        create_db_if_not_exists()

        cur.execute(
            "INSERT INTO parser VALUES (%s, %s, %s, %s, %s)", row)  # [!!!]
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


""" Pie chart that will be automatically opened after we run our program """
contendant_with_degree = overall_number_of_contendants - contendant_without_degree
labels = 'People Without Degree', 'People With Degree'
sizes = [contendant_without_degree, contendant_with_degree]
colors = ['orange', 'brown']
explode = (0.3, 0)


plt.pie(sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct=lambda p: '{:.2f}%  ({:,.0f})'.format(p, p * sum(sizes) / 100),
        shadow=True,
        startangle=140)
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
