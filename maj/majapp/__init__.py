from flask import Flask, redirect


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # a simple page that says hello

    @app.route('/')
    def top():
        return redirect('http://localhost:8000/search')

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import login
    app.register_blueprint(login.bp)

    from . import search
    app.register_blueprint(search.bp)

    from . import favorite
    app.register_blueprint(favorite.bp)

    from . import favorite_del
    app.register_blueprint(favorite_del.bp)

    from . import detail
    app.register_blueprint(detail.bp)

    from . import register
    app.register_blueprint(register.bp)

    from . import user_register
    app.register_blueprint(user_register.bp)

    return app
