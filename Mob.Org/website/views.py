from urllib import response
from flask import Blueprint, redirect, render_template, request, session,url_for
import flask
views = Blueprint('views',__name__)
from . import mysql

##user side
@views.route('/')
def index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM t_item WHERE id = 1")
    if resultValue > 0:
        userDetails = cur.fetchall()
        result = cur.execute("SELECT * FROM t_item LIMIT 5")
        if result > 0:
            details = cur.fetchall()
        if 'username' in session:
            username = "username"
            return render_template("index.html",userDetails=userDetails,details=details,username=username)
        else:
            return render_template("index.html",userDetails=userDetails,details=details)
    #return render_template("index.html") May error didi kay waray nagreturn if (resultValue > 0) is False

@views.route('/view_item/<string:id_data>',methods=['GET','POST'])
def view_item(id_data):
    cur = mysql.connection.cursor()
    session['view_id_data'] = id_data
    revDetails = cur.execute("SELECT * FROM user_review WHERE item_id =%s LIMIT 4",(id_data))
    revDetails = cur.fetchall()
    itemDetails = cur.execute("SELECT * FROM t_item WHERE id =%s",(id_data))
    itemDetails = cur.fetchone()
    if itemDetails:
        if 'username' and 'user_id' in session:
            username = "username"
            user_id = session['user_id']
            if request.method == 'POST':
                status = request.form['status']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                ep_seen = request.form['ep_seen']
                rating = request.form['rating']
                if ep_seen > itemDetails[3]:
                    pass
                else:
                    cur.execute("""INSERT INTO t_list (user_id,item_id,start_date,end_date,ep_seen,rating,list_status)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                            (user_id,id_data,start_date,end_date,ep_seen,rating,status))
                    mysql.connection.commit()
            listDetails = cur.execute("SELECT * FROM t_list WHERE user_id = %s AND item_id =%s",(user_id,id_data))
            listDetails = cur.fetchone()
            if listDetails:
                bool_listdetails = "true"
                return render_template("view_item.html",itemDetails=itemDetails,username=username,bool_listdetails=bool_listdetails,listDetails=listDetails,revDetails=revDetails)
            return render_template("view_item.html",itemDetails=itemDetails,username=username,revDetails=revDetails)
        return render_template("view_item.html",itemDetails=itemDetails,revDetails=revDetails)

@views.route('/view_edit_item',methods=['GET','POST'])
def view_edit_item():
    cur = mysql.connection.cursor()
    if 'view_id_data' and 'username' and 'user_id'in session:
        id_data = session['view_id_data']
        user_id = session['user_id']
        if request.method == 'POST':
            status = request.form['status']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            ep_seen = request.form['ep_seen']
            rating = request.form['rating']
            cur.execute(""" UPDATE t_list SET start_date=%s, end_date=%s, ep_seen=%s, rating=%s, list_status=%s WHERE user_id=%s AND item_id=%s"""
                                    ,(start_date,end_date,ep_seen,rating,status,user_id,id_data))
            mysql.connection.commit()
            return redirect(url_for("views.view_item",id_data = id_data))

@views.route('/view_all_review',methods=['GET','POST'])
def view_all_review():
    cur = mysql.connection.cursor()
    id_data = session['view_id_data']
    view_all_review = "true"
    itemDetails = cur.execute("SELECT * FROM t_item WHERE id =%s",(id_data))
    itemDetails = cur.fetchone()
    if itemDetails:
        reviewDetails = cur.execute("SELECT * FROM user_review WHERE item_id = %s",(id_data))
        if reviewDetails > 0:
            reviewDetails = cur.fetchall()
            if 'username' and 'user_id' in session:
                username = "username"
                user_id = session['user_id']
                listDetails = cur.execute("SELECT * FROM t_list WHERE user_id = %s AND item_id =%s",(user_id,id_data))
                listDetails = cur.fetchone()
                if listDetails:
                    bool_listdetails = "true"
                    return render_template("view_item.html",view_all_review=view_all_review,itemDetails=itemDetails,username=username,bool_listdetails=bool_listdetails,listDetails=listDetails,reviewDetails=reviewDetails)
            return render_template("view_item.html",view_all_review=view_all_review,itemDetails=itemDetails,reviewDetails=reviewDetails)
        else:
            if 'username' and 'user_id' in session:
                username = "username"
                user_id = session['user_id']
                listDetails = cur.execute("SELECT * FROM t_list WHERE user_id = %s AND item_id =%s",(user_id,id_data))
                listDetails = cur.fetchone()
                if listDetails:
                    bool_listdetails = "true"
                    return render_template("view_item.html",view_all_review=view_all_review,itemDetails=itemDetails,username=username,bool_listdetails=bool_listdetails,listDetails=listDetails)
            return render_template("view_item.html",view_all_review=view_all_review,itemDetails=itemDetails)

            
@views.route('/add_review', methods=['GET','POST'])
def add_review():
    cur = mysql.connection.cursor()
    id_data = session['view_id_data']
    revDetails = cur.execute("SELECT * FROM user_review WHERE item_id =%s LIMIT 4",(id_data))
    revDetails = cur.fetchall()
    itemDetails = cur.execute("SELECT * FROM t_item WHERE id =%s",(id_data))
    itemDetails = cur.fetchone()
    if itemDetails:
        if 'view_id_data' and 'username' and 'user_id' in session:
            username = "username"
            user_id = session['user_id']
            listDetails = cur.execute("SELECT * FROM t_list WHERE user_id = %s AND item_id =%s",(user_id,id_data))
            listDetails = cur.fetchone()
            if listDetails:
                bool_listdetails = "true"
                if request.method == 'POST':
                    review_date = request.form['review_date']
                    add_review = request.form['add_review']
                    cur.execute(""" INSERT INTO t_review (user_id,item_id,r_date,rv_description) VALUES (%s,%s,%s,%s)""",
                                    (user_id,id_data,review_date,add_review))
                    mysql.connection.commit()
                ##return render_template("view_item.html",itemDetails=itemDetails,username=username,bool_listdetails=bool_listdetails,listDetails=listDetails,revDetails=revDetails)
                return redirect(url_for("views.view_item",id_data = id_data))
            else:
                ## need to be revised tommorow
                return render_template("login.html")
        else:
            return render_template("login.html")
        

##admin side
@views.route('/admin_base')
def home():
    return redirect("/film_table", code=301)

#--------------------------------- ADD FILM ---------------------------------------------------#
@views.route('/add_film', methods=['GET','POST'])
def add_film():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['item_name']
        type = "TV"
        episode = request.form['episode']
        date = request.form['date']
        source = request.form['source']
        demographic = request.form['demographic']
        duration = request.form['duration']
        synopsis = request.form['synopsis']
        background = request.form['background']
        poster = request.form['poster']
        trailer = request.form['trailer']
        cur.execute(""" INSERT INTO 
                    t_item (item_name,t_type,episode,date_release,item_source,demographic,duration,synopsis,background,poster,trailer) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """,(name,type,episode,date,source,demographic,duration,synopsis,background,poster,trailer))
        mysql.connection.commit()
        return redirect(url_for("views.film_table"))
    return render_template("add_film.html")

#--------------------------------- VIEW FILM TABLE ---------------------------------------------------#
#Cid
@views.route('/film_table')
def film_table():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("Select * FROM t_item")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template("table_film.html",userDetails=userDetails)
    return render_template("table_film.html")

#--------------------------------- DELETE FILM TABLE ---------------------------------------------------#
@views.route('/delete_film/<string:id_data>')
def delete_film(id_data):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM t_item WHERE id=%s""",(id_data))
    cur.execute("ALTER TABLE t_item AUTO_INCREMENT = 1")
    mysql.connection.commit()
    return redirect(url_for("views.film_table"))

