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
    for i in range(len(titles)):
        if scores[i]=='X':
            continue
        else:
            db.recommend.insert([{'id':new_id, 'title':titles[i], 'score':scores[i]}])

def train():
    # 전체 데이터를 불러와서 추천 시스템 학습
    df = pd.DataFrame(list(db.recommend.find()), columns=['id', 'title', 'score'])
    user_limit= 10 # 10개 이상 평가한 유저의 데이터만 사용
    user_counts_df = df.groupby("id").size().reset_index(name="user_rating_count")
    filtered_id = user_counts_df[user_counts_df["user_rating_count"] >= user_limit]
    filtered_id = list(filtered_id["id"])
    df = df[df["id"].isin(filtered_id)]
    df = Dataset.load_from_df(df[['id', 'title','score']],
                                        reader=Reader(rating_scale=(0,10)))
    trainset=df.build_full_trainset()
    recommender = SVD(n_factors=160, n_epochs=86, lr_all=0.022, reg_all=0.024)
    recommender.fit(trainset)
    return recommender

def recommend(recommender, new_id, titles):
    # 새 고객이 평가하지 않은 작품중
    unscored = title_list-set(titles)
    pred = [recommender.predict(new_id, i, verbose=False) for i in unscored]
    # 가장 예상 평점이 높은 작품 5개 추천
    pred = pd.DataFrame([[i.iid, i.est] for i in pred], columns=['title', 'score'])
    pred.sort_values('score', ascending=False, inplace=True)
    pred.reset_index(drop=True, inplace=True)
    titles = list(pred.title.loc[:5])
    scores = list(pred.score.loc[:5])
    return titles, scores

@app.route('/game_recommend/')
def rec_index():
    random_titles = random.sample(title_list, 8)
    return render_template('recommendform.html',
                            random_titles=random_titles)

@app.route('/game_recommend/results', methods=['POST'])
def rec_results():
    new_id = datetime.datetime.now().timestamp()
    if request.method =='POST':
        jsonData = request.get_json()
        titles = jsonData['titles']
        scores = jsonData['scores']
        add_data(new_id, titles, scores)
        titles, scores =  recommend(train(), new_id, titles)
        result = {"status":200, "predict":scores, "result": titles}
    else:
        result = {"status":201}

    return jsonify(result)

if __name__=='__main__':
    app.run(debug=True)
