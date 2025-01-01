from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your secret key from reCAPTCHA Admin Console
SECRET_KEY = "6Ld2SqsqAAAAAMNee-R5-bwW_mQBPzSz7kbLPcVz"

@app.route("/submit/", methods=["POST"])
def verify_captcha():
    # Get the CAPTCHA response from the client
    recaptcha_response = request.form.get("g-recaptcha-response")
    if not recaptcha_response:
        return jsonify({"status": "fail", "message": "CAPTCHA token missing"}), 400

    # Verify CAPTCHA response with Google
    payload = {"secret": SECRET_KEY, "response": recaptcha_response}
    verification = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    result = verification.json()

    if result.get("success"):
        return jsonify({"status": "success", "message": "CAPTCHA verified successfully!"})
    else:
        return jsonify({"status": "fail", "message": "CAPTCHA verification failed"}), 400

if __name__ == "__main__":
    app.run(debug=True)
