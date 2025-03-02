from flask import *
from public import *
from admin import *
from user import *


app = Flask(__name__)
app.secret_key="secret_key"
app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(user)



app.run(debug=True, port=5555)