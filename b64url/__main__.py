from b64url import app
app.run(host='127.0.0.1', port=8080, workers=8, access_log=False)