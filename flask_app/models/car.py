from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
pattern = r"^(?=.*\d.*\d.*\d)[A-Za-z\d]{5,7}$"

class Car:
    db_name = 'blocked_cars'
    def __init__( self , data ):
        self.id = data['id']
        self.plates = data['plates']
        self.distance = data['distance']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_car_by_id(cls, data):
        query = "SELECT * FROM cars WHERE cars.id = %(car_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    #READ
    @classmethod
    def get_all(cls):
        query = "SELECT cars.*, users.first_name, users.last_name FROM cars LEFT JOIN users ON cars.user_id = users.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        cars = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for car in results:
                cars.append(car)
            return cars
        return cars
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (plates, distance, user_id) VALUES ( %(plates)s, %(distance)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET plates = %(plates)s, distance = %(distance)s WHERE cars.id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE cars.id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
        #DELETE
    @classmethod
    def deleteAllJoins(cls, data):
        query = "DELETE FROM joins WHERE car_id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def join(cls, data):
        query = "INSERT INTO joins (car_id, car_id2, user_id) VALUES ( %(car_id)s, %(car_id2)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    @classmethod
    def unjoin(cls, data):
        query = "DELETE FROM joins WHERE car_id = %(car_id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_cars_joined(cls, data):
        query = "SELECT car_id FROM joins WHERE joins.car_id2 = %(car_id2)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        joinedCars = []
        if results:
            for row in results:
                joinedCars.append(row)
            return joinedCars
        return joinedCars
    
    @classmethod
    def get_cars_blocked(cls, data):
        query = "SELECT * FROM joins LEFT JOIN cars on joins.car_id2 = cars.id LEFT JOIN users on joins.user_id = users.id WHERE joins.car_id = %(car_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        joinedCars = []
        if results:
            for row in results:
                joinedCars.append(row)
            return joinedCars
        return joinedCars

    
    @classmethod
    def get_logged_user_car(cls, data):
        query = "SELECT * FROM cars WHERE cars.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        joinedCars = []
        if results:
            for row in results:
                joinedCars.append(row)
            return joinedCars
        return joinedCars

    @staticmethod
    def validate_car(car):
        is_valid = True
        if not re.match(pattern, car['plates']):
            flash('Targa nuk është e saktë!', 'platesCar')
            is_valid= False
        if not car.get('distance'):
            flash('Distanca e përafërt duhet të përcaktohet!', 'distanceCar')
            is_valid= False
        return is_valid
