from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Lista do przechowywania otrzymanych danych
received_data = []

# Template HTML dla strony głównej
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Data Inspector</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        textarea { height: 100px; resize: vertical; }
        button { background-color: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .info { background-color: #e7f3ff; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
        .nav { text-align: center; margin-bottom: 30px; }
        .nav a { color: #007bff; text-decoration: none; margin: 0 15px; font-weight: bold; }
        .nav a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">Wyślij dane</a>
            <a href="/view-data">Podgląd danych</a>
            <a href="/clear-data">Wyczyść dane</a>
        </div>
        
        <h1>📊 Data Inspector</h1>
        
        <div class="info">
            <strong>Informacje o endpointach:</strong><br>
            • <code>POST /api/data</code> - przyjmuje dowolne dane JSON<br>
            • <code>GET /view-data</code> - wyświetla wszystkie otrzymane dane<br>
            • <code>GET /clear-data</code> - czyści wszystkie dane<br>
            • <code>GET /api/status</code> - status aplikacji
        </div>

        <h2>🔧 Test formularza</h2>
        <form method="POST" action="/api/data">
            <div class="form-group">
                <label for="name">Nazwa:</label>
                <input type="text" id="name" name="name" placeholder="Wprowadź nazwę">
            </div>
            
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" placeholder="Wprowadź email">
            </div>
            
            <div class="form-group">
                <label for="message">Wiadomość:</label>
                <textarea id="message" name="message" placeholder="Wprowadź wiadomość"></textarea>
            </div>
            
            <div class="form-group">
                <label for="type">Typ:</label>
                <select id="type" name="type">
                    <option value="test">Test</option>
                    <option value="feedback">Feedback</option>
                    <option value="bug">Bug Report</option>
                    <option value="other">Inne</option>
                </select>
            </div>
            
            <button type="submit">📤 Wyślij dane</button>
        </form>

        <h2>🚀 Test API (JavaScript)</h2>
        <button onclick="sendTestData()">Wyślij dane testowe przez JS</button>
        
        <script>
        function sendTestData() {
            const testData = {
                test: true,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                random_number: Math.floor(Math.random() * 1000),
                nested_object: {
                    level1: {
                        level2: "głęboko zagnieżdżone dane"
                    }
                },
                array_data: ["element1", "element2", "element3"]
            };
            
            fetch('/api/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(testData)
            })
            .then(response => response.json())
            .then(data => {
                alert('Dane wysłane! Status: ' + data.status);
            })
            .catch(error => {
                alert('Błąd: ' + error);
            });
        }
        </script>
    </div>
</body>
</html>
'''

# Template dla podglądu danych
VIEW_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Podgląd danych - Data Inspector</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .nav { text-align: center; margin-bottom: 30px; }
        .nav a { color: #007bff; text-decoration: none; margin: 0 15px; font-weight: bold; }
        .nav a:hover { text-decoration: underline; }
        .data-item { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; margin-bottom: 20px; padding: 20px; }
        .timestamp { color: #6c757d; font-size: 0.9em; margin-bottom: 10px; }
        .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; margin-bottom: 10px; }
        .method-GET { background-color: #d4edda; color: #155724; }
        .method-POST { background-color: #cce7ff; color: #004085; }
        .method-PUT { background-color: #fff3cd; color: #856404; }
        .method-DELETE { background-color: #f8d7da; color: #721c24; }
        .headers { background-color: #e9ecef; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .data-content { background-color: white; padding: 15px; border-radius: 4px; border-left: 4px solid #007bff; }
        .json-data { background-color: #f8f8f8; padding: 10px; border-radius: 4px; font-family: 'Courier New', monospace; white-space: pre-wrap; overflow-x: auto; }
        .no-data { text-align: center; color: #6c757d; padding: 40px; }
        .stats { background-color: #e7f3ff; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">Wyślij dane</a>
            <a href="/view-data">Podgląd danych</a>
            <a href="/clear-data">Wyczyść dane</a>
        </div>
        
        <h1>📋 Podgląd otrzymanych danych</h1>
        
        <div class="stats">
            <strong>Statystyki:</strong> Otrzymano {{ data_count }} żądań
        </div>
        
        {% if data_items %}
            {% for item in data_items %}
            <div class="data-item">
                <div class="timestamp">🕒 {{ item.timestamp }}</div>
                <div class="method method-{{ item.method }}">{{ item.method }}</div>
                <strong>{{ item.url }}</strong>
                
                {% if item.headers %}
                <div class="headers">
                    <strong>Headers:</strong><br>
                    {% for key, value in item.headers.items() %}
                    <strong>{{ key }}:</strong> {{ value }}<br>
                    {% endfor %}
                </div>
                {% endif %}
                
                <div class="data-content">
                    <strong>Otrzymane dane:</strong>
                    <div class="json-data">{{ item.data_formatted }}</div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="no-data">
                <h3>🔍 Brak danych</h3>
                <p>Nie otrzymano jeszcze żadnych danych. Wyślij coś przez formularz lub API!</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    """Strona główna z formularzem"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/api/data', methods=['POST', 'GET', 'PUT', 'DELETE'])
def receive_data():
    """Endpoint do przyjmowania dowolnych danych"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Zbierz wszystkie możliwe dane z żądania
    data_entry = {
        'timestamp': timestamp,
        'method': request.method,
        'url': request.url,
        'endpoint': request.endpoint,
        'remote_addr': request.remote_addr,
        'headers': dict(request.headers),
        'args': dict(request.args),  # Query parameters
        'form': dict(request.form),  # Form data
        'files': [f.filename for f in request.files.values()],  # Uploaded files
    }
    
    # Próbuj pobrać dane JSON
    try:
        if request.is_json:
            data_entry['json'] = request.get_json()
        else:
            data_entry['json'] = None
    except:
        data_entry['json'] = None
    
    # Próbuj pobrać raw data
    try:
        raw_data = request.get_data(as_text=True)
        if raw_data:
            data_entry['raw_data'] = raw_data
    except:
        data_entry['raw_data'] = None
    
    # Sformatuj dane do wyświetlenia
    data_entry['data_formatted'] = json.dumps(data_entry, indent=2, ensure_ascii=False, default=str)
    
    # Dodaj do listy
    received_data.append(data_entry)
    
    # Zwróć odpowiedź
    response_data = {
        'status': 'success',
        'message': 'Dane otrzymane pomyślnie',
        'timestamp': timestamp,
        'data_id': len(received_data),
        'received_fields': list(data_entry.keys())
    }
    
    # Jeśli to żądanie z formularza, przekieruj z komunikatem
    if request.form:
        return f'''
        <html>
        <head><meta charset="utf-8"></head>
        <body style="font-family: Arial; margin: 40px; text-align: center;">
            <h2>✅ Dane wysłane pomyślnie!</h2>
            <p>Timestamp: {timestamp}</p>
            <p>ID: {len(received_data)}</p>
            <a href="/" style="color: #007bff;">← Powrót do formularza</a> | 
            <a href="/view-data" style="color: #007bff;">Podgląd danych →</a>
        </body>
        </html>
        '''
    
    return jsonify(response_data)

@app.route('/view-data')
def view_data():
    """Strona z podglądem wszystkich otrzymanych danych"""
    return render_template_string(VIEW_TEMPLATE, 
                                data_items=list(reversed(received_data)),  # Najnowsze na górze
                                data_count=len(received_data))

@app.route('/clear-data')
def clear_data():
    """Wyczyść wszystkie dane"""
    global received_data
    count = len(received_data)
    received_data = []
    
    return f'''
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial; margin: 40px; text-align: center;">
        <h2>🗑️ Dane wyczyszczone</h2>
        <p>Usunięto {count} elementów</p>
        <a href="/" style="color: #007bff;">← Powrót do formularza</a> | 
        <a href="/view-data" style="color: #007bff;">Podgląd danych →</a>
    </body>
    </html>
    '''

@app.route('/api/status')
def status():
    """Status aplikacji"""
    return jsonify({
        'status': 'running',
        'data_count': len(received_data),
        'last_request': received_data[-1]['timestamp'] if received_data else None,
        'endpoints': [
            'POST /api/data - przyjmuje dane',
            'GET /view-data - podgląd danych', 
            'GET /clear-data - czyści dane',
            'GET /api/status - ten endpoint'
        ]
    })

if __name__ == '__main__':
    print("🚀 Uruchamianie Data Inspector...")
    print("📡 Dostępne endpointy:")
    print("   • http://localhost:5000/ - Strona główna")
    print("   • http://localhost:5000/api/data - Endpoint do wysyłania danych")
    print("   • http://localhost:5000/view-data - Podgląd otrzymanych danych")
    print("   • http://localhost:5000/clear-data - Wyczyść dane")
    print("   • http://localhost:5000/api/status - Status aplikacji")
    print("\n💡 Możesz wysyłać dane przez:")
    print("   • Formularz na stronie głównej")
    print("   • POST żądania na /api/data")
    print("   • curl, Postman, lub inne narzędzia")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
