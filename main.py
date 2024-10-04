from bs4 import BeautifulSoup
import requests

# hardcore html content load
# html_content = ''' snippet '''
url = 'https://podzial.mech.pk.edu.pl/stacjonarne/html/plany/o7.html'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'tabela'})

    headers = [header.get_text() for header in table.find_all('th')]

    rows = table.find_all('tr')[1:]  # Skip the first header row

    timetable = []
    for row in rows:
        cells = row.find_all('td')
        period_info = {
            'period': cells[0].get_text(),
            'time': cells[1].get_text(),
            'classes': [cell.get_text(strip=True) for cell in cells[2:]]  # MOnday to Friday
        }
        timetable.append(period_info)

    for period in timetable:
        print(f"Period {period['period']} ({period['time']}):")
        for i, cls, in enumerate(period['classes']):
            print(f"{headers[i + 2]}: {cls}")  # headers correspond to days of the week
        print()
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

