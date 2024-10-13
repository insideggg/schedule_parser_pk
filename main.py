from bs4 import BeautifulSoup
import requests

# hardcore html content load
# html_content = ''' snippet '''
url = 'https://podzial.mech.pk.edu.pl/stacjonarne/html/plany/o7.html'

response = requests.get(url)

# use scripts directly to filter the 'timetable' list
def delete_unnecessary_stuff(class_info):
    unnecessary_symbols = ["L05", "L01", "K01", "(K)"]
    exceptional_symbols = ["L02", "K02"]

    # deleting elements which including unnecessary elements / leave only those that are needed
    if any(symbol in class_info for symbol in unnecessary_symbols):
        if any(symbol in class_info for symbol in exceptional_symbols):
            pass
        else:
            class_info = ""

    return class_info


def get_timetable():
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'class': 'tabela'})

        # skip first two headers ('Nr', 'Godz')
        headers = [header.get_text() for header in table.find_all('th')[2:]]

        rows = table.find_all('tr')[1:]  # Skip the first header row and start reading from "1. 7:30-8:15..."

        timetable = {day: [] for day in headers}
        for row in rows:
            cells = row.find_all('td')
            period = cells[0].get_text()
            time = cells[1].get_text()

            for i, day in enumerate(headers):
                # i+2 because first subject cell starts from 3 column
                class_info = cells[i + 2].get_text(strip=True)

                class_name_N = ''
                class_name_P = ''

                # there is bug if -p comes first
                if "-n" in class_info and "-p" in class_info:
                    class_parts = class_info.split("-n", 1)
                    class_name_N = class_parts[0] + "-n"
                    class_name_P = class_parts[1].split("-p", 1)[0] + "-p" if "-p" in class_parts[1] else ''
                elif "-n" in class_info and "-p" not in class_info:
                    # lesson is only in (N) week
                    class_name_N = class_info
                elif "-n" not in class_info and "-p" in class_info:
                    # lesson is only in (P) week
                    class_name_P = class_info
                elif "-n" not in class_info and "-p" not in class_info:
                    class_name_N = class_info
                    class_name_P = class_info

                # simplify to make it possible read from android app
                timetable[day].append([period, time, class_name_N, class_name_P])

                # timetable[day].append({
                #     'period': period,
                #     'time': time,
                #     'class_name_N': class_name_N.strip(),
                #     'class_name_P': class_name_P.strip()  # if class_name_P else class_name_N.strip()
                # })

        return timetable
        # with open('timetable.txt', 'w', encoding='utf-8') as f:
        #     for day, schedule in timetable.items():
        #         f.write(f"{day}:\n")
        #         for entry in schedule:
        #             f.write(f"Period: {entry['period']} Time: {entry['time']}: Class (N): {entry['class_name_N']} Class (P): {entry['class_name_P']}\n")
        #         f.write("\n")
        # print("Schedule has been successfully written to timetable.txt!")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return 0

print(get_timetable())