#--------------------------------- UPDATE FILM TABLE ---------------------------------------------------#
@views.route('/update_film/<string:id_data>', methods=['GET','POST'])
def update_film(id_data):
   cur = mysql.connection.cursor()
   resultValue = cur.execute("Select * FROM t_item WHERE id = %s",(id_data))
   if resultValue > 0:
        userDetails = cur.fetchall()
        if request.method == 'POST':
            name = request.form['item_name']
            episode = request.form['episode']
            date = request.form['date']
            source = request.form['source']
            demographic = request.form['demographic']
            duration = request.form['duration']
            synopsis = request.form['synopsis']
            background = request.form['background']
            poster = request.form['poster']
            trailer = request.form['trailer']
            cur.execute(""" UPDATE t_item SET item_name=%s, episode=%s,date_release=%s,item_source=%s,
                        demographic=%s,duration=%s,synopsis=%s,background=%s,poster=%s,trailer=%s WHERE id=%s""",
                        (name,episode,date,source,demographic,duration,synopsis,background,poster,trailer,id_data))
            mysql.connection.commit()
            return redirect(url_for("views.film_table"))
        return render_template("update_film.html",userDetails=userDetails)
   return render_template("update_film.html")

#--------------------------------- ADD CHARACTER DIRECTOR TO A FILM---------------------------------------------------#
#Cid
@views.route('/film_table/<string:id_data>/<string:view_type>', methods=['GET', 'POST'])
def film_character_director(id_data, view_type):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        if view_type == "characters":
            item_character_list = cur.execute("""SELECT 
                t_character.id, 
                t_character.char_fname, 
                t_character.char_lname, 
                t_character.char_role, 
                t_character.char_poster FROM t_character 
                INNER JOIN t_char_item ON t_char_item.char_id = t_character.id 
                and t_char_item.item_id = %s""", (id_data))
            has_char = False
            if item_character_list > 0:
                item_character_list_result = cur.fetchall()
                has_char = True
            character_list = cur.execute("SELECT * FROM t_character")
            if character_list > 0 and has_char:
                character_list_result = cur.fetchall()
                return render_template("film_character_director.html", 
                                        result_list = item_character_list_result, 
                                        character_list = character_list_result,
                                        film_id = id_data, 
                                        view_type = view_type)
            elif character_list > 0:
                character_list_result = cur.fetchall()
                return render_template("film_character_director.html", 
                                        result="NULL", 
                                        character_list=character_list_result,
                                        film_id = id_data,
                                        view_type = view_type)
            else:
                return render_template("film_character_director.html", 
                                        result="NULL", 
                                        character_list="NULL",
                                        film_id = id_data,
                                        view_type= view_type)

        elif view_type == "directors":
            item_director_list = cur.execute("""SELECT 
                t_director.id, 
                t_director.direct_fname, 
                t_director.direct_lname FROM t_director 
                INNER JOIN t_item_director ON t_director.id = t_item_director.director_id
                and t_item_director.item_id = %s""", (id_data))
            has_dir = False
            if item_director_list > 0:
                item_director_list_result = cur.fetchall()
                has_dir = True
            director_list = cur.execute("SELECT * FROM t_director")
            if director_list > 0 and has_dir:
                director_list_result = cur.fetchall()
                return render_template("film_character_director.html", 
                                        result_list = item_director_list_result, 
                                        director_list = director_list_result,
                                        film_id = id_data, 
                                        view_type= view_type)
            elif director_list > 0:
                director_list_result = cur.fetchall()
                return render_template("film_character_director.html", 
                                        result="NULL", 
                                        director_list=director_list_result,
                                        film_id = id_data,
                                        view_type= view_type)
            else:
                return render_template("film_character_director.html", 
                                        result="NULL", 
                                        character_list="NULL",
                                        film_id = id_data,
                                        view_type= view_type)
   
    elif request.method == "POST":
        if view_type == "characters":
            character_id = request.form['form-select']
            cur.execute(""" INSERT INTO t_char_item (char_id, item_id) 
                VALUES (%s, %s) """,(character_id, id_data))
            mysql.connection.commit()
        elif view_type == "directors":
            director_id = request.form['form-select']
            cur.execute(""" INSERT INTO t_item_director (director_id, item_id) 
                VALUES (%s, %s) """,(director_id, id_data))
            mysql.connection.commit()
        return flask.redirect("/film_table/"+id_data+"/"+view_type, code=301)
    return redirect(url_for("views.film_table"))

