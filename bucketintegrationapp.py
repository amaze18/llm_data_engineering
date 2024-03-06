from flask import Flask, request, redirect
import boto3
app = Flask(__name__)

# Replace with your S3 bucket name and access credentials
S3_BUCKET_NAME = "testbucket-375"
AWS_ACCESS_KEY_ID = "AKIA3WKM46OFHLP6P7HD"
AWS_SECRET_ACCESS_KEY = "rRiHgHYrMfaN8gRr64YBt/QHLoCycdsQmx6oQK0S"

@app.route("/")
def index():
    return open("index.html").read()

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        return "File uploaded successfully!<button onclick='location.href=\"/\";'>Go Back</button>"
    else:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload File</title>
        </head>
        <body>
            <h1>Upload File</h1>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <button type="submit">Upload</button>
            </form>
            <br>
            <button onclick='location.href=\"/\";'>Go Back</button>
        </body>
        </html>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
