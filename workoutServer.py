import os
import sqlalchemy
import random
import string
import oauth2client
import httplib2
import json
import requests
import codecs
from flask
import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, make_response
from datetime
import datetime
from sqlalchemy.orm
import scoped_session, sessionmaker
from sqlalchemy
import create_engine, asc, desc
from flask
import session as sessionmaker
from oauth2client.client
import flow_from_clientsecrets
from oauth2client.client
import FlowExchangeError
from werkzeug.utils
import secure_filename
from flask_sqlalchemy
import SQLAlchemy
from flask_mail
import Mail, Message
from flask_login
import LoginManager, current_user, login_user, logout_user, login_required
from random
import randint

reader = codecs.getreader("utf-8")

UPLOAD_FOLDER = os.path.dirname('static/im/usrs')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
ALLOWED_EXTENSIONS_VIDEOS = set(['mpg', 'mpeg', 'mp4', 'mov'])

app = Flask(__name__)

from sqlalchemy
import create_engine
from sqlalchemy.orm
import sessionmaker
from create_db_wo
import Base, User, W, E, UserMixin, Stats, Common_E

engine = create_engine('sqlite:///wo_db_engine.db')
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind = engine))

app.config.update(
  DEBUG = True,

  MAIL_SERVER = 'smtp.gmail.com',
  MAIL_PORT = 465,
  MAIL_USE_SSL = True,

)

mail = Mail(app)

login = LoginManager(app)
login.login_view = 'showLogin'
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "showLogin"

skipped = True

@login_manager.user_loader
def load_user(id):
  user = session.query(User).filter_by(id = id).one()
return user

@app.teardown_request
def remove_session(ex = None):
  session.remove()

@app.route('/logout')
def logout():
  print("logged out")
logout_user()

return redirect(url_for('showLogin'))

@app.route('/home')
@app.route('/', methods = ['POST', 'GET'])
def showLogin():

  all_users = session.query(User).all()

if current_user.is_authenticated:
  return redirect(url_for('main'))
if request.method == "POST":

  for a in all_users:

  if request.form["email"].lower() == a.email.lower():
  if request.form['p'] == a.p:
  login_user(a, remember = True)
return redirect(url_for('main'))
return render_template('index.html')

@app.route('/exercise/add/desc/', methods = ['POST', 'GET'])
@login_required
def desc_e():
  if request.method == 'POST':
  www = Common_E(name = request.form['name'], description = request.form['description'])
session.add(www)
session.commit()
return render_template('desc_e.html')
return render_template('desc_e.html')

@app.route('/forgot/pw/recover/', methods = ['POST', 'GET'])
def forgotPW():
  msg = Message()
all_users = session.query(User).all()
if request.method == 'POST':
  for a in all_users:
  if a.email == request.form['email'].lower():
  print(a.email + ' is email ' + request.form['email'] + ' is request email')
msg = Message('Password Recovery from RSG', sender = 'paynedanielfranklin@gmail.com', recipients = [request.form['email']])
msg.html = " <p> <br>Your Recovered Password is: <strong>" + a.p
mail.send(msg)
return redirect(url_for('showLogin'))
return redirect(url_for('showLogin'))
return redirect(url_for('showLogin'))

@app.route('/signup/', methods = ['POST', 'GET'])
def createAccount():
  all_users = session.query(User).all()
if request.method == 'POST':
  for a in all_users:
  if a.email.lower() == request.form['email'].lower():
  return redirect(url_for('showLogin'))
if request.form['p2'] == request.form['p']:
  newUser = User(name_first = request.form['name_first'].capitalize(), name_last = request.form['name_last'].capitalize(), email = request.form['email'].lower(),
    p = request.form['p'])
session.add(newUser)
session.commit()
login_user(newUser, remember = True)
return redirect(url_for('main'))
return redirect(url_for('showLogin'))

@app.route('/main')
@login_required
def main():
  print('inside main')
user_default = session.query(User).filter_by(id = current_user.id).one()
print(str(user_default.name_first))
all_w = get_usr_workouts()
all_e = session.query(E).all()
imageTester = ['za1.jpg', 'za2.jpg', 'za3.jpg', 'za4.jpg', 'za5.jpg', 'za6.jpg', 'za7.jpg']

return render_template('main.html', users_workouts = all_w, all_e = all_e, user = user_default, images = imageTester, all_exercises = all_e)

