from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacancies = db.vacancies


def find_vacancies(zp):
    for doc in vacancies.find({'$or': [{'salary.amount_from': {'$gt': zp}}, {'salary.amount_to': {'$gt': zp}}]}):
        pprint(doc)


if __name__ == '__main__':
    sal = int(input("Enter salary: "))
    find_vacancies(sal)
