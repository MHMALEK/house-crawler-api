from flask import Blueprint, request, jsonify

# from database import User, db_session
import requests
from firebase_admin import db


bp = Blueprint("auth", __name__, url_prefix="/users")


@bp.route("/register", methods=["POST"])
def register():
    chat_id = request.json.get("chat_id")
    ref = db.reference("chat_ids")
    ref.child(str(chat_id)).set(True)
    return {"chat_id": chat_id}, 201


@bp.route("/list", methods=["GET"])
def list_users():
    ref = db.reference("chat_ids")
    chat_ids = ref.get()
    if chat_ids is None:
        return {"chat_ids": []}
    else:
        return {"chat_ids": list(chat_ids.keys())}


@bp.route("/<chat_id>", methods=["GET"])
def get_single_user(chat_id):
    if chat_id is None:
        return jsonify({"error": "Missing chat_id parameter"}), 400
    ref = db.reference("chat_ids")
    user = ref.child(chat_id).get()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"chat_id": chat_id}), 200


@bp.route("/<chat_id>", methods=["DELETE"])
def remove_user(chat_id):
    chat_id_to_remove = chat_id
    ref = db.reference("chat_ids")
    ref.child(chat_id_to_remove).delete()
    return {"removed_chat_id": chat_id_to_remove}, 200


@bp.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "An error occurred, please try again later"}), 500
