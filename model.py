__author__ = 'Adamlieberman'
from scipy.spatial import cKDTree  #Using c for pickle
from utility import *
import pickle

def generate_features(df,col,feat_cols):
    features = df.groupby([col]).mean()
    namez = features.copy()
    namez.reset_index(level=0,inplace=True)
    #pickle namez
    namez.to_pickle('namez.p')
    features.to_pickle('features.p')
    feat_vec = features[feat_cols]
    return namez,features,feat_vec


def build_tree(feat_vec,filename):
    #Build KDTre
    tree = cKDTree(feat_vec)

    #Pickle KDTree
    f = open(filename,'w')
    pickle.dump(tree,f)
    f.close()
    return


def load_model(pickle_file):
    with open(pickle_file, 'rb') as fid:
        model = pickle.load(fid)
    fid.close()
    return model


def get_recommendations(index,reverse_dict_name,user_beer,features):
    recommended_beers = []
    beer_feats = []
    for i in index:
        beer_feats.append(features.iloc[i])
        recommended_beers.append(str(reverse_dict_name[features.iloc[i].name]))

    #Remove user beer since it has distance 0 in the lookup
    if user_beer in recommended_beers:
        indx = recommended_beers.index(user_beer)
        recommended_beers.remove(user_beer)
        beer_feats.pop(indx)

    return recommended_beers,beer_feats


def format_reccomended_stats(reverse_dict_brewery, reverse_dict_style,beer_feats):
    new_feats = []
    for i in beer_feats:
        i = list(i.values)
        print
        bn = int(i[0])
        sn = int(i[4])
        i[0] = string_handler(reverse_dict_brewery[bn]) #get the name
        i[1] = round(float(i[1]),2)
        i[2] = round(float(i[2]),2)
        i[3] = round(float(i[3]),2)
        i[4] = string_handler(reverse_dict_style[sn])#get the style
        i[5] = round(float(i[5]),2)
        i[6] = round(float(i[6]),2)
        new_feats.append(i)
    return new_feats
        #holder = []
        #name = reverse_dict_name[i[0]]  #brewery name
        #overall_reviews = i[1]
        #overall_aroma = i[2]
        #overall_appearance = i[3]
        #style = reverse_dict_style[int(i[4])]
        #overall_palate = i[5]
        #overall_taste = i[6]



if __name__ == "__main__":

    #Load Data
    print('Loading Data...')
    link = 'https://query.data.world/s/cqa9clje3ye4un611s1nw5fo3'
    features = ['beer_name','brewery_name','review_overall','review_aroma','review_appearance','beer_style','review_palate','review_taste']
    df = load_data(link,features)

    #Preprocess Data
    print('Preprocessing Data...')
    df = preprocess(df)
    print(df.head(5))

    #Mappings
    print('Remapping Data...')
    dict_brewery, reverse_dict_brewery, df = mapping(df,'brewery_name','reverse_dict_brewery.p',reverse=True)
    dict_style, reverse_dict_style, df = mapping(df,'beer_style','reverse_dict_style.p',reverse=True)
    dict_name, reverse_dict_name, df = mapping(df,'beer_name','reverse_dict_name.p',reverse=True)
    print(df.head(5))

    #Feature Generation - Use what we have but groupby and take mean
    print('Building Features')

    feat_cols = ['brewery_name', 'review_overall', 'review_aroma',
       'review_appearance', 'beer_style', 'review_palate', 'review_taste']
    namez, features,feat_vec = generate_features(df,'beer_name',feat_cols)

    #features = df.groupby(['beer_name']).mean()
    #namez = features.copy()
    #namez.reset_index(level=0,inplace=True)
    #feat_vec = features[['brewery_name', 'review_overall', 'review_aroma',
       #'review_appearance', 'beer_style', 'review_palate', 'review_taste']].values   #removed beer name

    #Build Tree
    print('Building Tree')
    build_tree(feat_vec,'tree.p')

    #Load Tree
    print('Loading Tree')
    tree = load_model('tree.p')

    #Sample of user selecting craft beer to query
    user_beer = 'harboe bear beer premium strong beer'
    query_beer = dict_name[user_beer]
    query_vec = namez[namez['beer_name'] == query_beer].values.flatten()[1:]

    #Querying KDTree
    print('Querying Tree')
    k_val = 4
    distance,index = tree.query(query_vec,k=k_val)

    #Recommended Beers
    print("Getting Recommendations")
    recommended_beers,beer_feats = get_recommendations(index,reverse_dict_name,user_beer,features)
    print("\n",'Recommended Beers:')
    print(recommended_beers)
    for i in recommended_beers:
        print(str(i))

    #Format Recommended Stats
    stats = format_reccomended_stats(reverse_dict_brewery, reverse_dict_style,beer_feats)
    print stats
    for i in stats:
        for j in i:
            print j