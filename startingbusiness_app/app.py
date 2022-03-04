from startingbusiness_app import create_app

from config import DevelopmentConfig

from flask_mail import Mail

app = create_app(DevelopmentConfig)


if __name__ == '__main__':
    mail = Mail(app)
    app.run()
