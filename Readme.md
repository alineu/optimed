# OptiMed

**OptiMed** is a [Python](https://www.python.org/) drug-recommendation web-application that uses [Flask](https://palletsprojects.com/p/flask/) as webserver and is deployed on [Heroku](https://www.heroku.com/). Database management and the user interface are handled with [PostgreSQL](https://www.postgresql.org/) and [JavaScript](https://www.javascript.com/) ([AngularJS](https://angular.io/)), respectively.

![](/static/info.png)

## [Live Demo](https://optimed-stage.herokuapp.com/)

Click on the above link (Live Demo) and follow the instructions.

## How it works?

**OptiMed** uses a SQL database that is created by analyzing 260000 online pharmaceutical reviews from [Drugs.com](https://www.drugs.com/) ([Reference](http://archive.ics.uci.edu/ml/datasets/Drug+Review+Dataset+%28Drugs.com%29)). A combination of multiple metrics determines the winner drug for a given user condition:
- User ratings from the dataset
- [Sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) score from user reviews which is obtained using [Natural language processing (NLP)](https://en.wikipedia.org/wiki/Natural_language_processing)
- User distance to pharmacies from [this database](https://www.washingtonpost.com/graphics/2019/investigations/dea-pain-pill-database/#download-resources) provided by the [Washington Post](https://www.washingtonpost.com/) (currently unavailable)
- Real-time drug prices from [WellRx.com](https://www.wellrx.com/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)