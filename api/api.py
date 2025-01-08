from flask import Flask, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from service.deepface_my import detect_and_crop_faces, get_img_embeddings
import os

app = Flask(__name__)

output_folder = os.path.join(app.root_path, "..", "deepface-output")  # 使用动态路径


# 在图片中截取人脸
@app.route("/detect_faces", methods=["POST"])
def detect_faces():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        temp_image_path = os.path.join("/tmp", filename)
        file.save(temp_image_path)
        saved_faces = detect_and_crop_faces(temp_image_path, output_folder)
        if not saved_faces:
            return jsonify({"msg": "No faces detected", "size": 0}), 200
        return jsonify({"msg": saved_faces, "size": len(saved_faces)}), 200


# 获取人脸图片
@app.route("/get_face_image/<filename>", methods=["GET"])
def get_face_image(filename):
    image_path = os.path.join(output_folder, filename)

    if not os.path.exists(image_path):
        abort(404, description="File not found")

    return send_file(image_path, mimetype="image/jpeg")


# 获取图片的特征向量
@app.route("/embeddings", methods=["POST"])
def embeddings():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        temp_image_path = os.path.join("/tmp", filename)
        file.save(temp_image_path)
        embeddings = get_img_embeddings(temp_image_path, output_folder)
        return jsonify({"msg": "success", "embeddings": embeddings}), 200
    else:
        return jsonify({"message": "No image uploaded"}), 500
