from startingbusiness_app import create_app

from config import DevelopmentConfig

from flask_mail import Mail

app = create_app(DevelopmentConfig)
# mail = Mail(app)

if __name__ == '__main__':
    app.run()
