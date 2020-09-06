from bs4 import BeautifulSoup
import urllib.request
import re
import textwrap

url = "https://2020.pycon.org.au/program/sun/#rube-codeberg-competition"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    text = response.read()

m = None
soup = BeautifulSoup(text, 'html.parser')
quoted = re.compile('"[^"]*"')
for p in soup.find_all('p'):
    for c in p.children:
        if "on the screen" in str(c):
            s = c.previous_sibling.string
            for value in quoted.findall(s):
                m = value
                break

open('error.py', 'w').write(
    textwrap.dedent(
        f'''
            class MyException(ZeroDivisionError):
               def __str__(self):
                 return {m}
        '''
    )
)

from error import MyException

class MyClass(int):
    def __init__(self, i):
        self.i = i

    def __floordiv__(self, b):
        if b == 0:
            raise MyException
        else:
            return super().__floordiv__(b)

i = MyClass(0)

i // 0

