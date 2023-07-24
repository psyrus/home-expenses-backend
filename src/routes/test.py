from ..app import app

# Test

@app.route("/test", methods=["GET"])
def get_test():
    return "test"
