from app import db
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
    __tablename__ = 'results'

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

class DrugSearchResult(db.Model):
    __tablename__ = 'drugs'

    index = db.Column(db.Integer, primary_key=True)
    drugName = db.Column(db.String())
    condition = db.Column(db.String())
    rating = db.Column(db.Integer)
    usefulCount = db.Column(db.Integer)
    sentiment = db.Column(db.Integer)
    weighted_by_count_rating = db.Column(db.Integer)    


    def __init__(self, index, drugName, condition, rating, 
        usefulCount, sentiment, weighted_by_count_rating):

        self.index = index
        self.drugName = drugName
        self.condition = condition
        self.rating = rating
        self.usefulCount = usefulCount
        self.sentiment = sentiment
        self.weighted_by_count_rating = weighted_by_count_rating

    def __repr__(self):
        return '<index {}>'.format(self.index)

class PharmacyLocations(db.Model):
    __tablename__ = 'pharmacies_latlon'

    BUYER_DEA_NO = db.Column(db.String(), primary_key=True)
    BUYER_STATE = db.Column(db.String())
    BUYER_COUNTY = db.Column(db.String())
    lat = db.Column(db.String())
    lon = db.Column(db.String()) 


    def __init__(self, BUYER_DEA_NO, BUYER_STATE, BUYER_COUNTY, lat, lon):

        self.BUYER_DEA_NO = BUYER_DEA_NO
        self.BUYER_STATE = BUYER_STATE
        self.BUYER_COUNTY = BUYER_COUNTY
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<index {}>'.format(self.BUYER_DEA_NO)

class PharmacyDetails(db.Model):
    __tablename__ = 'pharmacies_detail'

    BUYER_DEA_NO = db.Column(db.String(), primary_key=True)
    BUYER_BUS_ACT = db.Column(db.String())
    BUYER_NAME = db.Column(db.String())
    BUYER_ADDL_CO_INFO = db.Column(db.String())
    BUYER_ADDRESS1 = db.Column(db.String())
    BUYER_ADDRESS2 = db.Column(db.String())
    BUYER_CITY = db.Column(db.String())
    BUYER_STATE = db.Column(db.String())
    BUYER_ZIP = db.Column(db.String())
    BUYER_COUNTY = db.Column(db.String())


    def __init__(self, BUYER_DEA_NO, BUYER_BUS_ACT, BUYER_NAME, 
        BUYER_ADDL_CO_INFO, BUYER_ADDRESS1, BUYER_ADDRESS2, 
        BUYER_CITY, BUYER_STATE, BUYER_ZIP, BUYER_COUNTY):

        self.BUYER_DEA_NO = BUYER_DEA_NO
        self.BUYER_BUS_ACT = BUYER_BUS_ACT
        self.BUYER_NAME = BUYER_NAME
        self.BUYER_ADDL_CO_INFO = BUYER_ADDL_CO_INFO
        self.BUYER_ADDRESS1 = BUYER_ADDRESS1
        self.BUYER_ADDRESS2 = BUYER_ADDRESS2
        self.BUYER_CITY = BUYER_CITY
        self.BUYER_STATE = BUYER_STATE
        self.BUYER_ZIP = BUYER_ZIP
        self.BUYER_COUNTY = BUYER_COUNTY

    def __repr__(self):
        return '<index {}>'.format(self.BUYER_DEA_NO)