@app.route('/upload/workout/<int:workout_id>/', methods = ['GET', 'POST'])
@login_required
def upload_workout(workout_id):
  print('inside main')
user_default = session.query(User).filter_by(id = current_user.id).one()
print(str(user_default.name_first))
all_w = get_usr_workouts()
all_e = session.query(E).filter_by(w_id = workout_id, user_id = user_default.id).all()
this_workout = session.query(W).filter_by(id = workout_id).one()
imageTester = ['za1.jpg', 'za2.jpg', 'za3.jpg', 'za4.jpg', 'za5.jpg', 'za6.jpg', 'za7.jpg']
if request.method == 'POST':
  if request.form.get('full_body') == 'yes':
  this_workout.full_body = True
if request.form.get('upper_body') == 'yes':
  this_workout.upper_body = True
if request.form.get('lower_body') == 'yes':
  this_workout.lower_body = True
this_workout.uploaded = True
this_workout.description = request.form['description']
session.add(this_workout)
session.commit()
return redirect(url_for('main'))

return render_template('upload_workout.html', all_e = all_e, user = user_default, images = imageTester, this_workout = this_workout)

@app.route('/download/<int:workout_id>/', methods = ['GET', 'POST'])
@login_required
def download_workout(workout_id):
  this_user = get_cur_user()
dw = session.query(W).filter_by(id = workout_id).one()
dw.download_count = dw.download_count + 1
session.add(dw)
session.commit()
print('download count for workout ' + dw.name + ' is ' + str(dw.download_count))
dw_e = session.query(E).filter_by(w_id = dw.id).all()

new_workout = W(name = dw.name, owner_id = this_user.id, has_weeks = True, uploaded = False, original_owner = dw.original_owner, description = dw.description)
session.add(new_workout)
session.commit()
for d in dw_e:
  newExercise = E(name = d.name, sets = d.sets, day = d.day, reps = d.reps, rest_between_minutes = d.rest_between_minutes, rest_between_seconds = d.rest_between_seconds, time_for_set = d.time_for_set, w_id = new_workout.id, user_id = this_user.id)
session.add(newExercise)
session.commit()
return redirect(url_for('main'))

@app.route('/community/')
@login_required
def community():
  this_user = get_cur_user()
uploaded_workouts = session.query(W).filter_by(uploaded = True).all()
all_user_workouts = session.query(W).filter_by(owner_id = this_user.id).all()
for u in uploaded_workouts:
  print('workout name is ' + u.name + ' download amount is ' + str(u.download_count))

imageTester = ['za1.jpg', 'za2.jpg', 'za3.jpg', 'za4.jpg', 'za5.jpg', 'za6.jpg', 'za7.jpg', 'za8.jpg', 'za9.jpg', 'za10.jpg', 'za11.jpg', 'za12.jpg', 'za13.jpg', 'za14.jpg', 'za15.jpg', 'za16.jpg', 'za17.jpg', 'za18.jpg', 'za19.jpg']

return render_template('community.html', this_user = this_user, uploaded_workouts = uploaded_workouts, images = imageTester, all_user_workouts = all_user_workouts)

@app.route('/community/info/<int:workout_id>/')
@login_required
def workoutInfo(workout_id):
  print('inside main')
this_user = get_cur_user()
workout = session.query(W).filter_by(id = workout_id).one()
imageTester = ['za1.jpg', 'za2.jpg', 'za3.jpg', 'za4.jpg', 'za5.jpg', 'za6.jpg', 'za7.jpg']
randomizer = randint(0, len(imageTester) - 1)
all_users = session.query(User).all()
all_e = session.query(E).filter_by(w_id = workout_id).all()
days_rest = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
has_day = False
rest_days = 0
for i in range(0, len(days_rest)):
  for a in all_e:
  if a.day == days_rest[i]:
  has_day = True
print(a.day + ' is equal to ' + days_rest[i])
if has_day == False:
  rest_days = rest_days + 1
print(rest_days)
has_day = False

for a in all_users:
  if a.id == workout.original_owner:
  original_owner = a

return render_template('workoutInfo.html', rest_days = rest_days, this_user = this_user, all_e = all_e, workout = workout, image = imageTester[randomizer], original_owner = original_owner)

@app.route('/createWorkout', methods = ['POST', 'GET'])
@login_required
def createWorkout():
  this_user = get_cur_user()
