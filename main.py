from bs4 import BeautifulSoup
import requests

# hardcore html content load
# html_content = ''' snippet '''
url = 'https://podzial.mech.pk.edu.pl/stacjonarne/html/plany/o7.html'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'tabela'})

    # skip first two headers ('Nr', 'Godz')
    headers = [header.get_text() for header in table.find_all('th')[2:]]

    rows = table.find_all('tr')[1:]  # Skip the first header row

    timetable = {day: [] for day in headers}
    for row in rows:
        cells = row.find_all('td')
        period = cells[0].get_text()
        time = cells[1].get_text()

        for i, day in enumerate(headers):
            timetable[day].append({
                'period': period,
                'time': time,
                'class': cells[i + 2].get_text(strip=True) # i+2 because first subject cell starts from 3 column
            })

    with open('timetable.txt', 'w', encoding='utf-8') as f:
        for day, schedule in timetable.items():
            f.write(f"{day}:\n")
            for entry in schedule:
                f.write(f"Period: {entry['period']} Time: {entry['time']}: Class: {entry['class']}\n")
            f.write("\n")
    print("Schedule has been successfully written to timetable.txt!")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