#--------------------------------- DELETE CHARACTER DIRECTOR FROM A FILM ---------------------------------------------------#
#Cid
@views.route('/film_table/<string:id_data>/<string:view_type>/delete/<string:view_type_id>')
def delete_film_character_director(id_data, view_type, view_type_id):
    cur = mysql.connection.cursor()
    if view_type == "characters":
        cur.execute("DELETE FROM t_char_item WHERE char_id = %s AND item_id = %s",(view_type_id, id_data))
        mysql.connection.commit()
        cur.execute("DELETE FROM t_actor_char WHERE char_id = %s", (view_type_id))
        mysql.connection.commit()
    elif view_type == "directors":
        cur.execute("DELETE FROM t_item_director WHERE director_id = %s AND item_id = %s",(view_type_id, id_data))
        mysql.connection.commit()
    return flask.redirect("/film_table/"+id_data+"/"+view_type, code=301)

#--------------------------------- VIEW CHARACTER TABLE ---------------------------------------------------#
#Cid
@views.route('/admin_base/characters/view', methods=['GET', 'POST'])
def view_character():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        result = cur.execute('SELECT * FROM t_character')
        if result > 0:
            characters_result = cur.fetchall()
            return render_template("view_character_director.html", 
                                        view_type="characters",
                                        type = "view",
                                        result_list = characters_result)
        return render_template("view_character_director.html", 
                                    view_type="characters",
                                    type = "view",
                                    result_list = "NULL")
    elif request.method == 'POST':
        char_fname = request.form['characterFName']
        char_lname = request.form['characterLName']
        char_role = request.form['characterRole']
        char_poster_url = request.form['characterPosterURL']
        print(char_fname, char_lname, char_role, char_poster_url)
        result = cur.execute("""INSERT INTO t_character(char_fname, char_lname, char_role, char_poster) 
                            VALUES (%s, %s, %s, %s)""",(char_fname, char_lname, char_role, char_poster_url))
        mysql.connection.commit()
        return flask.redirect("/admin_base/characters/view", code=301)