default_user = session.query(User).filter_by(id = current_user.id).one()
print(str(default_user.name_first))
if request.method == 'POST':
  new_workout = W(name = request.form['name'], owner_id = default_user.id, has_weeks = True, uploaded = False, original_owner = this_user.id, description = "")
print('does not have weeks')
session.add(new_workout)
session.commit()
return redirect(url_for('main'))
return render_template('createWorkout.html')

@app.route('/workout/<int:id>/')
@login_required
def workout(id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = id).one()
thisE = get_exercises(id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
all_exercises = session.query(E).filter_by(user_id = this_user.id, w_id = id).all()

names = []
unique_names = []
name_id = []

tester = []

for i in all_user_e:
  names.append(i.name)

for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)

for n in name_id:
  print(n)

for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))

if thisWorkout.owner_id == this_user.id:
  return render_template('workout.html', all_exercises = all_exercises, thisWorkout = thisWorkout, all_e = thisE, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

@app.route('/workout/add/<int:thisWorkout_id>/<int:e_id>/<string:day>/', methods = ['POST', 'GET'])
@login_required
def addExerciseFromTemplate(thisWorkout_id, e_id, day):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = thisWorkout_id, owner_id = this_user.id).one()
this_e_template = session.query(E).filter_by(user_id = this_user.id, id = e_id).one()
return render_template('addFromTemplate.html', this_user = this_user, this_e_template = this_e_template, thisWorkout = thisWorkout, day = day)

@app.route('/workout/<int:thisWorkout_id>/', methods = ['POST', 'GET'])
@login_required
def addExercise(thisWorkout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = thisWorkout_id).one()
all_e = get_exercises(thisWorkout_id)
if request.method == "POST":

  newExercise = E(name = request.form['exerciseName'].lower(), sets = request.form['sets'], day = request.form['day'].lower(), reps = request.form['reps'], rest_between_minutes = request.form['restBetweenMinutes'], rest_between_seconds = request.form['restBetweenSeconds'], time_for_set = request.form['timeForSet'], w_id = thisWorkout.id, user_id = this_user.id)
session.add(newExercise)
session.commit()
return redirect(url_for(newExercise.day, workout_id = thisWorkout.id))
return redirect(url_for('workout', id = thisWorkout.id))

@app.route('/workout/exercise/edit/<int:thisWorkout_id>/<int:thisExercise_id>/<string:day>/', methods = ['POST', 'GET'])
@login_required
def editExercise(thisWorkout_id, thisExercise_id, day):
  this_user = get_cur_user()
this_users_workouts = get_usr_workouts()
if request.method == 'POST':
  print('inside edit exercise post')
for t in this_users_workouts:
  if t.id == thisWorkout_id:
  this_exercise = session.query(E).filter_by(id = thisExercise_id, w_id = t.id).one()
this_exercise.name = request.form['name'].lower()
this_exercise.sets = request.form['sets']
this_exercise.reps = request.form['reps']
this_exercise.rest_between_minutes = request.form['restBetweenMinutes']
this_exercise.rest_between_seconds = request.form['restBetweenSeconds']
this_exercise.time_for_set = request.form['timeForSet']
session.add(this_exercise)
session.commit()
return redirect(url_for(day, workout_id = t.id))

for t in this_users_workouts:
  if t.id == thisWorkout_id:
  this_exercise = session.query(E).filter_by(id = thisExercise_id, w_id = t.id).one()
return render_template('editExercise.html', thisWorkout = t, thisExercise = this_exercise, user = this_user, day = day)
return redirect(url_for('workout', id = thisWorkout_id))

@app.route('/workout/weight/<int:workout_id>/<int:exercise_id>/', methods = ['POST', 'GET'])
@login_required
def beginWorkout_weight(workout_id, exercise_id):
  global skipped
skipped = True
this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisExercise = session.query(E).filter_by(id = exercise_id).one()
thisExercise.weight = 0
session.add(thisExercise)
session.commit()
if request.method == 'POST':
  thisExercise.weight = request.form['weight']

session.add(thisExercise)
session.commit()

skipped = False;

print('inside beginWorkout_weight weight is ' + str(thisExercise.weight) + ' skipped is equal to ' + str(skipped))
return redirect(url_for('beginWorkout', workout_id = thisWorkout.id, exercise_id = thisExercise.id))
return render_template('exerciseWeight.html', thisWorkout = thisWorkout, thisExercise = thisExercise)

