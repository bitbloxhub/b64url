from sanic import Sanic, response, exceptions
from aredis import StrictRedis
from jinja2 import Environment, PackageLoader, select_autoescape
import base64

__version__ = '0.1.0'

app = Sanic("b64url")

app.config["REDIS_HOST"] = "127.0.0.1"
app.config["REDIS_PORT"] = 6379

env = Environment(
    loader=PackageLoader("b64url"),
    autoescape=False
)


@app.get("/")
async def index(request):
    return response.html(env.get_template("index.html").render())

@app.get("/upload")
async def uploadurl(request):
    return response.html(env.get_template("upload.html").render())

@app.post("/pupload")
async def pupload(request):
    redis = StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"])
    if not await redis.exists(request.form.get("filename")):
        await redis.set(request.form.get("filename"), base64.b64encode(request.files.get("file").body))
    return response.redirect("/")

@app.get("/file/<filename:str>")
async def fileget(request, filename):
    redis = StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"])
    if await redis.exists(filename):
        content = base64.b64decode(await redis.get(filename))
        return response.raw(content)
    else:
        raise exceptions.FileNotFound("Cannot find the file you were looking for, sorry!", request.url, request.path)
    

@app.get("/de64/<b64:str>")
async def de64(request, b64):
    return response.raw(base64.b64decode(b64))