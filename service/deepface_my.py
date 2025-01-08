from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import os
import time
import deepface.commons.image_utils as deepface_image_utils


def detect_and_crop_faces(image_path, output_folder):
    # 检查输出文件夹是否存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 加载图片
    image = cv2.imread(image_path)
    if image is None:
        print("无法加载图片，请检查路径")
        return

    try:
        # 使用 DeepFace 的 extract_faces 方法
        faces = DeepFace.extract_faces(
            img_path=image_path,
            detector_backend="mtcnn",  # 更强大的检测器
            enforce_detection=False,  # 避免抛出未检测到人脸的异常
        )

        # 如果没有检测到人脸，打印提示信息
        if len(faces) == 0 or faces[0]["confidence"] == 0:
            print(f"未检测到人脸：{image_path}")
            return

        # 获取图片的文件名（不含路径和扩展名）
        base_filename = os.path.splitext(os.path.basename(image_path))[0]

        # 遍历检测到的人脸并保存
        saved_faces = []
        for i, face in enumerate(faces):
            # 转换为 uint8 格式
            face_array = (face["face"] * 255).astype("uint8")

            face_array = enhance_face(face_array)
            # 获取时间戳
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # 确定保存路径：文件名 + 时间戳 + 索引
            out_name = f"{base_filename}_{timestamp}_{i}.jpg"
            output_path = os.path.join(output_folder, out_name)

            # 保存裁剪后的人脸图片
            cv2.imwrite(output_path, face_array)
            print(f"人脸已保存到: {output_path}")
            saved_faces.append(out_name)
        return saved_faces
    except Exception as e:
        print(f"人脸检测失败：{e}")


def enhance_face(face_image):
    """
    对人脸图像进行增强处理，提升图像质量，帮助后续模型识别
    例如：亮度、对比度、去噪等
    """
    # 增强对比度（可选）
    face_image = cv2.convertScaleAbs(face_image, alpha=1.3, beta=30)

    # 去噪处理（可选）
    face_image = cv2.fastNlMeansDenoisingColored(face_image, None, 10, 10, 7, 21)

    return face_image


def get_img_embeddings(file_path, output_folder):
    saved_faces = detect_and_crop_faces(file_path, output_folder)
    if saved_faces is None:
        return None
    embeddings_list = []
    for face in saved_faces:
        img_path = os.path.join(output_folder, face)
        try:
            embeddings = DeepFace.represent(img_path=img_path, model_name="Facenet512")
            embeddings_list.append(embeddings)
        except Exception as e:
            print(f"提取人脸向量失败：{e}")
    return embeddings_list
