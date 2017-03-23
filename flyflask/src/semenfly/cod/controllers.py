from fucor.application import *
from fucor.cod.models import *
from fucor.cod.services import *

mod_cod = Blueprint('coder', __name__, url_prefix='/coder', template_folder='templates')

@mod_cod.route('/', methods=['GET', 'POST'])
def cod_index():
    return render_template("cod/index.html")

@mod_cod.route("/page/<path>", methods=['GET'])
def cod_page(path):
    try:
        return render_template("cod/{path}.html".format(path=path))
    except Exception as e:
        return render_template("cod/index.html".format(path=path))
        

@mod_cod.route("/add", methods=['GET','POST'])
def cod_coder_add():
    if request.method == 'POST':
        pass
    return render_template("cod/index.html")
