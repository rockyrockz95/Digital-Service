from . import db
from sqlalchemy import CheckConstraint
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note")


class Client(db.Model, UserMixin):
    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
        }


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "data": self.data,
            "date": self.date,
        }

class Client(db.Model, UserMixin):
    clientID = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    # one account per email
    client_email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    # case of family members
    address = db.Column(db.VARCHAR(50), unique=False)
    client_password = db.Column(db.VARCHAR(15), unique=False, nullable=False)
    # TODO: look up lazy
    appointments = db.relationship("Appointment", backref="client", lazy=True)
    reviews = db.relationship("Review", backref="client", lazy=True)

    def to_json(self):
        return {
            "clientID": self.clientID,
            "clientName": self.client_name,
            "clientEmail": self.client_email,
            "address": self.address,
            "password": self.password,
        }


class Technician(db.Model, UserMixin):
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

    appointments = db.relationship("Appointment", backref="tech", lazy=True)
    reviews = db.relationship("Review", backref="tech", lazy=True)
    schedules = db.relationship("Schedule", backref="tech", lazy=True)
    
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


# one to many with Client, Technician
# one to many with Client, Technician
class Appointment(db.Model):
    appointmentID = db.Column(db.Integer, primary_key=True)
    clientID = db.Column(db.Integer, db.ForeignKey("client.clientID"))
    techID = db.Column(db.Integer, db.ForeignKey("technician.techID"))
    clientID = db.Column(db.Integer, db.ForeignKey("client.clientID"))
    techID = db.Column(db.Integer, db.ForeignKey("technician.techID"))
    purpose = db.Column(db.VARCHAR(30), nullable=False, unique=False)
    price = db.Column(db.Integer, nullable=False, unique=False)
    # might combine into dateTime
    day = db.Column(db.VARCHAR(20), nullable=False, unique=False)
    # TODO: day and time combination should be unique; probably should combine
    # TODO: check if in utc
    time = db.Column(db.DateTime(timezone=True), nullable=False, unique=False)
    additional_comment = db.Column(db.VARCHAR(200), nullable=True, unique=False)

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


# one to many with technician
# one to many with technician
class Schedule(db.Model):
    scheduleID = db.Column(db.Integer, primary_key=True)
    techID = db.Column(db.Integer, db.ForeignKey("technician.techID"))
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


# one to many with client, tech
class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    clientID = db.Column(db.Integer, db.ForeignKey("client.clientID"))
    techID = db.Column(db.Integer, db.ForeignKey("technician.techID"))
    review_content = db.Column(db.VARCHAR(250), nullable=True, unique=False)
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
