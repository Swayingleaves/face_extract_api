# 使用Deepface抽取人脸、抽取特征向量

## http api

### 抽取人脸
请求
```http
curl -XPOST 'http://127.0.01:5006/detect_faces' --form 'file=@"/Users/edy/Downloads/duorenlian.jpeg"'
```

返回
```json
{
    "msg": [
        "duorenlian_20250108_123459_0.jpg",
        "duorenlian_20250108_123459_1.jpg",
        "duorenlian_20250108_123459_2.jpg",
        "duorenlian_20250108_123459_3.jpg",
        "duorenlian_20250108_123459_4.jpg",
        "duorenlian_20250108_123459_5.jpg",
        "duorenlian_20250108_123459_6.jpg"
    ],
    "size": 7
}
```
抽取出的人脸保存在项目目录下的/deepface-output下以上传的文件名加上传时间+抽取的人脸序号命令保存

### 获取抽取出的人脸图片
请求
```http
curl -XGET 'http://127.0.0.1:5006/get_face_image/duorenlian_20250108_123459_0.jpg'
```

返回图片

### 获取人脸特征向量
请求
```http
curl -XPOST 'http://127.0.0.1:5000/embeddings' --form 'file=@"/Users/edy/Downloads/10.jpg"'
```

返回
```json
{
    "embeddings": [
        [
            {
                "embedding": [
                    0.20108041167259216,
                    -0.17052577435970306,
                    -1.4283512830734253,
                    -0.0520436055958271,
                    -0.146202951669693,
                    0.6637242436408997,
                    -0.2972835302352905,
                    1.1632393598556519
                ],
                "face_confidence": 0.96,
                "facial_area": {
                    "h": 636,
                    "left_eye": [
                        404,
                        236
                    ],
                    "right_eye": [
                        328,
                        379
                    ],
                    "w": 524,
                    "x": 0,
                    "y": 0
                }
            }
        ]
    ],
    "msg": "success"
}
```