@app.route('/workout/beginWorkout/<int:workout_id>/<int:exercise_id>/')
@login_required
def beginWorkout(workout_id, exercise_id):
  global skipped
this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisExercise = session.query(E).filter_by(id = exercise_id).one()
images = ['2.jpg', '1.jpg', '14.jpg', '9.jpg', '12.jpg', '13.jpg', '16.jpg', '17.jpg', '18.jpg']
randomizer = randint(0, len(images) - 1)
imageRandomizer = images[randomizer]

print('inside beginWorkout weight is ' + str(thisExercise.weight) + ' skipped is equal to ' + str(skipped))

if thisExercise.weight == '':
  thisExercise.weight = 0
session.add(thisExercise)
session.commit()
print('this exercise has no weight')
print('this weight is ' + str(thisExercise.weight))
return render_template('exercise.html', thisWorkout = thisWorkout, thisExercise = thisExercise, imageRandomizer = imageRandomizer, day = thisExercise.day)

def get_cur_user():
  this_user = session.query(User).filter_by(id = current_user.id).one()
return this_user

def get_usr_workouts():
  this_user = get_cur_user()
usr_workouts = session.query(W).filter_by(owner_id = this_user.id).all()
return usr_workouts

def get_exercises(w_id):
  this_user = get_cur_user()
if session.query(W).filter_by(owner_id = this_user.id, id = w_id).one().id == w_id:
  thisE = session.query(E).filter_by(w_id = w_id).all()
return thisE

@app.route('/workout/del/query/<int:workout_id>')
@login_required
def del_Workout_Confirm(workout_id):
  this_user = get_cur_user()
this_users_workouts = get_usr_workouts()
for t in this_users_workouts:
  if t.id == workout_id:
  return render_template('deleteWorkoutConfirm.html', w_id = t)
return redirect(url_for('main'))

@app.route('/workout/del/confirm/<int:workout_id>', methods = ['POST', 'GET'])
@login_required
def del_Workout(workout_id):
  this_user = get_cur_user()
this_users_workouts = get_usr_workouts()
for t in this_users_workouts:
  if t.id == workout_id:
  this_w = session.query(W).filter_by(id = workout_id).one()
workouts_E = session.query(E).filter_by(w_id = workout_id).all()
for w in workouts_E:
  session.delete(w)
session.commit()
session.delete(this_w)
session.commit()
return redirect(url_for('main'))

@app.route('/workout/del/confirm/<int:exercise_id>/<int:w_id>/', methods = ['POST', 'GET'])
@login_required
def del_Exercise_Confirm(exercise_id, w_id):
  this_user = get_cur_user()
print(this_user.name_first)
this_users_workouts = get_usr_workouts()
this_exercise = session.query(E).filter_by(id = exercise_id).one();
for t in this_users_workouts:
  print('w_id is equal to ' + str(w_id) + 't id is equal to ' + str(t))
if w_id == t.id:
  return render_template('deleteConfirm.html', exercise_id = exercise_id, id = w_id, this_exercise = this_exercise)
return redirect(url_for('main'))

@app.route('/workout/del/<int:exercise_id>/<int:w_id>/<string:day>/', methods = ['POST', 'GET'])
@login_required
def del_Exercise(exercise_id, w_id, day):
  this_user = get_cur_user()
print(this_user.name_first)
this_users_workouts = get_usr_workouts()
for t in this_users_workouts:
  if session.query(E).filter_by(id = exercise_id).one().w_id == t.id:
  this_e = session.query(E).filter_by(id = exercise_id).one()
session.delete(this_e)
session.commit()
return redirect(url_for(day, workout_id = w_id))

return redirect(url_for('workout', id = w_id))

@app.route('/workout/stat/save/<int:w_id>/<int:sets>/<int:weight>/<string:name>/<int:reps>/<int:e_id>/')
@app.route('/workout/stat/save/<int:w_id>/<int:weight>/<string:name>/<int:reps>/<int:e_id>/')
@login_required
def record_Stats(w_id, sets, weight, name, reps, e_id):
  this_user = get_cur_user()
this_users_workouts = get_usr_workouts()
this_e = session.query(E).filter_by(id = e_id, user_id = this_user.id).one()
for t in this_users_workouts:
  if session.query(E).filter_by(id = e_id).one().w_id == t.id:
  print("we good yo")
