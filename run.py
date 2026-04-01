#from == carpeta // import == variable

from app import app #esto solo funciona con archivo __init__

if __name__ == "__main__":
    app.run(debug=True)         