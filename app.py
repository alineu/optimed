import os
import requests
import operator
import re
import nltk
import json
from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
from bs4 import BeautifulSoup, SoupStrainer
import difflib
from sqlalchemy import desc
from stop_words import stops as stop_words
# from nltk.corpus import stopwords
#stop_words = stopwords.words('english')
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
from models import OptiMedResult
db.create_all()
Base = db.Model.metadata.reflect(db.engine)
conditions_table = db.Model.metadata.tables['drugs']
pharmacies_latlon = db.Model.metadata.tables['pharmacies_latlon']
pharmacies_detail = db.Model.metadata.tables['pharmacies_detail']
# from utils.app_utils import *

q = Queue(connection=conn)


def find_matching_condition(user_condition, threshold=0.5):
    unique_conditions = [str(condition[0]).lower().strip() for condition in db.session.query(
        conditions_table.c.condition).group_by(conditions_table.c.condition).all()]
    difflib_similarity_score = []
    user_condition = re.sub('[^a-zA-Z]', ' ', user_condition)
    user_conditions = [x.strip() if x not in stop_words else '' for x in user_condition.lower().split()]
    try:
        user_conditions = list(filter(('').__ne__, user_conditions))
    except ValueError as e:
        pass
    for condition in unique_conditions:
        condition = re.sub('[^a-zA-Z]', ' ', condition)
        conditions = [x.strip() if x not in stop_words else '' for x in condition.lower().split()]
        try:
            conditions.remove('')
        except ValueError as e:
            pass
        scores = []
        for db_cond in conditions:
            for user_cond in user_conditions:
                scores.append(difflib.SequenceMatcher(None, user_cond, db_cond).ratio())  
        if max(scores)>threshold:
            if len(scores)>1:
                score = sum(sorted(scores)[-2:])/2.0
            else:
                score=max(scores)
        else:
            score = 0
        difflib_similarity_score.append([score, condition])
    scores = sorted(difflib_similarity_score, key=lambda x: -x[0])[:5] 
    return scores

def find_matching_drugs(identified_condition):
    drug_candidates = [' '.join([str(drug[i]) for i in range(1,3)]) for drug in db.session.query(conditions_table.c.condition, conditions_table.c.drug, conditions_table.c.accum_score)
    .filter(conditions_table.c.condition == identified_condition)
    .order_by(desc(conditions_table.c.accum_score))[:5]]
    return drug_candidates

def find_drug_price_wellrx(drug, zipcode='02115', first_try=True):
    
    url = f"https://www.wellrx.com/prescriptions/{drug}/{zipcode}"
    r = requests.get(url)
    soup_1 = BeautifulSoup(r.text, 'html.parser', parse_only=SoupStrainer('span'))
    prices = [re.sub(r"[^0-9\.]","",i.text) for i in soup_1.find_all('span', attrs={'class':'price price-large'})]
    if prices[0]=='':
        if first_try and '-' in drug:
            drug = '-'.join(drug.split('-')[::-1])
            return find_drug_price_wellrx(drug, zipcode=zipcode, first_try=False)
        pass
    soup_2 = BeautifulSoup(r.text, 'html.parser', parse_only=SoupStrainer('p'))
    pharmacy_names = [i.text for i in soup_2.find_all('p', attrs={'class': 'list-title'})]
    # pharmacy_names = [i.text for i in soup_2.find_all('p', attrs={'id': 'multipharm-loc-key', 'class': 'list-title'})]
    # soup_3 = BeautifulSoup(r.text, 'html.parser', parse_only=SoupStrainer('p'))
    # pharmacy_names = [i.text for i in soup_2.find_all('p', attrs={'id': 'singlepharm-name', 'class': 'list-title'})]
    # return dict(zip(pharmacy_names, prices))
    return prices

