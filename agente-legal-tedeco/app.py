import os
from flask import Flask, request, render_template_string
from openai import OpenAI

# Inicializa el cliente moderno de OpenAI sin proxies
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Asesor Legal TEDECO</title>
    <style>
        body {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
            padding: 40px;
        }
        .container {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 30px;
            max-width: 800px;
            margin: auto;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #006400;
            text-align: center;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            margin-top: 15px;
            margin-bottom: 25px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        input[type="submit"] {
            background-color: #006400;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 6px;
            cursor: pointer;
            display: block;
            margin: auto;
        }
        .respuesta {
            margin-top: 30px;
            padding: 20px;
            background-color: #e9f5e9;
            border-radius: 6px;
            border-left: 5px solid #006400;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Asesor Legal TEDECO</h1>
        <form method="post">
            <label for="pregunta">Escribe tu pregunta legal:</label>
            <input type="text" id="pregunta" name="pregunta" required>
            <input type="submit" value="Consultar">
        </form>
        {% if respuesta %}
        <div class="respuesta">
            <strong>Respuesta:</strong><br>
            {{ respuesta }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    respuesta = ""
    if request.method == "POST":
        pregunta = request.form["pregunta"]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asesor legal experto en Ecuador en IESS, seguros y derechos de los ciudadanos. Responde con precisión, empatía y profesionalismo."},
                {"role": "user", "content": pregunta}
            ]
        )
        respuesta = completion.choices[0].message.content
    return render_template_string(HTML, respuesta=respuesta)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
