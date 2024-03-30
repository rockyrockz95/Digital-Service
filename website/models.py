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


class Provider(db.Model, UserMixin):
    ProviderID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.VARCHAR(100))
    Password = db.Column(db.VARCHAR(64))
    Name = db.Column(db.VARCHAR(32))
    Industry = db.Column(db.VARCHAR(10))  # pet || nail
    Address = db.Column(db.VARCHAR(255))
    Email = db.Column(db.VARCHAR(64))
    Number = db.Column(db.BIGINT)
    Rating = db.Column(db.Integer)
    PriceRate = db.Column(db.Integer)
    Specialization = db.Column(db.VARCHAR(64))
    Company = db.Column(db.VARCHAR(100))

    Appointments = db.relationship("Appointment", backref="provider", lazy=True)
    Schedules = db.relationship("Schedule", backref="provider", lazy=True)

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
    CustomerID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.VARCHAR(100))
    Password = db.Column(db.VARCHAR(64))
    Name = db.Column(db.VARCHAR(32))
    Address = db.Column(db.VARCHAR(255))
    Email = db.Column(db.VARCHAR(64))
    Number = db.Column(db.BIGINT)

    Appointments = db.relationship("Appointment", backref="customer", lazy=True)
    Pets = db.relationship("Pet", backref="customer", lazy=True)

    def to_json(self):
        return {
            "CustomerID": self.CustomerID,
            "CustomerName": self.Name,
            "CustomerEmail": self.Email,
            "Address": self.Address,
            "Password": self.Password,
        }


# TODO: Consider reserved id for no pets (ie -1)
class Pet(db.Model):
    PetID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("customer.CustomerID"))
    Name = db.Column(db.VARCHAR(64))
    Age = db.Column(db.Integer)
    Species = db.Column(db.VARCHAR(3))
    Breed = db.Column(db.VARCHAR(32))

    Appointments = db.relationship("Appointment", backref="pet", lazy=True)

    def to_json(self):
        return {
            "PetID": self.PetID,
            "CustomerID": self.CustomerID,
            "Name": self.Name,
            "Breed": self.Breed,
        }


class Schedule(db.Model):
    ScheduleID = db.Column(db.Integer, primary_key=True)
    ProviderID = db.Column(db.Integer, db.ForeignKey("provider.ProviderID"))
    Day = db.Column(db.DATE)
    StartTime = db.Column(db.DATETIME)
    EndTime = db.Column(db.DATETIME)


class Service(db.Model):
    ServiceID = db.Column(db.Integer, primary_key=True)
    ServiceType = db.Column(db.VARCHAR(64))
    PriceRate = db.Column(db.Integer)

    Appointments = db.relationship("Appointment", backref="service", lazy=True)

    def to_json(self):
        return {
            "ServiceID": self.ServiceID,
            "ServiceType": self.ServiceType,
            "PriceRate": self.PriceRate,
        }


# TODO: GET GROUP FEEDBACK
class Appointment(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True)
    ScheduleID = db.Column(db.Integer, db.ForeignKey("schedule.ScheduleID"))
    CustomerID = db.Column(db.Integer, db.ForeignKey("customer.CustomerID"))
    ProviderID = db.Column(db.Integer, db.ForeignKey("provider.ProviderID"))
    PetID = db.Column(db.Integer, db.ForeignKey("pet.PetID"))
    ServiceID = db.Column(db.Integer, db.ForeignKey("service.ServiceID"))
    Type = db.Column(db.VARCHAR(10))  # pet || nail
    Status = db.Column(db.VARCHAR(32))
    BorrowDate = db.Column(db.DATETIME)
    ReturnDate = db.Column(db.DATETIME)
    Cost = db.Column(db.Integer)

    def to_json(self):
        return {
            "AppointmentID": self.AppointmentID,
            "CustomerID": self.CustomerID,
            "ProviderID": self.ProviderID,
            "ScheduleID": self.ScheduleID,
            "ServiceID": self.ServiceID,
            "StartTime": self.BorrowDate,
            "EndTime": self.ReturnDate,
        }