print(sets)
today = datetime.now().date()
print(today)
stat_record = Stats(name_of = name, owner_id = this_user.id, sets_completed = sets, weight = weight, date_done = today)
session.add(stat_record)
session.commit()
for_fw = session.query(E).filter_by(id = e_id).one()
for_fw.previous_weight = weight
session.add(for_fw)
session.commit()
print(stat_record.name_of)
print(stat_record.owner_id)
print(stat_record.sets_completed)
print(stat_record.weight)
print(stat_record.date_done)
return redirect(url_for(this_e.day, workout_id = w_id))
return redirect(url_for(this_e.day, workout_id = w_id))

@app.route('/stats/')
@login_required
def user_stats():
  same_dates = []
this_user = get_cur_user()
this_users_workouts = get_usr_workouts()
all_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()

unique_dates = []
dates = []

names = []
unique_names = []

for i in all_stats:
  dates.append(i.date_done.date())
names.append(i.name_of)

for d in dates:
  while unique_dates.count(str(d)) < 1:
  print('doing while')
unique_dates.append(str(d))

for u in unique_dates:
  print('unique dates are ' + str(u))

for n in names:
  while unique_names.count(n) < 1:
  unique_names.append(n)
for u in unique_names:
  print('name is ' + u)

return render_template('statsMain.html', user = this_user, users_workouts = this_users_workouts, dates = unique_dates[::-1], names = unique_names)

@app.route('/stats/<string:stat_id>/')
@login_required
def user_stats_date(stat_id):
  same_dates = []
this_user = get_cur_user()
this_users_workouts = get_usr_workouts()
all_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
l_date = []
l_name_of = []
l_sets_completed = []
l_weight = []
l_owner_id = []
counter = 0
unique_dates = []

labels = []
values = []

for i in all_stats:
  print(str(i.date_done.date()) + ' is the date done')
if str(i.date_done.date()) == stat_id:

  labels.append(i.name_of)

for i in all_stats:
  for l in range(0, len(labels)):
  if i.name_of == labels[l] and str(i.date_done.date()) == stat_id:
  values.append(i.weight)
break
maxAmount = max(values) + 50
return render_template('stats.html', user = this_user, users_workouts = this_users_workouts, values = values, labels = labels, date = stat_id, maxAmount = maxAmount)

@app.route('/stats/names/<string:name>/')
@login_required
def user_stats_name(name):
  same_dates = []
this_user = get_cur_user()
this_users_workouts = get_usr_workouts()
all_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
l_date = []
l_name_of = []
l_sets_completed = []
l_weight = []
l_owner_id = []
counter = 0
unique_dates = []
print('name is ' + name)

labels = []
values = []

for i in all_stats:
  if i.name_of == name:
  labels.append(str(i.date_done.date()))

for i in range(0, len(all_stats)):
  for l in range(0, len(labels)):
  if str(all_stats[i].date_done.date()) == labels[l] and all_stats[i].name_of == name:
  values.append(all_stats[i].weight)
break
maxAmount = max(values) + 50

return render_template('statsName.html', user = this_user, users_workouts = this_users_workouts, values = values, labels = labels, name = name, maxAmount = maxAmount)

@app.route('/director/<string:day>/<int:workout_id>/')
@login_required
def director(day, workout_id):
  return redirect(url_for(day, workout_id = workout_id))

