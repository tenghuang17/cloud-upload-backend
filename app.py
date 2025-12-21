import hmac
import uuid
import json
import os, boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

s3_client = boto3.client("s3")
sqs_client = boto3.client("sqs")
bucket_name = "upload-demo-nick"
QUEUE_URL = "https://sqs.ap-northeast-1.amazonaws.com/858949074941/Request_Queue"
#  boto3自動讀export 的環境變數、 只有一個client 不須寫os.environ
#  export AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY、AWS_DEFAULT_REGION

app = Flask(__name__)
CORS(
    app,
    origins=[
        "http://localhost:5173",
        "https://cloud-upload-frontend.vercel.app"
    ],
    supports_credentials=True
)

def unified_filename_to_s3key(filename):
    #  日期資料夾，例如：20250120
    date_prefix = datetime.utcnow().strftime("%Y%m%d")
    # UUID  (32 字  hex，不含 dash)
    unique_id = uuid.uuid4().hex  # "85df1c8e91bd4dd0ab57921c"
    #  組出 key
    s3_key = f"encrypted/{date_prefix}/{unique_id}_{filename}"
    return s3_key

@app.route("/get_URL", methods=["POST"])
def get_URL():
    data = request.get_json(silent=True)
    # 讀headers:    request.headers.get()
    # 讀body (Json) request.get_json() // (formdata)requst.files["file"]
    # 遇無效JSON不丟錯，回傳None   data==送過來的整個body(JSON)格式
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    filename = data.get("filename") 
    s3_key = unified_filename_to_s3key(filename)
    content_type = data.get("contentType", "application/octet-stream")

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": s3_key, "ContentType": content_type},
        ExpiresIn=120  # 有效時間 (秒)
    )
    return jsonify({"presigned_url": presigned_url, "key": s3_key}), 200

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

@app.route("/upload_success",methods=["POST"])
def upload_success():   # 收前端通知 : 上傳s3成功
    data = request.get_json()
    s3_key = data["key"]      # 前端最後回傳的資訊 s3 key等 看需要哪些組成message後   
    bucket = data["bucket"]                     #    SQS(message)-->  worker 下載後 解密  寫回 s3
    print("got upload success noitce")

    message = {
        "bucket": bucket,
        "key": s3_key,
        "action": "decrypt"
    }
    sqs_client.send_message(         # message immutable  <= 256 KB
        QueueUrl=QUEUE_URL,          # MessageBody has to be string     can't be python dict
        MessageBody=json.dumps(message)    # json.dumps    Python objext ->  string
    )                                      # json.loads    string  -> python object

    return {"status":"message_sent_to_worker"}

if __name__ == "__main__":
    app.run(port = 5000, host = "0.0.0.0")
