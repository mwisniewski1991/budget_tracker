from app import create_app
from os import environ

app = create_app()

if __name__ == '__main__':  
    PORT = environ.get('FLASK_PORT')
    app.run(debug = True, host='0.0.0.0', port=PORT)