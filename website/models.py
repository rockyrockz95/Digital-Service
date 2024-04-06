from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note")


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


class ProviderSchedule(db.Model):
    __tablename__ = "ProviderSchedule"  # simplifies relationship declarations

    ScheduleID = db.Column(db.Integer, primary_key=True)
    Day = db.Column(db.DATE)
    StartTime = db.Column(db.DATETIME)
    EndTime = db.Column(db.DATETIME)

    Providers = db.relationship("Provider", backref="Schedule", lazy=True)

    def to_json(self):
        return {
            "ScheduleID": self.ScheduleID,
            "Day": self.Day,
            "Start": self.StartTime,
            "End": self.EndTime,
        }


class Provider(db.Model, UserMixin):
    __tablename__ = "Provider"

    ProviderID = db.Column(db.Integer, primary_key=True)
    ProviderSchedule = db.Column(
        db.Integer, db.ForeignKey("ProviderSchedule.ScheduleID")
    )
    Username = db.Column(db.VARCHAR(100))
    Password = db.Column(db.VARCHAR(64))
    Name = db.Column(db.VARCHAR(32))
    Industry = db.Column(db.VARCHAR(64))  # pet || nail
    Address = db.Column(db.VARCHAR(255))
    Email = db.Column(db.VARCHAR(64))
    Number = db.Column(db.BIGINT)
    Rating = db.Column(db.Integer)
    PriceRate = db.Column(db.Integer)
    Specialization = db.Column(db.VARCHAR(64))
    Company = db.Column(db.VARCHAR(64))

    PetAppointments = db.relationship("PetAppointment", backref="Provider", lazy=True)
    NailAppointments = db.relationship("NailAppointment", backref="Provider", lazy=True)
    Reviews = db.relationship("Review", backref="provider", lazy=True)

    def to_json(self):
        return {
            "id": self.ProviderID,
            "username": self.Username,
            "email": self.Email,
            "industry": self.Industry,
        }


# TODO: Check if the current user is a technician or client
# TODO: search the database if the current username is in the Technician or Client db, curr_user is: blank OR
# TODO: Add "ARE YOU TECHNICIAN or CLIENT option to the signup page"
# TODO: check if running this creates the EXACT same db as catcare db sql
class Customer(db.Model):
    __tablename__ = "Customer"

    CustomerID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.VARCHAR(100))
    Password = db.Column(db.VARCHAR(64))
    Name = db.Column(db.VARCHAR(32))
    Address = db.Column(db.VARCHAR(255))
    Email = db.Column(db.VARCHAR(64))
    Number = db.Column(db.BIGINT)

    NailAppointments = db.relationship("NailAppointment", backref="Customer", lazy=True)
    Pets = db.relationship("Pet", backref="customer", lazy=True)

    def to_json(self):
        return {
            "CustomerID": self.CustomerID,
            "CustomerName": self.Name,
            "CustomerEmail": self.Email,
        }


class Pet(db.Model):
    __tablename__ = "Pet"

    PetID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("Customer.CustomerID"))
    Name = db.Column(db.VARCHAR(64))
    Age = db.Column(db.Integer)
    Species = db.Column(db.VARCHAR(3))
    Breed = db.Column(db.VARCHAR(32))

    Appointments = db.relationship("PetAppointment", backref="Pet", lazy=True)

    def to_json(self):
        return {
            "PetID": self.PetID,
            "CustomerID": self.CustomerID,
            "Name": self.Name,
        }


class PetAppointment(db.Model):
    __tablename__ = "PetAppointment"

    AppointmentID = db.Column(db.Integer, primary_key=True)
    ProviderID = db.Column(db.Integer, db.ForeignKey("Provider.ProviderID"))
    PetID = db.Column(db.Integer, db.ForeignKey("Pet.PetID"))
    Status = db.Column(db.VARCHAR(32))
    BorrowDate = db.Column(db.DATETIME)
    ReturnDate = db.Column(db.DATETIME)

    def to_json(self):
        return {
            "AppointmentID": self.AppointmentID,
            "ProviderID": self.ProviderID,
            "BorrowDate": self.BorrowDate,
            "ReturnDate": self.ReturnDate,
        }


class NailAppointment(db.Model):
    __tablename__ = "NailAppointment"

    AppointmentID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("Customer.CustomerID"))
    ProviderID = db.Column(db.Integer, db.ForeignKey("Provider.ProviderID"))
    Status = db.Column(db.VARCHAR(32))
    StartTime = db.Column(db.DATETIME)
    EndTime = db.Column(db.DATETIME)

    def to_json(self):
        return {
            "AppointmentID": self.AppointmentID,
            "CustomerID": self.CustomerID,
            "ProviderID": self.ProviderID,
            "StartTime": self.StartTime,
            "EndTime": self.EndTime,
        }


class Review(db.Model):
    __tablename__ = "Review"

    ReviewID = db.Column(db.Integer, primary_key=True)
    ProviderID = db.Column(db.Integer, db.ForeignKey("Provider.ProviderID"))
    ServiceType = db.Column(db.VARCHAR(20))
    Rating = db.Column(db.Integer)
    Comment = db.Column(db.TEXT)

    def to_json(self):
        return {
            "ReviewID": self.ReviewID,
            "ProviderID": self.ProviderID,
            "ServiceType": self.ServiceType,
            "Rating": self.Rating,
        }
