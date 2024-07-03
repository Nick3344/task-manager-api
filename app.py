from app import create_app, db    
from app.resources import TaskResource, TaskListResource, UserRegister, UserLogin
from app import api
from app.swagger import swaggerui_blueprint

app = create_app()

# Create the database and tables
with app.app_context():
    db.create_all()

# Add resource endpoints
api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

# Register Swagger UI blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=swaggerui_blueprint.url_prefix)

if __name__ == '__main__':
    app.run(debug=True)
