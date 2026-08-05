import click
from flask.cli import with_appcontext

from .extensions import db
from .models import User


def register_commands(app):
    @app.cli.command("init-db")
    @with_appcontext
    def init_db():
        """Crea las tablas mediante SQLAlchemy."""
        db.create_all()
        click.echo("Base de datos inicializada.")

    @app.cli.command("create-admin")
    @click.option("--name", prompt=True)
    @click.option("--email", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    @with_appcontext
    def create_admin(name, email, password):
        """Crea el primer administrador mediante el ORM."""
        if len(password) < 8:
            raise click.ClickException("La contraseña debe tener al menos 8 caracteres")
        normalized_email = email.strip().lower()
        if db.session.scalar(db.select(User).where(User.email == normalized_email)):
            raise click.ClickException("El correo ya existe")
        user = User(name=name.strip(), email=normalized_email, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Administrador {normalized_email} creado.")

