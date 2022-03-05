from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacancies = db.vacancies

base_url = "https://hh.ru"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
params = {'search_field': 'name',
          'clusters': 'true',
          'ored_clusters': 'true',
          'enable_snippets': 'true'}


def get_vacancies(vacancy, page_cnt):
    params['text'] = vacancy

    for i in range(page_cnt):
        params['page'] = i
        response = requests.get(f'{base_url}/search/vacancy', headers=headers, params=params)
        dom = BeautifulSoup(response.text, 'html.parser')

        hh_vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

        for v in hh_vacancies:
            vacancy = {}
            info = v.find('a', {'class': 'bloko-link'})

            vacancy['name'] = info.getText()
            vacancy['link'] = info['href']
            vacancy['site'] = base_url

            salary = v.find('span', {'class': 'bloko-header-section-3'})
            if salary is not None:
                vacancy['salary'] = {}

                salary = salary.getText()
                sal_list = re.findall(r'\d+', "".join(salary.split()))

                amount_from = None
                amount_to = None
                if len(sal_list) == 2:
                    amount_from = int(sal_list[0])
                    amount_to = int(sal_list[1])
                else:
                    if salary.startswith('от'):
                        amount_from = int(sal_list[0])
                    elif salary.startswith('до'):
                        amount_to = int(sal_list[0])
                currency = salary[salary.rfind(' '):]

                vacancy['salary']['amount_from'] = amount_from
                vacancy['salary']['amount_to'] = amount_to
                vacancy['salary']['currency'] = currency

            if not vacancies.find_one({'link': vacancy['link']}):
                vacancies.insert_one(vacancy)


if __name__ == '__main__':
    vacancy = input("Enter vacancy: ")
    page_cnt = int(input("Enter page count: "))
    get_vacancies(vacancy, page_cnt)
