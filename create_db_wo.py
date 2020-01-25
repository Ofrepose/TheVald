import sys, os, sqlalchemy,datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, BigInteger, create_engine, Float,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base = declarative_base()

class User(UserMixin, Base):
	__tablename__ = 'user'

	name_first = Column(
		String(80), nullable = False)

	name_last = Column(
		String(80), nullable = False)

	email = Column(
		String(180), nullable = False)

	p = Column(
		String(80), nullable = False)

	is_validated = Column(
		String(80), default = 'no')

	initial_key = Column(
		BigInteger)

	pValid = Column(
		Integer, default = 1 )

	profile_picture = Column(
		String(180))

	starting_weight = Column(
		Integer)

	current_weight = Column(
		String(180))

	goal_photo_ini = Column(
		String(180))

	goal_photo_2 = Column(
		String(180))

	goal_photo_3 = Column(
		String(180))

	e_rated = Column(
		Text())

	r_1 = Column(
		Text())

	r_2 = Column(
		Text())

	r_3 = Column(
		Integer)

	r_4 = Column(
		Integer)

	id = Column(
		Integer, primary_key = True)

class W(Base):
	__tablename__ = 'w'

	name = Column(
		String(180))

	owner_id = Column(
		Integer, ForeignKey('user.id'))

	user = relationship(User)

	has_weeks = Column(
		Boolean, default = True )

	uploaded = Column(
		Boolean, default = False)

	original_owner = Column(
		Integer, default = 0)
	
	rating = Column (
		Integer, default = 0)

	description = Column(
		Text())

	full_body = Column(
		Boolean, default = False)

	upper_body = Column(
		Boolean, default = False)

	lower_body = Column(
		Boolean, default = False)

	featured = Column(
		Boolean, default = False)

	download_count = Column(
		Integer, default = 0)

	r_1 = Column(
		Text())

	r_2 = Column(
		Text())

	r_3 = Column(
		Integer)

	r_4 = Column(
		Integer)

	id = Column(
		Integer, primary_key = True)



class E(Base):
	__tablename__ = 'e'

	name = Column(
		String(180))

	sets = Column(
		Integer, default = 0)

	reps = Column(
		Integer, default = 0)

	rest_between_minutes = Column(
		Integer, default = 0)

	rest_between_seconds = Column(
		Integer, default = 0)

	time_for_set = Column(
		Integer, default = 0)

	w_id = Column(
		Integer, ForeignKey('w.id'))

	w = relationship(W)

	user_id = Column(
		Integer, ForeignKey('user.id'))

	user = relationship(User)

	weight = Column(
		Integer, default = 0)

	previous_weight = Column(
		Integer, default = 0)

	day = Column(
		String(80))

	r_1 = Column(
		Text())

	r_2 = Column(
		Text())

	r_3 = Column(
		Integer)

	r_4 = Column(
		Integer)

	id = Column(
		Integer, primary_key = True)



class Stats(Base):
	__tablename__ = 'stats'

	id = Column(
		Integer, primary_key = True)

	name_of = Column(
		String(80), nullable = False)

	owner_id = Column(
		Integer, ForeignKey('user.id'))

	user = relationship(User)

	sets_completed = Column(
		Integer, default = 0)

	weight = Column(
		Integer, default = 0)

	date_done = Column (
		DateTime, nullable = False)

	r_1 = Column(
		Text())

	r_2 = Column(
		Text())

	r_3 = Column(
		Integer)

	r_4 = Column(
		Integer)

class Common_E(Base):
	__tablename__ = 'common_e'

	id = Column(
		Integer, primary_key = True)

	name = Column(
		String(180))

	description = Column(
		Text())

	photo = Column(
		String(180))

	r_1 = Column(
		Text())

	r_2 = Column(
		Text())

	r_3 = Column(
		Integer)

	r_4 = Column(
		Integer)







engine = create_engine('sqlite:///wo_db_engine.db')
Base.metadata.create_all(engine)