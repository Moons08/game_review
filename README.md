# game_review
[metacritic](http://www.metacritic.com/game) game review analyze project

## Contents
- [Recommendation system](#Recommendation)
- [Sentiment Analysis](#Sentiment)

---

### Recommendation system
score base recommendation system
#### Tools
> Surprise, Mongodb, Flask, Scrapy
#### work flow
1. **Recieve** the user score of game
    - score : 0 - 10  
    - random pick the game
    - which had been scored at least 30 users

1. **Insert** user score on data base

1. **Train** model (SVD)
    - data size ~ 100k

1. **Recommend** the 10 highest expected score game
    - which had not been scored by user

- [Sample page](http://www.cocactus.tk/game_recommend/)
- [ipython note](https://github.com/Moons08/game_review/blob/master/note/01.recommend.ipynb)

#### To do
- recieve multiple scores
- make loading page

---

### Sentiment Analysis
review base sentiment prediction
#### Tools
> Scikit-learn, sqlite, Flask, Scrapy

#### work flow
1. **Train** model by scraped data
    - SGD classifier(logistic regression)
    - data size ~100k
1. Recieve user comment
1. **Predict** label
    - positive or negative
1. Recieve **feedback** from user
    - collect or incorrect
1. Insert user comment with feedback on data base
1. **update** model with new data
    - partial_fit

- [Sample page](http://www.cocactus.tk/game_review)

#### To do
- try other model
- try multiple label (sentiment)
- combine with recommendation system
