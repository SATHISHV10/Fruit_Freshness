from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Dataset folders
FRESH_FOLDER = "dataset/fresh"
ROTTEN_FOLDER = "dataset/rotten"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    filename = ""

    if request.method == "POST":

        if "image" not in request.files:
            return render_template(
                "index.html",
                result="No image selected.",
                image=""
            )

        file = request.files["image"]

        if file.filename == "":
            return render_template(
                "index.html",
                result="No image selected.",
                image=""
            )

        filename = file.filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        # Check whether the uploaded filename exists
        if os.path.isfile(os.path.join(FRESH_FOLDER, filename)):
            result = "🍏 FRUIT IS FRESH"

        elif os.path.isfile(os.path.join(ROTTEN_FOLDER, filename)):
            result = "🍎 FRUIT IS ROTTEN"

        else:
            result = "❓ IMAGE NOT FOUND IN DATASET"

    return render_template(
        "index.html",
        result=result,
        image=filename
    )


if __name__ == "__main__":
    app.run(debug=True)