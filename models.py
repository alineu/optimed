from app import db
from sqlalchemy.dialects.postgresql import JSON
from functools import reduce

class OptiMedResult(db.Model):
    __tablename__ = 'optimed_results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    all_drugs = db.Column(JSON)
    print("jiji")
    print(all_drugs)
    def __init__(self, url, all_drugs):
        self.url = url
        self.all_drugs = all_drugs

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Result(db.Model):
    __tablename__ = 'results'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


# class DrugSearchResult(db.Model):
#     __tablename__ = 'drugs'
#     __table_args__ = {'extend_existing': True}

#     condition = db.Column(db.String(), primary_key=True)
#     drug = db.Column(db.String())
#     count = db.Column(db.Integer)
#     avg_rating = db.Column(db.Float)
#     avg_sentiment = db.Column(db.Float)
#     avg_usefulCount = db.Column(db.Float) 
#     accum_score = db.Column(db.Float)    

#     def __init__(self, condition, drug, count, 
#         avg_rating, avg_sentiment, avg_usefulCount, accum_score):

#         self.condition = condition
#         self.drug = drug
#         self.count = count
#         self.avg_rating = avg_rating
#         self.avg_sentiment = avg_sentiment
#         self.avg_usefulCount = avg_usefulCount
#         self.accum_score = accum_score


#     def __repr__(self):
#         return '<index {}>'.format(self.index)

# class PharmacyLocations(db.Model):
#     __tablename__ = 'pharmacies_latlon'

#     BUYER_DEA_NO = db.Column(db.String(), primary_key=True)
#     BUYER_STATE = db.Column(db.String())
#     BUYER_COUNTY = db.Column(db.String())
#     lat = db.Column(db.String())
#     lon = db.Column(db.String()) 


#     def __init__(self, BUYER_DEA_NO, BUYER_STATE, BUYER_COUNTY, lat, lon):

#         self.BUYER_DEA_NO = BUYER_DEA_NO
#         self.BUYER_STATE = BUYER_STATE
#         self.BUYER_COUNTY = BUYER_COUNTY
#         self.lat = lat
#         self.lon = lon

#     def __repr__(self):
#         return '<index {}>'.format(self.BUYER_DEA_NO)

# class PharmacyDetails(db.Model):
#     __tablename__ = 'pharmacies_detail'

#     BUYER_DEA_NO = db.Column(db.String(), primary_key=True)
#     BUYER_BUS_ACT = db.Column(db.String())
#     BUYER_NAME = db.Column(db.String())
#     BUYER_ADDL_CO_INFO = db.Column(db.String())
#     BUYER_ADDRESS1 = db.Column(db.String())
#     BUYER_ADDRESS2 = db.Column(db.String())
#     BUYER_CITY = db.Column(db.String())
#     BUYER_STATE = db.Column(db.String())
#     BUYER_ZIP = db.Column(db.String())
#     BUYER_COUNTY = db.Column(db.String())


#     def __init__(self, BUYER_DEA_NO, BUYER_BUS_ACT, BUYER_NAME, 
#         BUYER_ADDL_CO_INFO, BUYER_ADDRESS1, BUYER_ADDRESS2, 
#         BUYER_CITY, BUYER_STATE, BUYER_ZIP, BUYER_COUNTY):

#         self.BUYER_DEA_NO = BUYER_DEA_NO
#         self.BUYER_BUS_ACT = BUYER_BUS_ACT
#         self.BUYER_NAME = BUYER_NAME
#         self.BUYER_ADDL_CO_INFO = BUYER_ADDL_CO_INFO
#         self.BUYER_ADDRESS1 = BUYER_ADDRESS1
#         self.BUYER_ADDRESS2 = BUYER_ADDRESS2
#         self.BUYER_CITY = BUYER_CITY
#         self.BUYER_STATE = BUYER_STATE
#         self.BUYER_ZIP = BUYER_ZIP
#         self.BUYER_COUNTY = BUYER_COUNTY

#     def __repr__(self):
#         return '<index {}>'.format(self.BUYER_DEA_NO)


class BaseScorer(object):

    def __init__(self):
        self._next_scorer = None

    def set_next(self, scorer):
        self._next_scorer = scorer

        return scorer

    def _call_next(self, case, score):

        if self._next_scorer is None:
            return score

        return self._next_scorer.score(case, score)

    def score(self, case, score=0):
        raise NotImplementedError

    @staticmethod
    def chain(scorers):
        reduce(lambda x, y: x.set_next(y), scorers)

        return scorers[0]

class RatingScorer(BaseScorer):

    def score(self, case, score=0, threshold=5):

        if case.rating > threshold:
            score += case.rating

        return self._call_next(case, score)


class SentimentScorer(BaseScorer):

    def score(self, case, score=0, threshold=0.5):

        if case.sentiment > threshold:
            score += case.sentiment

        return self._call_next(case, score)


class PopularityScorer(BaseScorer):

    def score(self, case, score=0):

        if case.count != 0:
            score += log(case.count)

        return self._call_next(case, score)
