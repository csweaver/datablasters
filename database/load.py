from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from build import Food, FoodTag, Menu, MenuRating, Allergen
import os
import re
import csv
import datetime

database = {
    'user': os.environ['DB_USERNAME'],
    'pass': os.environ['DB_PASSWORD'],
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port':  os.environ.get('DB_PORT', 5433),
    'database': os.environ.get('DB_DATABASE', 'datablaster')
}
engine = create_engine(
    "postgresql://{user}:{pass}@{host}:{port}/{database}".format(**database))
Base = declarative_base()
# Load Data
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CONTINENT = {
    "Vietnamese": "asia",
    "Cajun": "usa",
    "German": "europe",
    "Bistro": "europe",
    "Cuban": "panamerica",
    "West Texas BBQ": "usa",
    "Spanish": "europe",
    "Farm to Table": "usa",
    "Hawaiian Poke": "asia",
    "American Classics": "usa",
    "Indian": "asia",
    "Brazilian": "panamerica",
    "Korean": "asia",
    "French": "europe",
    "Thai": "asia",
    "Scandinavian": "europe",
    "SF Classics": "usa",
    "Oaxcan": "panamerica",
    "Super Bowl BBQ": "usa",
    "Peruvian": "panamerica",
    "Lunar New Year": "asia",
    "Basque": "europe",
    "Greek": "europe",
    "Tuscan": "europe"
}

months = {
    "January": "01",
    "February": "02",
}

menu_regex = re.compile("(\w+) - (\w+) (\d+) - (.+)")
food_regex = re.compile("(.*) ((\(\w+\))*)")

menu_id = None
with open("../2019_menu.txt") as fh:
    for i in fh:
        line = i.strip()

        # ignore empty lines
        if line == "":
            continue
        menu_result = menu_regex.findall(line)
        if menu_result:
            date = f"{months[menu_result[0][1]]}/{menu_result[0][2]}/2019"
            theme = menu_result[0][3]
            continent = CONTINENT[theme]
            new_menu = Menu(date=date, theme=theme, continent=continent)
            session.add(new_menu)
            session.flush()
            session.refresh(new_menu)
            menu_id = new_menu.id
        else:

            food_result = food_regex.findall(line)
            if menu_id:
                food = food_result[0][0]
                allergen_string = food_result[0][1]
                new_food = Food(menu_id=menu_id, item=food, allergen_string=allergen_string)
                session.add(new_food)


with open("../feedback_601.csv") as fh:
    csv_reader = csv.reader(fh)
    next(csv_reader)
    for line in csv_reader:
        d = line[2]
        date = datetime.datetime.strptime(d, "%d/%m/%Y").date()
        n_scores = line[17]
        score_1 = line[9]
        score_2 = line[11]
        score_3 = line[13]
        score_4 = line[15]
        new_score = MenuRating(date=date, n_scores=n_scores, score_1=score_1, score_2=score_2, score_3=score_3, score_4=score_4)
        session.add(new_score)

with open("../allergens.txt") as fh:
    for i in fh:
        line = i.strip()
        name, code = line.split("(")
        new_allergen = Allergen(code=f"({code}", name=name)
        session.add(new_allergen)

session.commit()

