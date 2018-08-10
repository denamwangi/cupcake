from flask_sqlalchemy import SQLAlchemy
# from json import dumps
from datetime import datetime

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """A user of the app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    primary_join_str = "and_(User.user_id==UserCupcake.user_id, UserCupcake.role == 'recipient')"
    secondary_join_str = "UserCupcake.cupcake_id==Cupcake.cupcake_id"
    cupcakes_received = db.relationship("Cupcake",
                                        secondary="usercupcakes",
                                        primaryjoin=primary_join_str,
                                        secondaryjoin=secondary_join_str,
                                        backref="recipients")
    primary_join_str = "and_(User.user_id==UserCupcake.user_id, UserCupcake.role == 'sender')"
    secondary_join_str = "UserCupcake.cupcake_id==Cupcake.cupcake_id"
    cupcakes_sent = db.relationship("Cupcake",
                                    secondary="usercupcakes",
                                    primaryjoin=primary_join_str,
                                    secondaryjoin=secondary_join_str,
                                    backref=db.backref("sender", uselist=False))

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<User {name} id: {id}>"
        return repr_str.format(name=self.name,
                               id=self.user_id)


class UserCupcake(db.Model):
    """An association table between Users and Cupcakes"""

    __tablename__ = "usercupcakes"

    usercupcake_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    role = db.Column(db.String(16))  # "recipient" or "sender"
    cupcake_id = db.Column(db.Integer,
                           db.ForeignKey("cupcakes.cupcake_id"),
                           nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<UserCupcake id: {id} user_id: {user_id} cupcake_id: {cupcake_id} role: {role}>"
        return repr_str.format(id=self.usercupcake_id,
                               user_id=self.user_id,
                               cupcake_id=self.cupcake_id,
                               role=self.role)

    @staticmethod
    def mark_sender(cupcake, sender):
        """A convenience method since SQLAlchemy won't fill in the data at
           creation time based on the relationships defined in the User class.
        """

        # get the UserCupcake record in question, update it, and save it
        usercupcake = (UserCupcake
                       .query
                       .filter(UserCupcake.cupcake_id == cupcake.cupcake_id,
                               UserCupcake.user_id == sender.user_id)
                       .first())
        usercupcake.role = "sender"
        db.session.commit()

    @staticmethod
    def mark_recipients(cupcake, recipients):
        """A convenience method since SQLAlchemy won't fill in the data at
           creation time based on the relationships defined in the User class.
        """

        # get the UserCupcake records in question, update them, and save them
        for recipient in recipients:
            usercupcake = (UserCupcake
                           .query
                           .filter(UserCupcake.cupcake_id == cupcake.cupcake_id,
                                   UserCupcake.user_id == recipient.user_id)
                           .first())
            usercupcake.role = "recipient"
        db.session.commit()


class Cupcake(db.Model):
    """A cupcake"""

    __tablename__ = "cupcakes"

    cupcake_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    reason = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<Cupcake id: {id} sender: {sender} recipients: {recipients} reason: {reason}>"
        return repr_str.format(id=self.cupcake_id,
                               sender=self.sender.name,
                               recipients=[r.name for r in self.recipients],
                               reason=self.reason)

    @classmethod
    def make_cupcake(cls, reason, sender, recipients):
        """A convenience method for making cupcakes, since the UserCupcakes
           have to be updated manually in order for sender/recipient roles
           to get recorded. Returns the cupcake already committed to the DB."""

        # make sure recipients were passed in as a list, and wrap if not
        if not isinstance(recipients, list):
            recipients = [recipients]

        cupcake = cls(reason=reason,
                      sender=sender,
                      recipients=recipients)
        db.session.add(cupcake)
        db.session.commit()
        UserCupcake.mark_sender(cupcake, sender)
        UserCupcake.mark_recipients(cupcake, recipients)

        return cupcake


##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///cupcakes"):
    """Connect the database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    # create a fake flask app, so that we can talk to the database by running
    # this file directly
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
