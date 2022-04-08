from flask import Flask, jsonify, render_template, send_from_directory
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields



app = Flask(__name__, template_folder='swagger/templates')


@app.route('/')
def hello_world():
    return 'Hellow World!'

# configure APIspecification 
# with open api, to get api response
spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin()]
) 

# when we call this url
# the open api response will be returned

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict()) 

# in the open api response the "paths"
# contain the apis that will be configured through Marshmallow Schema

# Here we will define an api which will respond list of Todo Items
class TodoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()

# Here another api that will respond an array of Todos
class TodoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(TodoResponseSchema))   

# define the actual api response
@app.route('/todo')     
def todo():
    """Get List of Todo
       ---
       get:
           description: Get List of Todos
           responses:
                 200:
                    description: Return a todo list
                    content:
                        application/json:
                            schema: TodoListResponseSchema
    
    """


    dummy_data = [{
        'id': 1,
        'title': 'Finish this task',
        'status': False

    },{
        'id': 2,
        'title': 'Finish that task',
        'status': True
    }]
    return TodoListResponseSchema().dump({'todo_list': dummy_data})

with app.test_request_context():
    spec.path(view=todo)    



@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')

    else:
        return send_from_directory('./swagger/static', path)    
        

if __name__ == '__main__':
    app.run(debug=True)