# -*- coding:utf-8 -*-
from fucor.single.single_base import *

from flask_bootstrap import Bootstrap

DEV_ORACLE = "oracle+cx_oracle://ktrdb:dev4kotric@210.97.19.50:1521/orcl"
DEV_OWNER = 'KTRDB'

ERP_ORACLE = "oracle+cx_oracle://KTR_DEV:KTR12#@192.168.1.13:1521/orcl"
ERP_OWNER = 'KTR_DEV'

DB_URL = ERP_ORACLE
DB_OWNER = ERP_OWNER

# SQLITE3 = "sqlite:///D:/fucor_db.db"
SQLITE3 = "sqlite:///D:/single_db.db"

app = Flask(__name__)
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE3
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN '] = True # 2017.01.04 추가
Bootstrap(app)

metadata = MetaData()
db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit': False })

'''
# ------------------------------------------------------------------------------
MODELS
# ------------------------------------------------------------------------------
'''

param_map = db.Table('CM_PARAM_MAP' \
    , db.Model.metadata
    , db.Column('param_id',db.Integer,db.ForeignKey('CM_PARAM.id'))  \
    , db.Column('params_name',db.String(100),db.ForeignKey('CM_PARAMS.name')) \
)  

class Base(db.Model):
    __abstract__  = True    
    @staticmethod
    def timestamp():
        return db.func.current_timestamp()
    
class CM_API(db.Model):
    __tablename__ = "CM_API"
    id          = db.Column(db.Integer, nullable=False, primary_key=True)
    api_descr   = db.Column(db.String(500),nullable=False)
    api_comment = db.Column(db.String(500),nullable=False)
    api_sample  = db.Column(db.Text)
    methods     = db.Column(db.String(500)) # GET/POST/PUT/DELETE
    req_uri     = db.Column(db.String(1000)) # Call
    req_headers = db.Column(db.String(1000))
    req_body    = db.Column(db.String(1000))
    res_headers = db.Column(db.String(1000))
    res_body    = db.Column(db.Text)
    create_dt   = db.Column(db.DateTime,  default=Base.timestamp())
    update_dt   = db.Column(db.DateTime,  default=Base.timestamp(), onupdate=Base.timestamp()) 
    params_name = db.Column(db.String(50), db.ForeignKey('CM_PARAMS.name'))

class CM_PARAMS(db.Model):
    __tablename__ = "CM_PARAMS"
    name        = db.Column(db.String(100),primary_key=True)
    descr       = db.Column(db.String(100), nullable=True) 
    create_dt   = db.Column(db.DateTime,  default=Base.timestamp())
    update_dt   = db.Column(db.DateTime,  default=Base.timestamp(), onupdate=Base.timestamp())                               
    cm_param    = db.relationship('CM_PARAM',secondary=param_map, backref="CM_PARAMS")
    cm_api      = db.relationship('CM_API', backref="CM_PARAMS")
    
    def __repr__(self):
        return '<CM_PARAM {} {} {} desc : {}>'.format(self.name, self.data_type,self.descr )


class CM_PARAM(db.Model):
    __tablename__ = "CM_PARAM"
    id          = db.Column(db.Integer, nullable=False, primary_key=True)
    param_name  = db.Column(db.String(100), nullable=False)
    param_value = db.Column(db.String(100), nullable=False)
    data_type   = db.Column(db.String(100), nullable=True)
    location    = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=False, default="NA") 
    create_dt   = db.Column(db.DateTime,  default=Base.timestamp())
    update_dt   = db.Column(db.DateTime,  default=Base.timestamp(), onupdate=Base.timestamp())    

    def __repr__(self):
        return '<CM_PARAM {} {} {} method_id : {}>'.format(self.name, self.data_type, self.descr )


class TODO(db.Model):
    __tablename__ = "TODO"
    id     = db.Column(db.Integer,nullable=False, primary_key=True)
    title  = db.Column(db.String(200),nullable=False)
#     items  = db.relationship('ITEMS', backref="TODO", lazy="dynamic")
    items  = db.relationship('ITEMS', backref="TODO")
    
    @staticmethod
    def to_dict(todo_id):
        d = {}
        todo = db.session.query(TODO).filter(TODO.id == todo_id).one()
        d['title'] = todo.title
        d['items'] = []
        for x in todo.items:
            item_title = x.title
            item_hidden = True if x.hidden == 1 else False
            item_done = True if x.done == 1 else False
            d['items'].append({ 'title':item_title, 'hidden':item_hidden, 'done':item_done })
        return d


class ITEMS(db.Model):
    __tablename__ = "ITEMS"
    id       = db.Column(db.Integer,nullable=False, primary_key=True)
    todo_id  = db.Column(db.Integer,db.ForeignKey('TODO.id'))
    title    = db.Column(db.String(200),nullable=False)
    hidden   = db.Column(db.Integer,nullable=True,default=0)
    done     = db.Column(db.Integer,nullable=True,default=0)


'''
# ------------------------------------------------------------------------------
ROUTES
# ------------------------------------------------------------------------------
'''
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api")
def show_api():
    return render_template("api_page.html")

@app.route("/example/<int:no>")
def example(no=0):
    if no == 1:
        return render_template("example_1.html")
    else:
        return render_template("index.html")

import json

@app.route("/todo",methods=['GET','POST'])
def todo():
    if request.method == 'POST':
        try:
            data = {}
            for x in request.form.keys():
                d = json.loads(x)
                data = d['data']
                break
            
            print(1)
            eprint("-----------")
            eprint(data)
            eprint(data.get('items'))
            eprint("-----------")
            title = data.get('title')
            todo = db.session.query(TODO).filter(TODO.title == title).one()
            db.session.query(ITEMS).filter(ITEMS.todo_id == todo.id).delete()
            print(2)
            for it in data.get('items'):
                print(2-1)
                item = ITEMS()
                item.todo_id = todo.id
                item.title = it['title']
                if 'hidden' in it:
                    item.hidden = 1 if it['hidden'] else 0
                if 'done' in it:
                    item.done = 1 if it['done'] else 0
                todo.items.append(item)
             
            print(3)
            db.session.add(todo)   
            db.session.commit()
            eprint("title",data.get('title'))
            return jsonify({'status' : 'success' })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status' : 'error', 'message' : str(e) })

    return jsonify(TODO.to_dict(1))

if __name__ == '__main__xxxxxx':
    todo = TODO()
    todo.title = "공통개발"
    todo_list = [
        '엑셀 다운로드'
        , '공통개발 준비하기'
        , '데이터베이스 이관 준비'
    ]
    for x in todo_list:
        items = ITEMS()
        items.title = x
        todo.items.append(items)
     
    db.session.add(todo)
    try:
        db.session.commit()
    except Exception as e:
        eprint(e)
        db.session.rollback()



if __name__ == '__main__111':
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    db.metadata.drop_all(db.engine,tables=[
        CM_PARAMS.__table__
        , CM_PARAM.__table__
        , CM_API.__table__
    ])    
    db.create_all()

if __name__ == '__main__44':
    app.run(debug=True)

   
    
    
    
    
    
    
    
    
    
