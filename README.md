# game_review

[metacritic](http://www.metacritic.com/game) game review analyze project

## Contents

- Recommendation system
- Sentiment Analysis

### Recommendation system

score base recommendation system

#### Tools

> Surprise, Mongodb, Flask, Scrapy

#### work flow

1. **Receive** the user score of game
    - score : 0 - 10  
    - random pick the game
    - which had been scored at least 30 users

1. **Insert** user score on data base

1. **Train** model (SVD)
    - data size ~ 100k

1. **Recommend** the 6 highest expected score game
    - which had not been scored by user

- [ipython note](https://github.com/Moons08/game_review/blob/master/note/01.recommend.ipynb)

#### To do

- receive multiple scores (done)
- make loading page (done)
- make it OOP

---

### Sentiment Analysis

review base sentiment prediction

#### Tools

> Scikit-learn, sqlite, Flask, Scrapy

#### work flow

1. **Train** model by scraped data
    - SGD classifier(logistic regression)
    - data size ~100k
2. Receive user comment
3. **Predict** label
    - positive or negative
4. Receive **feedback** from user
    - collect or incorrect
5. Insert user comment with feedback on data base
6. **update** model with new data
    - partial_fit

- [note - scikit](https://github.com/Moons08/game_review/blob/master/note/02.NLP_scikit.ipynb)
- [note - doc2vec](https://github.com/Moons08/game_review/blob/master/note/03.NLP_doc2vec.ipynb)

#### To do

- try other model
- try multiple label (sentiment)
- combine with recommendation system
