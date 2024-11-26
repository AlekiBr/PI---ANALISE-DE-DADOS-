from flask import Flask, render_template, request, send_file, jsonify
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from reportlab.pdfgen import canvas
import tempfile
import json
from datetime import datetime
import statistics

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_url = None
    stats = {}
    if request.method == 'POST' and 'data' in request.form:
        data = request.form['data']
        chart_type = request.form['chart_type']
        
        # Processar os dados
        try:
            data = [list(map(float, row.split())) for row in data.split('\n') if row.strip()]
        except ValueError as e:
            return f"Erro ao converter dados: {e}"

        # Calcular estatísticas
        flattened_data = [item for sublist in data for item in sublist]
        stats['mean'] = statistics.mean(flattened_data)
        stats['median'] = statistics.median(flattened_data)
        stats['mode'] = statistics.mode(flattened_data)
        stats['max'] = max(flattened_data)
        stats['min'] = min(flattened_data)
        stats['stdev'] = statistics.stdev(flattened_data)
        stats['variance'] = statistics.variance(flattened_data)

        plt.figure()
        if chart_type == 'scatter':
            for row in data:
                plt.scatter(range(len(row)), row)
        elif chart_type == 'line':
            for row in data:
                plt.plot(row)
        elif chart_type == 'bar':
            for row in data:
                plt.bar(range(len(row)), row)
        elif chart_type == 'polar':
            if all(len(row) >= 2 for row in data):  # Verifica se todas as linhas têm pelo menos 2 elementos
                angles = [row[0] for row in data]
                distances = [row[1] for row in data]
                plt.polar(angles, distances)
            else:
                return "Erro: Dados insuficientes para gráfico polar."
        elif chart_type == 'heatmap':
            plt.imshow(data, cmap='hot', interpolation='nearest')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url, stats=stats)

@app.route('/export_excel', methods=['POST'])
def export_excel():
    data = request.form['data']
    data = [list(map(float, row.split())) for row in data.split('\n') if row.strip()]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return send_file(output, download_name='grafico.xlsx', as_attachment=True)

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    data = request.form['data']
    data = [list(map(float, row.split())) for row in data.split('\n') if row.strip()]

    plt.figure()
    if all(len(row) >= 2 for row in data):  # Verifica se todas as linhas têm pelo menos 2 elementos
        angles = [row[0] for row in data]
        distances = [row[1] for row in data]
        plt.polar(angles, distances)
    else:
        return "Erro: Dados insuficientes para gráfico polar."

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
        tmpfile.write(img.getvalue())
        tmpfile_path = tmpfile.name

    pdf_output = io.BytesIO()
    c = canvas.Canvas(pdf_output)
    c.drawImage(tmpfile_path, 0, 0, width=500, height=400)
    c.showPage()
    c.save()
    pdf_output.seek(0)

    return send_file(pdf_output, download_name='grafico.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
