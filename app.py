import hmac
import os, boto3
from flask import Flask, request, jsonify
from flask_cors import CORS

s3_client = boto3.client("s3")
#  boto3自動讀export 的環境變數、 只有一個client 不須寫os.environ
#  export AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY、AWS_DEFAULT_REGION

app = Flask(__name__)
CORS(app,
     resources={r"/get_URL": {"origins": [
         "http://localhost:5173", "https://cloud-upload-frontend-p7oj8bgxb-tenghuangs-projects.vercel.app/"
     ]}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["POST", "OPTIONS"])

@app.route("/get_URL", methods=["POST"])
def get_URL():
    data = request.get_json(silent=True)
    # 讀headers:  request.headers.get()
    # 遇無效JSON不丟錯，回傳 None   data==送過來的整個body
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    filename = data.get("filename")
    content_type = data.get("contentType", "application/octet-stream")

    bucket_name = "upload-demo-nick"

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": filename, "ContentType": content_type},
        ExpiresIn=1000  # 有效時間 (秒)
    )

    return jsonify({"presigned_url": presigned_url, "key": filename}), 200

if __name__ == "__main__":
    app.run(port = 5000, host = "0.0.0.0")
