from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120),nullable=False)

    favoritos_personajes: Mapped[list["TablaIntermediaDePersonajesFavoritos"]] = db.relationship('TablaIntermediaDePersonajesFavoritos',  back_populates="user", cascade="all, delete-orphan")
    favoritos_planetas:Mapped[list["TablaIntermediaDePlanetasFavoritos"]] = db.relationship('TablaIntermediaDePlanetasFavoritos', back_populates="user", cascade="all, delete-orphan")   
    
    def serialize(self):
        return {
            "id": self.id,
            "username":self.username,
            "email": self.email,
            # do not serialize the password, its a security breach

        }

class Planets(db.Model):
    __tablename__="planets"

    id: Mapped[int] = mapped_column (primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    clima: Mapped[str] = mapped_column(String(80), nullable=True)

    usuarios_que_favearon_planeta: Mapped[list["TablaIntermediaDePlanetasFavoritos"]] = db.relationship("TablaIntermediaDePlanetasFavoritos", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "clima": self.clima
        }

class Characters(db.Model):
    __tablename__="characters"

    id: Mapped[int] = mapped_column (primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    color_de_ojos: Mapped[str] = mapped_column(String(80), nullable=True)

    usuarios_que_favearon_personaje: Mapped[list["TablaIntermediaDePersonajesFavoritos"]] = db.relationship("TablaIntermediaDePersonajesFavoritos", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "color_de_ojos": self.color_de_ojos
        }

class TablaIntermediaDePersonajesFavoritos(db.Model):
    __tablename__="tabla_intermedia_de_personajes_favoritos"

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('characters.id', primary_key=True))

    user = db.relationship("User", back_populates="favoritos_personajes")
    character = db.relationship("Characters", back_populates="usuarios_que_favearon_personaje")

    def serialize(self):
        return{
            "user_id":self.user_id,
            "character_id":self.character_id,
        }

class TablaIntermediaDePlanetasFavoritos(db.Model):
    __tablename__="tabla_intermedia_de_planetas_favoritos"

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), primary_key=True)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey('planets.id', primary_key=True))

    user= db.relationship("User", back_populates="favoritos_planetas")
    planet = db.relationship("Planets", back_populates="usuarios_que_favearon_planeta")

    def serialize(self):
        return{
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }