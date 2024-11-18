from create_app import create_app
from api.routes_api import api


app = create_app()

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
