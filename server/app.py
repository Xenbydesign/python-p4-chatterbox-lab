from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALACHEMY_ECHO"] = True
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        message = [
            message.to_dict() for message in Message.query.order_by("created_at")
        ]
        response = make_response(message, 200)
        return response

    else:
        data = request.json
        new_message = Message(body=data.get("body"), username=data.get("username"))

        db.session.add(new_message)
        db.session.commit()

        return new_message.to_dict(), 201


# @app.route("/messages")
# def messages():
#     return render_template("index.html")


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = db.session.get(Message, id)
    if message:
        if request.method == "DELETE":
            db.session.delete(message)
            db.session.commit()
            return "", 204
        else:
            data = request.json
            for attr, value in data.items():
                setattr(message, attr, value)

            db.session.commit()
            return message.to_dict(), 200
    else:
        return {"error": f"Message not found with id #{id}"}, 404


if __name__ == "__main__":
    app.run(port=5555, debug=True)
