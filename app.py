from flask import Flask, request
import boto3

app = Flask(__name__)

# Replace with your S3 bucket name and access credentials
S3_BUCKET_NAME = "your_bucket_name"
AWS_ACCESS_KEY_ID = "your_access_id"
AWS_SECRET_ACCESS_KEY = "your_acess_key"

@app.route("/")
def index():
    return open("index.html").read()

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("files[]")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        for file in files:
            s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)

        return open("success.html").read()
    else:
        return open("index.html").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