@app.route('/main/workout/monday/<int:workout_id>/')
@login_required
def monday(workout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisE = get_exercises(workout_id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
todays_e = session.query(E).filter_by(user_id = this_user.id, day = 'monday', w_id = workout_id).all()
all_e_desc = session.query(Common_E).all()
names = []
unique_names = []
name_id = []
tester = []
for i in all_user_e:
  names.append(i.name)
for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)
for n in name_id:
  print(n)
for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))
if thisWorkout.owner_id == this_user.id:
  return render_template('monday.html', thisWorkout = thisWorkout, day = "monday", all_e_desc = all_e_desc, all_e = todays_e, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

@app.route('/main/workout/tuesday/<int:workout_id>/')
@login_required
def tuesday(workout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisE = get_exercises(workout_id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
todays_e = session.query(E).filter_by(user_id = this_user.id, day = 'tuesday', w_id = workout_id).all()
all_e_desc = session.query(Common_E).all()
names = []
unique_names = []
name_id = []
tester = []
for i in all_user_e:
  names.append(i.name)
for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)
for n in name_id:
  print(n)
for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))
if thisWorkout.owner_id == this_user.id:
  return render_template('tuesday.html', thisWorkout = thisWorkout, day = "tuesday", all_e_desc = all_e_desc, all_e = todays_e, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

@app.route('/main/workout/wednesday/<int:workout_id>/')
@login_required
def wednesday(workout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisE = get_exercises(workout_id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
todays_e = session.query(E).filter_by(user_id = this_user.id, day = 'wednesday', w_id = workout_id).all()
all_e_desc = session.query(Common_E).all()
names = []
unique_names = []
name_id = []
tester = []
for i in all_user_e:
  names.append(i.name)
for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)
for n in name_id:
  print(n)
for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))
if thisWorkout.owner_id == this_user.id:
  return render_template('wednesday.html', thisWorkout = thisWorkout, day = "wednesday", all_e_desc = all_e_desc, all_e = todays_e, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

@app.route('/main/workout/thursday/<int:workout_id>/')
@login_required
def thursday(workout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisE = get_exercises(workout_id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
todays_e = session.query(E).filter_by(user_id = this_user.id, day = 'thursday', w_id = workout_id).all()
all_e_desc = session.query(Common_E).all()
names = []
unique_names = []
name_id = []
tester = []
for i in all_user_e:
  names.append(i.name)
for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)
for n in name_id:
  print(n)
for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))
if thisWorkout.owner_id == this_user.id:
  return render_template('thursday.html', thisWorkout = thisWorkout, day = "thursday", all_e_desc = all_e_desc, all_e = todays_e, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

@app.route('/main/workout/friday/<int:workout_id>/')
@login_required
def friday(workout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisE = get_exercises(workout_id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
todays_e = session.query(E).filter_by(user_id = this_user.id, day = 'friday', w_id = workout_id).all()
all_e_desc = session.query(Common_E).all()
names = []
unique_names = []
name_id = []
tester = []
for i in all_user_e:
  names.append(i.name)
for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)
for n in name_id:
  print(n)
for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))
if thisWorkout.owner_id == this_user.id:
  return render_template('friday.html', thisWorkout = thisWorkout, day = "friday", all_e_desc = all_e_desc, all_e = todays_e, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

@app.route('/main/workout/saturday/<int:workout_id>/')
@login_required
def saturday(workout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisE = get_exercises(workout_id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
todays_e = session.query(E).filter_by(user_id = this_user.id, day = 'saturday', w_id = workout_id).all()
all_e_desc = session.query(Common_E).all()
names = []
unique_names = []
name_id = []
tester = []
for i in all_user_e:
  names.append(i.name)
for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)
for n in name_id:
  print(n)
for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))
if thisWorkout.owner_id == this_user.id:
  return render_template('saturday.html', thisWorkout = thisWorkout, day = "saturday", all_e_desc = all_e_desc, all_e = todays_e, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

@app.route('/main/workout/sunday/<int:workout_id>/')
@login_required
def sunday(workout_id):
  this_user = get_cur_user()
thisWorkout = session.query(W).filter_by(id = workout_id).one()
thisE = get_exercises(workout_id)
user_stats = session.query(Stats).filter_by(owner_id = this_user.id).all()
all_user_e = session.query(E).filter_by(user_id = this_user.id).all()
todays_e = session.query(E).filter_by(user_id = this_user.id, day = 'sunday', w_id = workout_id).all()
all_e_desc = session.query(Common_E).all()
names = []
unique_names = []
name_id = []
tester = []
for i in all_user_e:
  names.append(i.name)
for d in names:
  while unique_names.count(str(d)) < 1:
  unique_names.append(str(d))
for a in all_user_e:
  for u in unique_names:
  if u == a.name:
  while tester.count(str(a.name)) < 1:
  print('name of exercise is ' + a.name + ' id of exercise is ' + str(a.id))
name_id.append(a.id)
tester.append(a.name)
for n in name_id:
  print(n)
for n in unique_names:
  print(n)
print('length of names is equal to ' + str(len(unique_names)))
print(len(name_id))
if thisWorkout.owner_id == this_user.id:
  return render_template('sunday.html', thisWorkout = thisWorkout, day = "sunday", all_e_desc = all_e_desc, all_e = todays_e, unique_names = unique_names, name_id = name_id, user_stats = user_stats, user = this_user, all_user_e = all_user_e)
return redirect(url_for('main'))

if __name__ == '__main__':
  app.debug = False
app.run('0.0.0.0')
