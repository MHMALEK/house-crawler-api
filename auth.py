from flask import Blueprint, request, jsonify

# from database import User, db_session
import requests
from firebase_admin import db


bp = Blueprint("auth", __name__, url_prefix="/users")


@bp.route("/register", methods=["POST"])
def register():
    chat_id = request.json.get("chat_id")
    ref = db.reference('chat_ids')
    ref.child(chat_id).set(True)
    return {"chat_id": chat_id}, 201


@bp.route("/list", methods=["GET"])
def list_users():
    ref = db.reference('chat_ids')
    chat_ids = ref.get()
    return {"chat_ids": list(chat_ids.keys())}


@bp.route("/<chat_id>", methods=["DELETE"])
def remove_user(chat_id):
    chat_id_to_remove = chat_id
    ref = db.reference('chat_ids')
    ref.child(chat_id_to_remove).delete()
    return {"removed_chat_id": chat_id_to_remove}, 200


@bp.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "An error occurred, please try again later"}), 500
