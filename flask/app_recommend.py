from flask import Flask, render_template, request
from wtforms import Form, SelectField, validators, TextAreaField
from surprise import Dataset, Reader, SVD
import os
import json, pymongo
import numpy as np
import pandas as pd
import random
import datetime

app = Flask(__name__)
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.recommend
title_list=set(pd.read_csv('../data/title_list.csv').title)

def add_data(new_id, titles, scores):
    db.recommend.insert([{'id':new_id, 'title':titles, 'score':scores}])

def train():
    # 전체 데이터를 불러와서 추천 시스템 학습
    df = pd.DataFrame(list(db.recommend.find()), columns=['id', 'title', 'score'])
    user_limit= 10 # 10개 이상 평가한 유저의 데이터만 사용
    filtered_id = user_counts_df[user_counts_df["user_rating_count"] >= user_limit]
    filtered_id = list(filtered_id["id"])
    df = df[df["id"].isin(filtered_id)]
    df = Dataset.load_from_df(df[['id', 'title','score']],
                                        reader=Reader(rating_scale=(0,10)))
    trainset=df.build_full_trainset()
    recommender = SVD(n_factors=50, n_epochs=90, lr_all=0.02, reg_all=0.02)
    recommender.fit(trainset)
    return recommender

def recommend(recommender, new_id, titles):
    # 새 고객이 평가하지 않은 작품중
    unscored = title_list-set(titles)
    pred = [recommender.predict(new_id, i, verbose=False) for i in unscored]
    # 가장 예상 평점이 높은 작품 10개 추천
    pred = pd.DataFrame([[i.iid, i.est] for i in pred], columns=['title', 'score'])
    pred.sort_values('score', ascending=False, inplace=True)
    pred.reset_index(drop=True, inplace=True)
    return list(pred.title.loc[:10])

class RecommendForm(Form):
    game_rec = SelectField(u'your score',
                        choices=[('0', '0'), ('1', '1'), ('2', '2'),
                                 ('3', '3'), ('4', '4'), ('5', '5'),
                                 ('6', '6'), ('7', '7'), ('8', '8'),
                                 ('9', '9'), ('10', '10')])

@app.route('/game_recommend/')
def rec_index():
    form = RecommendForm(request.form)
    random_titles = random.sample(title_list, 1)
    return render_template('recommendform.html',
                            form=form,
                            random_titles=random_titles)

@app.route('/game_recommend/results', methods=['POST'])
def rec_results():
    form = RecommendForm(request.form)
    if request.method =='POST' and form.validate():
        new_id = datetime.datetime.now().timestamp()
        titles = request.form['titles']
        scores = request.form['game_rec']
        add_data(new_id, titles, scores)
        result = recommend(train(), new_id, titles)

        return render_template('recommendresult.html', result=result)

if __name__=='__main__':
    app.run(debug=True)
