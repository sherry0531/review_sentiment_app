from flask import Flask, render_template, abort, request, jsonify
import numpy as np
from tensorflow import keras
#from keras.utils import to_categorical
from keras import models
from keras import layers
from keras.datasets import imdb
import time, datetime
import wandb

app = Flask(__name__)

wandb.login(key='dac290e00d055cc1030bc53cc495eca88eb95f86')

experiment_name = datetime.datetime.today().strftime('%Y-%m-%d')
run=wandb.init(project='IMDB sentiment',
                group=experiment_name,
                notes='production monitoring')
output = {}

index = imdb.get_word_index()
model = keras.models.load_model('my_model')

def w_to_index(text, index):
# to do: remove puncs
    lst = []
    non_exist = 9999999
    for w in text.split(" "):
        try:
            w_indx = index[w.lower()]
        except:
            w_indx = non_exist
        lst += [w_indx]
    return([lst])

def vectorize(sequences, dimension = 10000):
    non_exist = 9999999
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        sequence = [w for w in sequence if w != non_exist]
        results[i, sequence] = 1
    return results

def sentiment(vect):
    score = model(vect)
    if(score>0.5):
        return "Positive"
    else:
        return "Negative"

def calc_metrics(text, text_vec):
    text_len = len(text.split(" "))
    unique_words_perct = round(len(set(text.split(" ")))/text_len * 100, 1)
    new_text = np.sum(text_vec)
    new_text_perct = np.sum(text_vec)/text_len
    metrics = {'text_len': text_len,
                'unique_words_perct': unique_words_perct,
                'new_text': new_text,
                'new_text_perct': new_text_perct,
                }
    return(metrics)

def pred(model, text):
    time0 = time.time()
    text_index = w_to_index(text, index)
    vect = vectorize(text_index, dimension = 10000)
    sent = sentiment(vect)
    pred_time = time.time() - time0
    metrics = calc_metrics(text, vect)
    metrics['pred_time'] = pred_time
    monitor(metrics)
    return(sent)

def monitor(metrics):
    wandb.log({
           "Prediction Time": metrics['pred_time'],
           "Input Text Word Count": metrics['text_len'],
           "Input Text Unique Word Perct": metrics['unique_words_perct'],
           "Input Text Unseen Word Count": metrics['new_text'],
           "Input Text Unseen Word Perct": metrics['new_text_perct']})



@app.route("/", methods = ["GET","POST"])
def sentimentRequest():
    if request.method == "POST":
        sentence = request.form['q']
        sent = pred(model, sentence)
        output['sentiment'] = sent
        return jsonify(output)
    else:
        sentence = request.args.get('q')
        sent = pred(model, sentence)
        output['sentiment'] = sent
        return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
