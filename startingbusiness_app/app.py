from startingbusiness_app import create_app, config

app = create_app(config.DevelopmentConfig)

'''app.config['TESTING'] = True
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')'''


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