#--------------------------------- VIEW DIRECTORS TABLE ---------------------------------------------------#
#Cid
@views.route('/admin_base/directors/view', methods=['GET', 'POST'])
def view_director():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        result = cur.execute('SELECT * FROM t_director')
        if result > 0:
            directors_result = cur.fetchall()
            return render_template("view_character_director.html", 
                                        view_type = "directors",
                                        type = "view", 
                                        result_list = directors_result)
        return render_template("view_character_director.html", 
                                    view_type = "directors",
                                    type = "view", 
                                    result_list = "NULL")
    elif request.method == 'POST':
        dir_fname = request.form['directorFName']
        dir_lname = request.form['directorLName']
        result = cur.execute("""INSERT INTO t_director(direct_fname, direct_lname) 
                                    VALUES (%s, %s)""",(dir_fname, dir_lname))
        mysql.connection.commit()
        return flask.redirect("/admin_base/directors/view", code=301)

#--------------------------------- EDIT ViEW CHARACTERS TABLE---------------------------------------------------#
#Cid
@views.route('/admin_base/characters/edit/<string:id>', methods=['GET', 'POST'])
def view_edit_character(id):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        selected_character = cur.execute('SELECT * FROM t_character WHERE id = %s', (id,)) #Take note of comma
        selected_character = cur.fetchone()
        result = cur.execute('SELECT * FROM t_character')
        if result > 0:
            characters_result = cur.fetchall()
            return render_template("view_character_director.html", 
                                        view_type="characters",
                                        type = "edit",
                                        character = selected_character,
                                        result_list = characters_result)
        return render_template("view_character_director.html", 
                                    view_type="characters",
                                    type = "edit",
                                    character = selected_character,
                                    result_list = "NULL")
    elif request.method == 'POST':
        char_fname = request.form['characterFName']
        char_lname = request.form['characterLName']
        char_role = request.form['characterRole']
        char_poster_url = request.form['characterPosterURL']
        result = cur.execute("""UPDATE t_character SET 
                                char_fname = %s,
                                char_lname = %s,
                                char_role = %s,
                                char_poster = %s 
                                WHERE id = %s""",(char_fname, char_lname, char_role, char_poster_url, id))
        mysql.connection.commit()
        return flask.redirect("/admin_base/characters/view", code=301)

