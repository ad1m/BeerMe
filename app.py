__author__ = 'Adamlieberman'
import os
from flask import Flask, render_template, request
from utility import *
from model import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main.html')
def index2():
    return render_template('index2.html')
@app.route('/',methods=['GET','POST'])
def user_beer():

    #Get beer id from user's craft beer selection
    query_beer = int(request.form['beer']) #This is the beer_id
    print(query_beer)



    #Load namez dataframe for query vector
    namez = pd.read_pickle('namez.p')
    features = pd.read_pickle('features.p')
    print namez.head(10)
    query_vec = namez[namez['beer_name'] == query_beer].values.flatten()[1:]

    print query_vec
    #Load pickled KDTree
    tree = load_model('tree.p')
    k_val = 4
    distance,index = tree.query(query_vec,k=k_val)

    #Load reverse dictionary
    with open('reverse_dict_name.p', 'rb') as f:
        reverse_dict_name = pickle.load(f)
    user_beer = reverse_dict_name[query_beer]

    #get recommended beers

    with open('reverse_dict_brewery.p', 'rb') as f:
        reverse_dict_brewery = pickle.load(f)

    with open('reverse_dict_style.p', 'rb') as f:
        reverse_dict_style = pickle.load(f)


    recommended_beers,beer_feats = get_recommendations(index,reverse_dict_name,user_beer,features)
    formatted_feats = format_reccomended_stats(reverse_dict_brewery, reverse_dict_style,beer_feats)
    beer1 = str(recommended_beers[0])
    beer1_feats = formatted_feats[0]
    beer2 = str(recommended_beers[1])
    beer2_feats = formatted_feats[1]
    beer3 = str(recommended_beers[2])
    beer3_feats = formatted_feats[2]

    print(beer3)
    print beer3_feats

    return render_template('recommendations.html',beer1=beer1,beer1_feats=beer1_feats,beer2=beer2,
                           beer2_feats=beer2_feats,beer3=beer3,beer3_feats=beer3_feats)


@app.route('/recommendations')
def recos():
    return render_template('recommendations.html')

@app.route('/index.html')
def back():
    return render_template('index2.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

    #To get rid of the Errno[48] go to the terminal and type in lsof -i tcp:5000 and then kill the running numbers
    #kill <PID Number>