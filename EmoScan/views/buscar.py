from flask import (
    render_template, Blueprint, flash, redirect, request, session, url_for
)
from flask_login import login_required, current_user
import pandas as pd
import snscrape.modules.twitter as sntwitter
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from EmoScan.models.queries import Query
from EmoScan.models.tweets import Tweet
busc = Blueprint('busc', __name__, )


def get_tweets(filtros, numero_tweets):

    filtros_ = []
    if 'mostrar_respuestas' not in request.form:
        filtros += ' -filter:replies '
        filtros_.append(False)
    else:
        filtros_.append(True)
    
    if 'idioma' in request.form:
        idioma = request.form['idioma']
        if idioma == 'en':
            filtros += ' lang:en '
            filtros_.append('Inglés')
    
    if 'desde' in request.form and request.form['desde']:
        filtros += ' since:' + request.form['desde'] + ' '
        filtros_.append(request.form['desde'])
    else:
        filtros_.append(None)
    
    if 'hasta' in request.form and request.form['hasta']:
        filtros += ' until:' + request.form['hasta'] + ' '
        filtros_.append(request.form['hasta'])
    else:
        filtros_.append(None)
    
    if 'numero_tweets' in request.form and request.form['numero_tweets']:
        numero_tweets = int(request.form['numero_tweets'])
    elif 'numero_tweets1' in request.form and request.form['numero_tweets1']:
        numero_tweets = int(request.form['numero_tweets1'])
    elif 'numero_tweets2' in request.form and request.form['numero_tweets2']:
        numero_tweets = int(request.form['numero_tweets2'])
    else:
        numero_tweets = 100

    if numero_tweets <= 0:
        numero_tweets = 100
    
    filtros_.append(numero_tweets)
    
    if 'query' in request.form and request.form['query']:
        query = request.form['query']
        consulta = query + filtros
        scraper = sntwitter.TwitterSearchScraper(consulta)
        print(consulta)
        filtros_.append("Palabra clave")

    elif 'username' in request.form and request.form['username']:
        username = request.form['username']
        consulta = 'from:' + username + filtros
        scraper = sntwitter.TwitterSearchScraper(consulta)
        print(consulta)
        filtros_.append("Usuario")

    elif 'hashtag' in request.form and request.form['hashtag']:
        hashtag = request.form['hashtag']
        consulta = hashtag + filtros
        scraper = sntwitter.TwitterHashtagScraper(consulta)
        filtros_.append("Hashtag")

    tweets = []

    try:
        for i, tweet in enumerate(scraper.get_items()):
            data = [
                tweet.date.strftime('%d/%m/%Y'),
                tweet.rawContent,
                tweet.user.username,
            ]

            tweets.append(data)

            if i > numero_tweets - 2:
                break

    except Exception as e:
        flash('Error al obtener los tweets: {}'.format(str(e)), 'error')
        return redirect(url_for('busc.buscar'))

    return tweets, filtros_


@busc.route('/buscar_tweets', methods=('GET','POST'))
@login_required
def buscar():

    if request.method == 'POST':

        filtros = ''
        numero_tweets = 10

        tweets, filtros_ = get_tweets(filtros, numero_tweets)

        query_ = request.form.get('query', '') or request.form.get('username', '') or request.form.get('hashtag', '')

        query_obj = Query(id=None, user_id=current_user.id, query=query_, query_datetime=datetime.now(), query_type = filtros_[5], show_replies=filtros_[0], language=filtros_[1], from_date=filtros_[2], to_date=filtros_[3], tweet_count=filtros_[4])


        query_id_ = query_obj.savequery()

 
        # Guardar los tweets en la base de datos
        for tweet_data in tweets:
            tweet_obj = Tweet(
                id = None,
                user_id=current_user.id, 
                query_id=query_id_,
                date=tweet_data[0],
                content=tweet_data[1],
                tweet_user=tweet_data[2]
            )

            tweet_obj.saveTweets()

        tweets_ = Tweet.getTweetsByQuery(user_id=current_user.id, query_id=query_id_)
        tweets__ = []

        for tweet in tweets_:
            tweets__.append([tweet[1], tweet[2], tweet[3]])

        session['query_id'] = query_id_


        tweet_df = pd.DataFrame(tweets__, columns=["fecha", "tweet", "usuario"])
        tweet_df.to_csv("tweets.csv", index=False)

        session['show_table'] = True
        return redirect(url_for('busc.resultadosBuscar'))


    return render_template('buscar.html')


@busc.route('/resultados_busqueda', methods=('GET','POST'))
@login_required
def resultadosBuscar():

    page = request.args.get(get_page_parameter(), type=int, default=1)
    csv_data = pd.read_csv('tweets.csv')
    values = csv_data.values
    columns = csv_data.columns.tolist()

    show_table = session.get('show_table', False)

    per_page = 10  # Number of tweets to display per page
    
    total_tweets = len(csv_data)
    start = (page - 1) * per_page
    end = start + per_page
    values_paginated = values[start:end]
    
    # Create the pagination object
    pagination = Pagination(page=page, total=total_tweets, per_page=per_page, record_name='tweets', css_framework='bootstrap5')

    # Obtener los parámetros de búsqueda utilizados
    query_id = session.get('query_id')
    query_obj = Query.getQueryById(query_id)
    filtros_ = {
        'tipo': query_obj.query_type,
        'consulta': query_obj.query,
        'numero_tweets': query_obj.tweet_count,
        'mostrar_respuestas': query_obj.show_replies,
        'idioma': query_obj.language,
        'desde': query_obj.from_date,
        'hasta': query_obj.to_date
    }

    session['valor'] = 1

    return render_template('buscar_resultados.html',page=page, columns=columns, pagination=pagination, values=values_paginated, show_table = show_table, filtros=filtros_)


@busc.route('/volver_a_buscar', methods=['GET'])
@login_required
def volverABuscar():
    # Eliminar los datos guardados
    query_id= session.get('query_id')

    Tweet.deleteTweetsByQueryId(query_id)
    Query.deleteQueryById(query_id)
    session.pop('query_id', None)
    session.pop('show_table', None)
    
    return redirect(url_for('busc.buscar'))