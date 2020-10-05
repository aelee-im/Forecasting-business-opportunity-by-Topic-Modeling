import sqlite3
from bs4 import BeautifulSoup
import requests
import time

conn = sqlite3.connect('test.sqlite3')

for patent in conn.execute('select id from gp_search_new'):

    patent = patent[0]
    url = conn.execute('select url from gp_search_new where id = ?', (patent,)).fetchone()[0]
    print(url)
    if type(url) is str and 'https' in url:
        try:
            website = requests.get(url)
        except requests.exceptions.ConnectionError:
            status_code = "Connection refused"
        print(website.status_code)
        soup = BeautifulSoup(website.content, 'html.parser')
        full_text = ' '
        for i in ["%04d" % x for x in range(1, 1000)]:
            try:
                part = soup.find(id='p-' + i).text
                full_text += ' ' + part
            except Exception as e:
                print(e)
                break

        print(full_text)
        conn.execute('replace into gp_search_new(id,full_text) values(?,?)',(patent,full_text,))
        conn.commit()
        time.sleep(5)
