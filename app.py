import hmac
import os, boto3
from flask import Flask, request, jsonify
from flask_cors import CORS

s3_client = boto3.client("s3")
bucket_name = "upload-demo-nick"
#  boto3自動讀export 的環境變數、 只有一個client 不須寫os.environ
#  export AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY、AWS_DEFAULT_REGION

app = Flask(__name__)
CORS(app,
     resources={r"/get_URL": {"origins": [
         "http://localhost:5173",
         "https://cloud-upload-frontend.vercel.app"
     ]}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["POST", "OPTIONS"])

@app.route("/get_URL", methods=["POST"])
def get_URL():
    data = request.get_json(silent=True)
    # 讀headers:    request.headers.get()
    # 讀body (Json) request.get_json()  (formdata)requst.files["file"]
    # 遇無效JSON不丟錯，回傳None   data==送過來的整個body(JSON)格式
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    filename = data.get("filename")
    content_type = data.get("contentType", "application/octet-stream")

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": filename, "ContentType": content_type},
        ExpiresIn=120  # 有效時間 (秒)
    )

    return jsonify({"presigned_url": presigned_url, "key": filename}), 200
@app.route("/direct_uploadS3", methods=["POST"])
def direct_uploadS3():
    if "file" not in request.files:
        return jsonify({"error": "missing file"}), 400

    file = request.files["file"]
    key = request.form["filename"] or file.filename
    s3_client.upload_fileobj(
    	Fileobj = file, Bucket = bucket_name, Key = key
    )
    return jsonify({
	"message":"upload to s3 success",
	"key":key
    })
@app.route("/upload_success",method=["POST"])
def upload_success():
    data = request.get_json()
    filename = data["filename"]
    bucket = data["bucket"]

    print("got upload success noitce")
    return {"status":"recieved"}

if __name__ == "__main__":
    app.run(port = 5000, host = "0.0.0.0")
