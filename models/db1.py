# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
db.define_table('airport_info',
                Field('name', 'string'),
                Field('city', 'string'),
                Field('country', 'string'),
                Field('three_letter_code', 'string'),
                Field('latitude', 'double'),
                Field('longitude', 'double'))

db.define_table('user_airport_code',
                Field('three_letter_code', 'string' ),
                Field('created_on', 'datetime', default=request.now),
                Field('created_by', db.auth_user,   writable=False, default=auth.user_id),
               auth.signature)
db.user_airport_code.three_letter_code.widget = SQLFORM.widgets.autocomplete(request, db.airport_info.three_letter_code, limitby=(0,10), min_length=1)


db.define_table('user_dest',
                Field('three_letter_code', 'string'),
                Field('created_on', 'datetime', default =request.now),
                Field('created_by', db.auth_user,writable=False, default = auth.user_id))
db.user_dest.three_letter_code.widget = SQLFORM.widgets.autocomplete(request, db.airport_info.three_letter_code, limitby=(0,10), min_length=1)
if auth.is_logged_in():
    db.user_dest.three_letter_code.requires = IS_NOT_IN_DB(db((db.user_dest.three_letter_code == request.vars.three_letter_code) & (db.user_dest.created_by==auth.user.id)), 'user_dest.three_letter_code')

db.define_table('user_request_images',
                Field('image_path', 'string'),
                Field('link_to', 'string'),
                Field('source_code', 'string'),
                Field('destination_code', 'string'),
                Field('depart_date', 'date'),
                Field('return_date', 'date'),
                Field('created_on', 'datetime', default=request.now),
                Field('created_by', db.auth_user, default=auth.user_id),
               auth.signature)

db.define_table('user_flight_prices',
                Field('src_three_letter_code', 'string'),
                Field('dest_three_letter_code', 'string'),
                Field('price', 'double'),
                Field('departure_date', 'string'),
                Field('return_date', 'string'),
                Field('created_on', 'datetime', default=request.now),
                Field('created_by', db.auth_user, writable=False, default=auth.user_id))
