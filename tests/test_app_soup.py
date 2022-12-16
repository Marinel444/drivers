from bs4 import BeautifulSoup
import requests


def get_soup(url):
    s = requests.Session()
    response = s.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def test_table():
    soup = get_soup(url='http://localhost:5000/report')
    table = soup.find('table', class_='table table-striped').find('tbody')
    assert table.text.strip() == r"""1
SVF
Sebastian Vettel
FERRARI
0:01:04.415000"""


def test_table_desc():
    soup = get_soup(url='http://localhost:5000/report?order=desc')
    table = soup.find('table', class_='table table-striped').find('tbody')
    print(table.text.strip())
    assert table.text.strip() == r"""19
LHM
Lewis Hamilton
MERCEDES
0:06:47.540000"""


def test_drivers():
    soup = get_soup(url='http://localhost:5000/drivers')
    table = soup.find('div', class_='card-body').find('table', class_='table table-striped').find('tbody')
    print(table.text.strip())
    assert table.text.strip() == r'''SVF
Sebastian Vettel
FERRARI'''


def test_driver_url():
    soup = get_soup(url='http://localhost:5000/drivers/SVF')
    card = soup.find('div', class_='card')
    name = card.find('div', class_='card-body')
    driver_id, team = card.find(class_='list-group list-group-flush').find_all(class_='list-group-item')
    assert name.text.strip() == 'Sebastian Vettel'
    assert driver_id.text.strip() == 'ID: SVF'
    assert team.text.strip() == 'Team: FERRARI'
