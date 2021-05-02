import sqlite3

def create_data_schema():
    conn = sqlite3.connect('database.db')  # You can create a new database by changing the name within the quotes
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

    # Create table - CLIENTS
    c.execute('''CREATE TABLE RATING
                ([rating_id] INTEGER PRIMARY KEY,
                [enterprise] text,
                [title] text,
                [complain_body] text,
                [position_in_chat] integer,
                [link] text,
                [collect_date] text
                [category] text
                [subcategory] text
                [subcategory_id] text)''')
            
    # Create table - COUNTRY
    c.execute('''CREATE TABLE RANKING
                ([ranking_id] INTEGER PRIMARY KEY,
                [category] text,
                [enterprise] text,
                [percentage] text,
                [position] integer,
                [week] text,
                [collect_date] text)''')
            
    conn.commit()

def create_category_table():
    conn = sqlite3.connect('database.db')  # You can create a new database by changing the name within the quotes
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

    # Create table - CLIENTS
    c.execute('''CREATE TABLE CATEGORY
                ([category_id] INTEGER PRIMARY KEY,
                [name] text,
                [code] text,
                [super_category] text,
                [enterprise] text,
                [link] text,
                [is_super_category] 
                [collect_date] text)''')

    conn.commit()

def insert_in_ranking(conn, ranking):
    sql = ''' INSERT INTO RANKING(category, enterprise, percentage, position, week, collect_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, ranking)
    conn.commit()
    return cur.lastrowid

def insert_in_rating(conn, rating):
    sql = ''' INSERT INTO RATING(enterprise, title, complain_body, position_in_chat, link, category, subcategory, subcategory_id, collect_date)
              VALUES(?,?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, rating)
    conn.commit()
    return cur.lastrowid

def insert_in_category(conn, category):
    sql = ''' INSERT INTO CATEGORY(name, super_category, code, link, enterprise, is_super_category, collect_date)
              VALUES(?,?,?,?,?,?,?) '''
              
    cur = conn.cursor()
    cur.execute(sql, category)
    conn.commit()
    return cur.lastrowid

def get_reviews_categories(conn, enterprise):
    sql = ''' SELECT name, super_category, code from CATEGORY where enterprise = '{}' and is_super_category=0 '''.format(enterprise)
    
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    return rows

# https://www.sqlitetutorial.net/sqlite-python/insert/
# https://datatofish.com/create-database-python-using-sqlite3/