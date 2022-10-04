from flask import Flask,render_template,request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from numpy.linalg import norm
import pandas as pd
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#Authentication
client_credentials_manager = SpotifyClientCredentials(client_id='4b4cb4f8525543959104a2168e29e1c9', client_secret='8ea4d3b6032c4a35ba22999240e6859d')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
df = pd.read_csv(r"Dataset\database.csv")
df_songs_joined = pd.read_csv(r"Dataset\km_alog.csv")

df["mood_vec"] = df[["valence", "energy"]].values.tolist()


app=Flask(__name__)

def recommend(track_id, ref_df, sp, n_recs = 5):
    
    # Crawl valence and arousal of given track from spotify api
    global track_features
    track_features = sp.audio_features(track_id)[0]
    track_moodvec = np.array([track_features['valence'], track_features['energy']])
    print(f"mood_vec for {track_id}: {track_moodvec}")
    
    
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # If the input track is in the reference set, it will have a distance of 0, but should not be recommendet
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # Return n recommendations
    return ref_df_sorted.iloc[:n_recs]['id']

def recommend1():
    with open("Dataset\model1.pkl", "rb") as f:
        model = pickle.load(f)
    with open("Dataset\scalar_ss.pkl", "rb") as f:
        ss = pickle.load(f)
    columns_to_cluster = ['acousticness', 'danceability', 'energy', 
                      'instrumentalness', 'liveness','valence', 'tempo','speechiness', 'loudness']
    pr = pd.DataFrame(track_features, columns=columns_to_cluster,index=[0])
    y=model.predict(ss.transform(pr))
    final=df_songs_joined.loc[df_songs_joined['cluster']==int(y)]['id'].sample(frac=1).head(5)
    print(y)
    print(final)
    return list(final)

@app.route('/',methods=('GET','POST'))
def home():
    if request.method=="POST":
        song=request.form.get('song')
        s=sp.search(song,limit=1)['tracks']['items'][0]
        sid=s['id']
        sname=s['album']['name']
        try:
            aname=s['album']['artists'][0]['name']+", "+s['album']['artists'][1]['name']
        except:
            aname=s['album']['artists'][0]['name']
        img=s['album']['images'][1]['url']
        recc=list(recommend(sid,df,sp))
        recc.extend(recommend1())
        print(recc)
        recc_sname,recc_aname,recc_img,recc_url=[],[],[],[]
        for i in recc:
            try:
                tmp=sp.track(i)
                tmp_sn=tmp['name']
                tmp_an=tmp['album']['artists'][0]['name']
                tmp_im=tmp['album']['images'][0]['url']
                tmp_ur=tmp['external_urls']['spotify']    
            except:
                continue
            recc_sname.append(tmp_sn)
            recc_aname.append(tmp_an)
            recc_img.append(tmp_im)
            recc_url.append(tmp_ur)

        return render_template('index.html',sname=sname,aname=aname,img=img,r=zip(recc_sname,recc_aname,recc_img,recc_url))
    return render_template('index.html')
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__=="__main__":
    app.run()

#flask run --host=0.0.0.0