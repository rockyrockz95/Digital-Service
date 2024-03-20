from sqlalchemy import CheckConstraint
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note")


class Client(db.Model):
    clientID = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    # one account per email
    client_email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    # case of family members
    address = db.Column(db.VARCHAR(50), unique=False)
    client_password = db.Column(db.VARCHAR(15), unique=False, nullable=False)

    # turns fields into dictionary that can be converted into JSON (JS object notation)
    # api takes and sends JSON objects
    # JSON conventione: camelCase
    # Python convention: snake_case
    def to_json(self):
        return {
            "clientID": self.clientID,
            "clientName": self.client_name,
            "clientEmail": self.client_email,
            "address": self.address,
            "password": self.password,
        }


class Technician(db.Model):
    techID = db.Column(db.Integer, primary_key=True)
    tech_name = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    # TODO: change if causes problems; should be a N/A option
    specialization = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    # case of same company/store location
    location = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    company = db.Column(db.VARCHAR(15), unique=False, nullable=False)
    # technicians have to login to view bookings
    tech_email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    tech_password = db.Column(db.VARCHAR(50), unique=False, nullable=False)

    # turns fields into dictionary that can be converted into JSON (JS object notation)
    # api takes and sends JSON objects
    # JSON conventione: camelCase
    # Python convention: snake_case
    def to_json(self):
        return {
            "techID": self.techID,
            "techName": self.tech_name,
            "specialization": self.specialization,
            "company": self.company,
            "techEmail": self.tech_email,
            "location": self.location,
            "password": self.tech_password,
        }


class Appointment(db.Model):
    appointmentID = db.Column(db.Integer, primary_key=True)
    clientID = db.Column(db.Integer, db.ForeignKey(Client.clientID))
    techID = db.Column(db.Integer, db.ForeignKey(Technician.techID))
    purpose = db.Column(db.VARCHAR(30), nullable=False, unique=False)
    price = db.Column(db.Integer, nullable=False, unique=False)
    # might combine into dateTime
    day = db.Column(db.VARCHAR(20), nullable=False, unique=False)
    # timezone aware column
    # TODO: day and time combination should be unique; probably should combine
    time = db.Column(db.DateTime(timezone=True), nullable=False, unique=False)
    additional_comment = db.Column(db.String, nullable=True, unique=False)

    def to_json(self):
        return {
            "appointmentID": self.appointmentID,
            "clientID": self.clientID,
            "techID": self.techID,
            "purpose": self.purpose,
            "price": self.price,
            "day": self.day,
            "time": self.time,
            "additional_comment": self.additional_comment,
        }


class Schedule(db.Model):
    scheduleID = db.Column(db.Integer, primary_key=True)
    techID = db.Column(db.Integer, db.ForeignKey(Technician.techID))
    day = db.Column(db.VARCHAR(20), nullable=False, unique=False)
    # TODO: find a different time type for this
    startTime = db.Column(db.DateTime(timezone=True), nullable=False, unique=False)
    endTime = db.Column(db.DateTime(timezone=True), nullable=False, unique=False)

    def to_json(self):
        return {
            "scheduleID": self.scheduleID,
            "techID": self.techID,
            "day": self.day,
            "startTime": self.startTime,
            "endTime": self.endTime,
        }


class Review:
    reviewID = db.Column(db.Integer, primary_key=True)
    clientID = db.Column(db.Integer, db.ForeignKey(Client.clientID))
    techID = db.Column(db.Integer, db.ForeignKey(Technician.techID))
    review_content = db.Column(db.String, nullable=True, unique=False)
    # rating out of 5 stars
    rating = db.Column(
        db.Integer,
        CheckConstraint("rating <= 5", name="rating_max_limit"),
        nullable=False,
        unique=False,
    )

    def to_json(self):
        return {
            "reviewID": self.reviewID,
            "clientID": self.clientID,
            "techID": self.techID,
            "reviewContent": self.review_content,
            "rating": self.rating,
        }
