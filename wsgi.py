from resized.app import create_app
from resized.settings import Settings

app = create_app(Settings)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
