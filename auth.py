from flask import Blueprint, request, jsonify
from database import User, db_session


bp = Blueprint("auth", __name__, url_prefix="/users")


@bp.route("/register", methods=["POST"])
def register():
    chat_id = request.json.get("chat_id")
    user = User.query.filter_by(chat_id=str(chat_id)).first()
    if user is None:
        new_user = User(chat_id=str(chat_id))
        db_session.add(new_user)
        db_session.commit()
        return jsonify({"message": "User created successfully!"}), 201

    return jsonify(
        {
            "id": user.id,
            "chat_id": user.chat_id,
        }
    )


@bp.route("/list", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify(
        {"users": [{"id": user.id, "chat_id": user.chat_id} for user in users]}
    )


@bp.route("/<chat_id>", methods=["GET"])
def get_single_user(chat_id):
    user = User.query.filter_by(chat_id=str(chat_id)).first()
    if user is not None:
        return jsonify(
            {
                "id": user.id,
                "chat_id": user.chat_id,
            }
        )
    else:
        return jsonify({"error": "User not found"}), 404


@bp.route("/<chat_id>", methods=["DELETE"])
def remove_user(chat_id):
    user = User.query.filter_by(chat_id=str(chat_id)).first()
    if user is not None:
        db_session.session.delete(user)
        db_session.session.commit()
        return jsonify({"message": "User removed successfully!"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@bp.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "An error occurred, please try again later"}), 500
