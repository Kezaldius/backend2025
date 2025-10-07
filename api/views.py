from api import app

@app.route("/healthcheck")
def healthcheck():
    return {"status": "OK", "message": "Application is healthy"}