def get_winner_drugs(user_condition, num_retries=10, zipcode='02115'):
    results_dict = {}
    for attempt_no in range(num_retries):
        identified_condition = find_matching_condition(user_condition)[0]
        condition = identified_condition[1]
        try:
            drug = find_matching_drugs(condition)[attempt_no].split()[:-1]
            price = find_drug_price_wellrx(drug[0], zipcode=zipcode)[0]
            results_dict[drug[0]] = float(price)

        except IndexError as e:
            pass
    return results_dict
    # print(results_dict)
    # r = list(map(lambda x: json.dumps(x), results_dict))
    # # results_dict = json.loads(r)
    # print(results_dict)
    # json_object = json.dumps(results_dict, indent = 4) 
    # return json_object


# conn = db.session.connection()
# curs = conn.connection.cursor()
# curs.execute("ROLLBACK")
# conn.commit()

        # return drug_candidates
        # except IndexError as error:
        #     if attempt_no < (num_retries - 1):
        #         pass
        #     else:
        #         raise error


def find_meds(user_condition):
    
    all_drugs = get_winner_drugs(user_condition)
    print(all_drugs)
    errors = []
    try:

        result = OptiMedResult(
            url=user_condition,
            all_drugs=all_drugs
            # ,all_prices=all_prices
        )
        print('adding')
        db.session.add(result)
        print('commiting!')
        db.session.commit()
        print('doen!')
        print(result.id)
        return result.id
    except:
        errors.append("Unable to add the item to database.")
        return {"error": errors}

# def count_and_save_words(url):

#     errors = []

#     try:
#         r = requests.get(url)
#     except:
#         errors.append(
#             "Unable to get URL. Please make sure it's valid and try again."
#         )
#         return {"error": errors}

#     # text processing
#     raw = BeautifulSoup(r.text, 'html.parser').get_text()
#     nltk.data.path.append('./nltk_data/')  # set the path
#     tokens = nltk.word_tokenize(raw)
#     text = nltk.Text(tokens)

#     # remove punctuation, count raw words
#     nonPunct = re.compile('.*[A-Za-z].*')
#     raw_words = [w for w in text if nonPunct.match(w)]
#     raw_word_count = Counter(raw_words)

#     # stop words
#     no_stop_words = [w for w in raw_words if w.lower() not in stops]
#     no_stop_words_count = Counter(no_stop_words)

#     # save the results
#     try:
#         result = Result(
#             url=url,
#             result_all=raw_word_count,
#             result_no_stop_words=no_stop_words_count
#         )
#         db.session.add(result)
#         db.session.commit()
#         return result.id
#     except:
#         errors.append("Unable to add item to database.")
#         return {"error": errors}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    #return render_template('main.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    # return render_template('index.html')
    return render_template('about.html')

@app.route('/start', methods=['POST'])
def get_counts():
    # get url
    data = json.loads(request.data.decode())
    print(data)
    url = data["url"]
    # start job
    job = q.enqueue_call(
        func=find_meds, args=(url,), result_ttl=5000
    )
    # return created job id
    print(url)
    print('abolfazal')

    print(job.get_id())
    return job.get_id()

@app.route('/print')
def printMsg():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return "Check your console"
# @app.route('/findmed', methods=['POST'])
# def find_meds():
#     # get url
#     data = json.loads(request.data.decode())
#     user_condition = data["user_condition"]
    
#     # start job
#     job = q.enqueue_call(
#         func=get_winner_drugs, args=(user_condition,), result_ttl=2500
#     )
#     # return created job id
#     return job.get_id()


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        print('miaumiau')

        result = OptiMedResult.query.filter_by(id=job.result).first()
        print(result)
        # results = sorted(
        #     result.all_drugs.items(),
        #     key=operator.itemgetter(1),
        #     reverse=True
        # )[:3]
        # results = sorted(result.all_drugs.items())
        results = result.all_drugs
        print(results)
        return jsonify(results)
    else:
        return "Nay!", 202


if __name__ == '__main__':
    app.run(debug=True)
