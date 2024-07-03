from flask_restful import Resource, reqparse
from app.models import Task, User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Task parser
parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help="Title cannot be blank!")
parser.add_argument('description', type=str)
parser.add_argument('completed', type=bool)

# User parser
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help="Username cannot be blank!")
user_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")

class UserRegister(Resource):
    def post(self):
        args = user_parser.parse_args()
        if User.query.filter_by(username=args['username']).first():
            return {'message': 'User already exists'}, 400
        user = User(username=args['username'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        args = user_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        tasks = Task.query.all()
        return [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]

    @jwt_required()
    def post(self):
        args = parser.parse_args()
        task = Task(title=args['title'], description=args.get('description'), completed=args.get('completed', False))
        db.session.add(task)
        db.session.commit()
        return {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}, 201

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}

    @jwt_required()
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        args = parser.parse_args()
        task.title = args['title']
        task.description = args.get('description')
        task.completed = args.get('completed', task.completed)
        db.session.commit()
        return {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}

    @jwt_required()
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204
