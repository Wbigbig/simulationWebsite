from flask import Flask


app = Flask(__name__)

app.config.from_pyfile("./config/simulationWeb_config.py")
app.jinja_env.auto_reload = True    # 模板热更新

