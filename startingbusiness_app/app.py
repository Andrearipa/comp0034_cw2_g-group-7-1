from startingbusiness_app import create_app, config
from startingbusiness_app.config import DevelopmentConfig

app = create_app(config.DevelopmentConfig)

'''
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!' '''


if __name__ == '__main__':
    app.run()
