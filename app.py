from create_app import create_app

# Создаем экземпляр приложения
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