#--------------------------------- EDIT ViEW DIRECTORS TABLE---------------------------------------------------#
#Cid
@views.route('/admin_base/directors/edit/<string:id>', methods=['GET', 'POST'])
def view_edit_director(id):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        selected_director = cur.execute('SELECT * FROM t_director WHERE id = %s', (id,)) #Take note of comma
        selected_director = cur.fetchone()
        result = cur.execute('SELECT * FROM t_director')
        if result > 0:
            characters_result = cur.fetchall()
            return render_template("view_character_director.html", 
                                    view_type="directors",
                                    type = "edit",
                                    director = selected_director,
                                    result_list = characters_result)
        return render_template("view_character_director.html", 
                                view_type="directors",
                                director = selected_director,
                                type = "edit",
                                result_list = "NULL")
    elif request.method == "POST":
        dir_fname = request.form['directorFName']
        dir_lname = request.form['directorLName']
        cur.execute("""UPDATE t_director SET 
                    direct_fname = %s,
                    direct_lname = %s 
                    WHERE %s""", (dir_fname, dir_lname, id))
        mysql.connection.commit()
        return flask.redirect("/admin_base/directors/view", code=301)

#--------------------------------- DELETE VIEW CHARACTER TABLE---------------------------------------------------#
#Cid
@views.route('/admin_base/characters/delete/<string:id>')
def view_delete_character(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM t_char_item WHERE char_id = "+id)
    mysql.connection.commit()
    cur.execute("DELETE FROM t_actor_char WHERE char_id = "+id)
    mysql.connection.commit()
    cur.execute("DELETE FROM t_character WHERE id = "+id)
    mysql.connection.commit()
    return flask.redirect("/admin_base/characters/view", code=301)

#--------------------------------- DELETE VIEW DIRECTOR TABLE---------------------------------------------------#
#Cid
@views.route('/admin_base/directors/delete/<string:id>')
def view_delete_director( id):
    print("DElete DIRECTTORS")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM t_item_director WHERE director_id = %s", (id))
    mysql.connection.commit()
    cur.execute("DELETE FROM t_director WHERE id = %s", (id))
    mysql.connection.commit()
    return flask.redirect("/admin_base/directors/view", code=301)

#--------------------------------- ACTOR TABLE ---------------------------------------------------#
#Cid
@views.route('/view_actors', methods=['GET','POST'])
def film_actor():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        result = cur.execute("SELECT * from t_actor")
        if result > 0:
            result = cur.fetchall()
            return render_template("view_actor.html", actors = result, type="view")
        else:
            return render_template("view_actor.html", actors = "NULL", type="view")
    elif request.method == "POST":
        actor_fname = request.form['actorFName']
        actor_lname = request.form['actorLName']
        cur.execute("INSERT INTO t_actor(actor_fname, actor_lname) VALUES (%s, %s)", (actor_fname, actor_lname))
        mysql.connection.commit()
        return flask.redirect("/view_actors", code = 301)

#--------------------------------- ACTOR ADD ROLE TABLE ---------------------------------------------------#
#Cid
@views.route('/view_actors/add_role/<string:actor_id>', methods=['GET','POST'])
def add_role_actor(actor_id):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        actor_result = cur.execute("SELECT * FROM t_actor WHERE id = %s",(actor_id))
        actor_result = cur.fetchone()
        actor_character_list = cur.execute("""SELECT 
                    t_character.id, 
                    t_character.char_fname, 
                    t_character.char_lname, 
                    t_character.char_role, 
                    t_character.char_poster FROM t_character 
                    INNER JOIN t_actor_char 
                    ON t_actor_char.char_id = t_character.id 
                    and t_actor_char.actor_id = %s""", (actor_id))
        actor_character_list = cur.fetchall()
        actor_character_list = [list(actor_character) for actor_character in list(actor_character_list)]
        actor_character_list_with_film_title = []
        for character in actor_character_list:
            char_id = str(character[0])
            film_title = cur.execute("""SELECT 
                                    t_item.item_name FROM t_item 
                                    INNER JOIN t_char_item 
                                    ON t_item.id = t_char_item.item_id 
                                    and t_char_item.char_id = """+char_id)
            film_title_result = "Not Set"
            if film_title > 0:
                film_title = cur.fetchone()
                film_title_result = list(film_title)
            character.append(film_title_result)
            actor_character_list_with_film_title.append(character)

        available_character_list = cur.execute("""SELECT 
                    t_character.id, 
                    t_character.char_fname, 
                    t_character.char_lname, 
                    t_character.char_role FROM t_character""")
        available_character_list = cur.fetchall()
        return render_template("add_char_actor.html", 
                                actor = actor_result ,
                                actor_characters = actor_character_list_with_film_title,
                                character_list = available_character_list)
    elif request.method == "POST":
        c_id = request.form['form-select']
        cur.execute("""INSERT INTO 
                    t_actor_char(char_id, actor_id) 
                    VALUES (%s, %s)""",(c_id, actor_id))
        mysql.connection.commit()
        return flask.redirect("/view_actors/add_role/"+actor_id, code= 301)

#--------------------------------- ACTOR DELETE ROLE TABLE ---------------------------------------------------#
#Cid
@views.route('/view_actors/delete_role/<string:actor_id>/<string:char_id>')
def delete_role_actor(actor_id, char_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM t_actor_char WHERE actor_id = %s and char_id = %s", (actor_id, char_id))
    mysql.connection.commit()
    return flask.redirect("/view_actors/add_role/"+actor_id, code=301)

#--------------------------------- EDIT ACTOR TABLE ---------------------------------------------------#
#Cid
@views.route('/view_actors/edit/<string:actor_id>', methods=['GET','POST'])
def edit_actor(actor_id):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        result = cur.execute("SELECT * FROM t_actor WHERE id = %s", (actor_id))
        if result > 0:
            actor = cur.fetchone()
            actors = cur.execute("SELECT * from t_actor")
            if actors > 0:
                actors = cur.fetchall()
                return render_template("view_actor.html", type="edit", actors = actors, actor=actor)
    elif request.method == "POST":
        actor_fname = request.form['actorFName']
        actor_lname = request.form['actorLName']
        cur = mysql.connection.cursor()
        result = cur.execute("""UPDATE t_actor SET actor_fname = %s , actor_lname = %s 
                                WHERE id = %s """, (actor_fname, actor_lname, actor_id))
        mysql.connection.commit()
        return flask.redirect("/view_actors", code=301)
          
#--------------------------------- DELETE ACTOR TABLE ---------------------------------------------------#
#Cid
@views.route('/view_actors/delete/<string:actor_id>', methods=['GET','POST'])
def delete_actor(actor_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM t_actor WHERE id = %s", (actor_id))
    mysql.connection.commit()
    cur.execute("DELETE FROM t_actor_char WHERE actor_id = %s", (actor_id))
    mysql.connection.commit()
    return flask.redirect("/view_actors", code=301)

#--------------------------------- DELETE ACTOR TABLE ---------------------------------------------------#
#Cid
@views.route('/view_genre', methods=['GET','POST'])
def view_genre():
    return render_template("view_genre.html")


