import os

from flask import Flask, jsonify

from .extensions import cache, db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-secret"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-only-jwt-secret"),
        JWT_EXPIRES_MINUTES=int(os.getenv("JWT_EXPIRES_MINUTES", "60")),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://petshop:petshop@localhost:5432/petshop",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE="RedisCache" if os.getenv("REDIS_HOST") else "SimpleCache",
        CACHE_REDIS_HOST=os.getenv("REDIS_HOST", "localhost"),
        CACHE_REDIS_PORT=int(os.getenv("REDIS_PORT", "6379")),
        CACHE_REDIS_PASSWORD=os.getenv("REDIS_PASSWORD"),
        CACHE_REDIS_DB=0,
        CACHE_OPTIONS=(
            {"username": os.getenv("REDIS_USERNAME")}
            if os.getenv("REDIS_USERNAME")
            else {}
        ),
        CACHE_DEFAULT_TIMEOUT=300,
        )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    cache.init_app(app)

    from .commands import register_commands
    register_commands(app)

    from .auth.routes import auth_bp
    from .carts.routes import carts_bp
    from .invoices.routes import invoices_bp
    from .products.routes import products_bp
    from .users.routes import users_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(carts_bp, url_prefix="/api/carts")
    app.register_blueprint(invoices_bp, url_prefix="/api/invoices")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error="Recurso no encontrado"), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify(error="Método no permitido"), 405

    return app
