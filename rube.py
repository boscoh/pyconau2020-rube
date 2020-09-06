from bs4 import BeautifulSoup
import urllib.request
import re
import textwrap

url = "https://2020.pycon.org.au/program/sun/#rube-codeberg-competition"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    text = response.read()

m = {}
soup = BeautifulSoup(text, 'html.parser')
quoted = re.compile('"[^"]*"')
for p in soup.find_all('p'):
    for c in p.children:
        if "on the screen" in str(c):
            s = c.previous_sibling.string
            for value in quoted.findall(s):
                m["jackpot"] = value
                break

open('error.py', 'w').write(
    textwrap.dedent(
        f'''
            class MyZeroDivisionError(ZeroDivisionError):
               def __str__(self):
                 return %(jackpot)s
        ''' % m
    )
)


from error import MyZeroDivisionError

class MyInt(int):
    def __floordiv__(self, b):
        if b == 0:
            raise MyZeroDivisionError
        else:
            return super().__floordiv__(b)

one = MyInt(1)

one // 0


