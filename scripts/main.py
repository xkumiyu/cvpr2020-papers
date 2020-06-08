import lxml.html
import pandas as pd
import requests

URL = "http://cvpr2020.thecvf.com/program/main-conference"


def get_data_from_table(table):
    data = []
    session = table.getprevious().text_content().replace("Session: ", "")
    for tr in table.findall("tbody/tr"):
        row = [td.text for td in tr.findall("td")]
        if len(row) == 6:
            data.append(
                {
                    "Paper ID": row[5],
                    "Paper Title": row[3],
                    "Author(s)": row[4],
                    "Session": session,
                    "Oral" : session[:4] == "Oral"
                }
            )
    return data


def main():
    res = requests.get(URL)
    html = lxml.html.fromstring(res.text)

    data = []
    for table in html.xpath("//table"):
        data += get_data_from_table(table)

    df = pd.DataFrame(data).set_index("Paper ID")
    df.to_csv("papers.csv")


if __name__ == "__main__":
    main()
