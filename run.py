from app import create_app
app = create_app()
# For development purposes only
if __name__ == '__main__':
    app.run(debug=True)