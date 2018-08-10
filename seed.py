from model import db, connect_to_db, User, Cupcake, UserCupcake


def load_users():
    """Add sample users to the DB"""

    for user in ["Katie", "Dena", "Maya", "Kiko", "Carol"]:
        new_user = User(name=user,
                        email="{user}@gmail.com".format(user=user.lower()),
                        password=user)
        db.session.add(new_user)

    db.session.commit()
    print "users added"


# TODO add more
def load_cupcakes():
    """Add sample cupcakes to the DB"""

    katie, dena, maya, kiko, carol = User.query.all()
    Cupcake.make_cupcake("being awesome", katie, [dena, carol])
    Cupcake.make_cupcake("doing the thing", dena, kiko)
    Cupcake.make_cupcake("rooting for the Sox", katie, [dena, maya])

    print "cupcakes added"


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)

    db.create_all()
    load_users()
    load_cupcakes()
