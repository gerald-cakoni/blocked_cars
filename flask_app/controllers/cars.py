from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car
import datetime
import math
import random
import smtplib
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, session, request, flash

from .env import ADMINEMAIL
from .env import PASSWORD

from datetime import datetime
import os


@app.route('/add/car')
def addCar():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        return render_template('addCar.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/car', methods = ['POST'])
def createCar():
    if 'user_id' in session:
        if not Car.validate_car(request.form):
            return redirect(request.referrer)

        data = {
            'plates': request.form['plates'],
            'distance': request.form['distance'],
            'user_id': session['user_id'],
        }
        Car.save(data)
        return redirect('/mycars')
    return redirect('/')

@app.route('/edit/car/<int:id>')
def editCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
        print(loggedUser['id'])
        print(car['user_id'])
        if loggedUser['id'] == car['user_id']:
            return render_template('editCar.html', loggedUser = loggedUser, car= car)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/car/<int:id>')
def viewCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
        savedCars = []
        carsJoinedSpecific = Car.get_cars_blocked(data)
        for car2 in carsJoinedSpecific:
            savedCars.append(car2)

        print(savedCars)
        return render_template('showOne.html', loggedUser = loggedUser, car= car, savedcars=savedCars)
    return redirect('/')

@app.route('/edit/car/<int:id>', methods = ['POST'])
def updateCar(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        car = Car.get_car_by_id(data1)
        if loggedUser['id'] == car['user_id']:

            data = {
                'plates': request.form['plates'],
                'distance': request.form['distance'],
                'car_id': car['id'],
                'user_id': session['user_id'],
            }
            Car.update(data)
            return redirect('/mycars')
        return redirect('/mycars')
    return redirect('/')

@app.route('/delete/car/<int:id>')
def deleteCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
                # Check that loggedUser and car are not boolean values
        if isinstance(car, bool):
            return "Error: Could not retrieve user or car data"
        Car.deleteAllJoins(data)
        Car.delete(data)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/mycars')
def mycars():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }

    loggedUser = User.get_user_by_id(data)
    cars = Car.get_all()

    return render_template('myCars.html', cars = cars, loggedUser=loggedUser)

@app.route('/allcars')
def allcars():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    cars = Car.get_all()
    loggedUserCars = Car.get_logged_user_car(data)
    savedCars = []
    for car in loggedUserCars:
        dataC = {
            "car_id2": car["id"]
        }
        carsJoinedSpecific = Car.get_cars_joined(dataC)
        for car2 in carsJoinedSpecific:
            savedCars.append(car2["car_id"])

    return render_template('allCars.html', cars = cars, loggedUser=loggedUser, savedcars=savedCars)


@app.route('/join/<int:id>')
def joinCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }        
        joinedCar = Car.get_cars_joined(data)
        if id not in joinedCar:
            return redirect("/select/your/car/"+ str(id))

        return redirect(request.referrer)
    return redirect('/')
@app.route('/select/your/car/<int:id>')
def selectCarFinal(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data)
        carLogged = Car.get_logged_user_car(data)
        joinedCar = Car.get_cars_joined(data)

        if id not in joinedCar:
            return render_template("selectCar.html", carLogged = carLogged, car_id = id, loggedUser = loggedUser)

        return redirect(request.referrer)
    return redirect('/')

@app.route('/join/car/<int:car_id>', methods = ["POST"])
def selectCar(car_id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': car_id,
            'car_id2': request.form['car_id2']
        }
        
        joinedCar = Car.get_cars_joined(data)
        if id not in joinedCar:
            Car.join(data)
            return redirect("/")
        return redirect(request.referrer)
    return redirect('/')

@app.route('/unjoin/<int:id>')
def unsaveCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        print("/------------------------------------")
        Car.unjoin(data)
        return redirect(request.referrer)
    return redirect('/')


@app.route('/send/email/<email>/<targa>/<emri>')
def sendEmailReminder(email, targa, emri):
    if 'user_id' in session:
        receiver = email
        LOGIN = ADMINEMAIL
        TOADDRS  = receiver
        SENDER = ADMINEMAIL
        SUBJECT = 'Leviz makinen'
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
            % ((SENDER), "".join(TOADDRS), SUBJECT) )
        msg += f'{emri}!\nDuhet te shkosh te levizesh makinen pasi ke bllokuar rrugen. \nPersonat jane duke te pritur! Mos harro te zhbllokosh makinen ne sistem pasi ta kesh hapur rrugen'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()
        
        flash("Njoftimi u dërgua me sukses!", "emailSent")
        return redirect(request.referrer)