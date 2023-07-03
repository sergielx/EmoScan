from flask import (
    render_template, Blueprint, redirect, request, session, url_for
)
from flask_login import login_required, current_user
from EmoScan.models.tweets import Tweet
from EmoScan.models.queries import Query
import matplotlib.pyplot as plt


est = Blueprint('est', __name__, )

def generarGraficaSentimientos(query_id):
    tweets = Tweet.getTweetsByQuery(user_id=current_user.id, query_id=query_id)

    # Obtener la cantidad de tweets para cada sentimiento
    sentiment_counts = {'negativo': 0, 'neutro': 0, 'positivo': 0}
    for tweet in tweets:
        sentiment = tweet[4]  # Índice correspondiente al campo 'sentiment'
        sentiment_counts[sentiment] += 1

    # Crear la gráfica
    labels = sentiment_counts.keys()
    values = sentiment_counts.values()

    plt.figure(figsize=(5, 4))
    plt.bar(labels, values)
    plt.xlabel('Sentimiento')
    plt.ylabel('Cantidad de Tweets')
    plt.title('Distribución de Sentimientos')

    # Guardar la gráfica en un archivo temporal
    graph_file = './EmoScan' + url_for('static', filename='img/n_tipo_sent.png')
    plt.savefig(graph_file)
    plt.clf()
    plt.cla()
    plt.close()

    return sentiment_counts

def generarGraficaFecha(query_id):
    tweets = Tweet.getTweetsByQuery(user_id=current_user.id, query_id=query_id)

    # Obtener la fecha de cada tweet y el sentimiento asociado
    fecha_sentimiento = {}
    for tweet in tweets:
        fecha = tweet[1]  # Índice correspondiente al campo 'date'
        sentiment = tweet[4]  # Índice correspondiente al campo 'sentiment'
        if fecha in fecha_sentimiento:
            fecha_sentimiento[fecha].append(sentiment)
        else:
            fecha_sentimiento[fecha] = [sentiment]

    # Obtener los datos para la gráfica
    fechas = sorted(fecha_sentimiento.keys())
    valores_positivos = []
    valores_neutros = []
    valores_negativos = []

    for fecha in fechas:
        sentimientos = fecha_sentimiento[fecha]
        positivos = sentimientos.count('positivo')
        neutros = sentimientos.count('neutro')
        negativos = sentimientos.count('negativo')
        valores_positivos.append(positivos)
        valores_neutros.append(neutros)
        valores_negativos.append(negativos)

    # Crear la gráfica
    plt.figure(figsize=(5, 4))
    plt.plot(fechas, valores_positivos, label='Positivo')
    plt.plot(fechas, valores_neutros, label='Neutro')
    plt.plot(fechas, valores_negativos, label='Negativo')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad de Tweets')
    plt.title('Distribución de Sentimientos por Fecha')
    plt.legend()

    # Guardar la gráfica en un archivo temporal
    graph_file = './EmoScan' + url_for('static', filename='img/n_sentimientos_fecha.png')
    plt.savefig(graph_file)
    plt.clf()
    plt.cla()
    plt.close()

def generarGraficaCirc(sentiment_counts):
    labels = sentiment_counts.keys()
    values = sentiment_counts.values()

    plt.figure(figsize=(5, 4))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Porcentaje de Sentimientos')

    # Guardar la gráfica en un archivo temporal
    graph_file = './EmoScan' + url_for('static', filename='img/grafica_circ.png')
    plt.savefig(graph_file)

    plt.clf()
    plt.cla()
    plt.close()


@est.route('/estadisticas')
@login_required
def estadisticas():

    queries = Query.getQueriesWithSentimentByUser(user_id=current_user.id)

    return render_template('estadisticas.html', queries=queries)

@est.route('/estadisticas_resultados')
@login_required
def resultadosEstadisticas():

    if 'query_id' in request.args:
        query_id = request.args.get('query_id')
    elif 'query_id' in session:
        query_id = session['query_id']

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


    sentiment_count = generarGraficaSentimientos(query_id)
    generarGraficaFecha(query_id)
    generarGraficaCirc(sentiment_count)




    return render_template('estadisticas_resultados.html', filtros=filtros_)

@est.route('/eliminar_consulta', methods=['GET', 'POST'])
@login_required
def eliminarConsulta():

    if request.method == 'POST':
        query_id = request.form.get('query_id')

        # Eliminar los datos guardados
        Tweet.deleteTweetsByQueryId(query_id)
        Query.deleteQueryById(query_id)
 
    return redirect(url_for('est.estadisticas'))
    
@est.route('/eliminar_consultas_seleccionadas', methods=['POST'])
@login_required
def eliminarConsultasSeleccionadas():
    if request.method == 'POST':
        selected_queries = request.form.getlist('query_id')
        print(selected_queries)
        
        if selected_queries:
            for query_id in selected_queries:
                Tweet.deleteTweetsByQueryId(query_id)
                Query.deleteQueryById(query_id)

    return redirect(url_for('est.estadisticas'))