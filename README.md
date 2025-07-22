# 📊 Data Inspector

Prosty projekt Flask do weryfikacji danych wysyłanych do Twojej aplikacji. Idealny do debugowania i testowania API.

## 🚀 Szybki start

### 1. Instalacja

```bash
# Sklonuj lub pobierz pliki projektu
# Zainstaluj wymagane biblioteki
pip install -r requirements.txt
```

### 2. Uruchomienie

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: **http://localhost:5000**

## 📡 Dostępne endpointy

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/` | GET | Strona główna z formularzem testowym |
| `/api/data` | POST/GET/PUT/DELETE | Główny endpoint do przyjmowania danych |
| `/view-data` | GET | Podgląd wszystkich otrzymanych danych |
| `/clear-data` | GET | Wyczyść wszystkie zebrane dane |
| `/api/status` | GET | Status aplikacji i statystyki |

## 🔧 Funkcjonalności

### ✅ Co aplikacja zapisuje:
- **Timestamp** - dokładny czas otrzymania żądania
- **Metodę HTTP** (GET, POST, PUT, DELETE)
- **URL i parametry** zapytania
- **Headers** - wszystkie nagłówki HTTP
- **Dane JSON** - jeśli wysłane w formacie JSON
- **Dane formularza** - jeśli wysłane przez formularz
- **Raw data** - surowe dane żądania
- **Adres IP** klienta
- **Informacje o plikach** (jeśli załączone)

### 🎯 Jak używać:

1. **Formularz testowy** - przejdź na http://localhost:5000 i użyj formularza
2. **JavaScript API** - kliknij przycisk "Wyślij dane testowe przez JS"
3. **Zewnętrzne API** - używaj curl, Postman lub własnych aplikacji
4. **Podgląd danych** - sprawdź http://localhost:5000/view-data

## 💡 Przykłady testowania

### cURL:
```bash
# Podstawowy POST z JSON
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "data": "przykładowe dane"}'

# Formularz
curl -X POST http://localhost:5000/api/data \
  -d "name=Jan&email=jan@example.com"
```

### Python:
```python
import requests

# JSON
response = requests.post('http://localhost:5000/api/data', 
                        json={'test': 'python data'})

# Formularz
response = requests.post('http://localhost:5000/api/data',
                        data={'name': 'Python User'})
```

### JavaScript:
```javascript
fetch('/api/data', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({test: 'js data'})
})
```

## 🛠️ Dodatkowe informacje

- **Dane w pamięci** - wszystkie dane są przechowywane w pamięci RAM (znikają po restarcie)
- **Debug mode** - aplikacja działa w trybie debug z auto-reload
- **Cross-platform** - działa na Windows, Mac, Linux
- **Lightweight** - minimalne zależności, szybkie uruchomienie

## 🔍 Zastosowania

- **Debugowanie API** - sprawdź co dokładnie wysyła Twoja aplikacja
- **Testowanie integracji** - weryfikuj komunikację między systemami  
- **Prototypowanie** - szybkie testowanie konceptów API
- **Edukacja** - nauka jak działają żądania HTTP
- **Monitoring** - podgląd ruchu w aplikacji

## ⚙️ Konfiguracja

Możesz zmienić port i host w pliku `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🛡️ Bezpieczeństwo

⚠️ **Uwaga**: To narzędzie jest przeznaczone do **celów deweloperskich i testowych**. 
Nie używaj go w środowisku produkcyjnym bez odpowiednich zabezpieczeń!
