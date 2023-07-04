from flask import (
    render_template, Blueprint, redirect, request, session, url_for
)
from flask_login import login_required, current_user
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from flask_paginate import Pagination, get_page_parameter
import string
from EmoScan.models.tweets import Tweet
from EmoScan.models.queries import Query
ana = Blueprint('ana', __name__, )

# Descargar los recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

def preprocess_text(text):
    # Convertir el texto a minúsculas
    text = text.lower()

    # Tokenización
    tokens = word_tokenize(text)

    # Eliminación de stopwords y puntuación
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    tokens = [token for token in tokens if token not in stop_words and token not in punctuation]

    # Reconstrucción del texto preprocesado
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    sentiment2 = sentiment_scores['compound']
    return sentiment2


@ana.route('/analizar_tweets/', methods=('GET','POST'))
@login_required
def analizar():
    
    queries = Query.getQueriesByUser(user_id=current_user.id)

    return render_template('analizar.html', queries = queries)


@ana.route('/analizar_resultados/')
@login_required
def resultadosAnalizar():

    if 'query_id' in request.args:
        query_id = request.args.get('query_id')
    elif 'query_id' in session:
        query_id = session['query_id']

    session['query_id'] = query_id

    page = request.args.get(get_page_parameter(), type=int, default=1)


    tweets_ = Tweet.getTweetsByQuery(user_id=current_user.id, query_id=query_id)

    # Crear una lista para almacenar los tweets preprocesados
    tweets__ = []

    # Analizar el sentimiento de cada tweet.
    for tweet in tweets_:

        analyze = analyze_sentiment(tweet[2])
        if(analyze > 0):
            sent = 'positivo'
        elif(analyze < 0):
            sent = 'negativo'
        else:
            sent = 'neutro'


        Tweet.addPolAndSent(analyze, sent, tweet[0])
        tweets__.append([tweet[1], tweet[2], tweet[3], analyze, sent])

    tweet_df = pd.DataFrame(tweets__, columns=["fecha", "tweet", "usuario","polaridad", "sentimiento"])
    tweet_df.to_csv("tweets_preprocessed.csv", index=False)
    csv_data = pd.read_csv('tweets_preprocessed.csv')
    values = csv_data.values
    columns = csv_data.columns.tolist()

    # Número de tweets por página
    per_page = 10  
    
    total_tweets = len(csv_data)
    start = (page - 1) * per_page
    end = start + per_page
    values_paginated = values[start:end]
    
    # Crear el objeto de paginación
    pagination = Pagination(page=page, total=total_tweets, per_page=per_page, record_name='tweets', css_framework='bootstrap5')
    
    return render_template('analizar_resultados.html', page=page, columns=columns, pagination=pagination, values=values_paginated)


@ana.route('/eliminar_consulta', methods=['GET', 'POST'])
@login_required
def eliminarConsulta():

    if request.method == 'POST':
        query_id = request.form.get('query_id')
            
        # Eliminar los datos guardados
        Tweet.deleteTweetsByQueryId(query_id)
        Query.deleteQueryById(query_id)
 
    return redirect(url_for('ana.analizar'))
    
@ana.route('/eliminar_consultas_seleccionadas', methods=['POST'])
@login_required
def eliminarConsultasSeleccionadas():
    if request.method == 'POST':
        selected_queries = request.form.getlist('query_id')
      
        if selected_queries:
            for query_id in selected_queries:
                # Eliminar los datos guardados
                Tweet.deleteTweetsByQueryId(query_id)
                Query.deleteQueryById(query_id)

    return redirect(url_for('ana.analizar'))