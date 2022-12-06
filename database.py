import psycopg2
from psycopg2 import Error
from config import password_db
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT





class DataBase():
    def __init__(self, name_db):
        self.name_db = name_db


    def new_dbase(self):
       
        try:
            connection = psycopg2.connect(user="postgres",
                                            password=password_db,
                                            host="127.0.0.1",
                                            port="5432")

            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            sql_create_database = f'create database {self.name_db}'
            cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()



   
    def new_table(self, create_table_query):

        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)

            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()



    def add_user(self, user_id):
        
        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)
            cursor = connection.cursor()
            select_query = f"select exists(select user_id_vk from users where user_id_vk = {user_id})"
            cursor.execute(select_query)
            user_bool = cursor.fetchone()[0]
            if user_bool == False:
                insert_query = f""" INSERT INTO users (user_id_vk) 
                                VALUES 
                                ({user_id})"""
                cursor.execute(insert_query)
                connection.commit()
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"

        finally:
            if connection:
                cursor.close()
                connection.close()





    def add_data_user(self, user_id_vk, sex, relation, city, bdate):
        
        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)
            cursor = connection.cursor()
            select_query = f"select id_user from users where user_id_vk = {user_id_vk}"
            cursor.execute(select_query)
            id_user = cursor.fetchone()[0]
            select_query = f"select exists(select fk_id_user from users_data where fk_id_user = {id_user})"
            cursor.execute(select_query)
            fk_id_user = cursor.fetchone()[0]
            if fk_id_user == False:
                age = 2022 - int(bdate)
                insert_query = f""" INSERT INTO users_data (user_data_sex, user_data_relation, user_data_city, user_data_age, fk_id_user) 
                                VALUES 
                                ({sex}, {relation}, {city}, {age}, {id_user})"""
                cursor.execute(insert_query)
                connection.commit()
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()



    def update_city(self, user_id_vk, city):

        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)
            cursor = connection.cursor()
            select_query = f"select id_user from users where user_id_vk = {user_id_vk}"
            cursor.execute(select_query)
            id_user = cursor.fetchone()[0]
            update_query = f"update users_data set user_data_city = {city} where fk_id_user = {id_user}"
            cursor.execute(update_query)
            connection.commit()   
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()



    def update_age(self, user_id_vk, age):

        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)
            cursor = connection.cursor()
            select_query = f"select id_user from users where user_id_vk = {user_id_vk}"
            cursor.execute(select_query)
            id_user = cursor.fetchone()[0]
            update_query = f"update users_data set user_data_age = {age} where fk_id_user = {id_user}"
            cursor.execute(update_query)
            connection.commit()
            
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()






    def update_sex(self, user_id_vk, sex):

        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)

            cursor = connection.cursor()
            select_query = f"select id_user from users where user_id_vk = {user_id_vk}"
            cursor.execute(select_query)
            id_user = cursor.fetchone()[0]
            # kent = record
            update_query = f"update users_data set user_data_sex = {sex} where fk_id_user = {id_user}"
            cursor.execute(update_query)
            connection.commit()
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()



    def update_relation(self, user_id_vk, relation):

        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)

            cursor = connection.cursor()
            select_query = f"select id_user from users where user_id_vk = {user_id_vk}"
            cursor.execute(select_query)
            id_user = cursor.fetchone()[0]
            # kent = record
            update_query = f"update users_data set user_data_relation = {relation} where fk_id_user = {id_user}"
            cursor.execute(update_query)
            connection.commit()
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()




    def add_profileToUser(self, user_id_vk, profile):

        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)
            cursor = connection.cursor()
            select_query = f"select id_user from users where user_id_vk = {user_id_vk}"
            cursor.execute(select_query)
            id_user = cursor.fetchone()[0]
            select_query = f"""select exists(select id_profile_vk from view_profiles where id_profile_vk = {profile})"""
            cursor.execute(select_query)
            id_send_user = cursor.fetchone()[0]
            if id_send_user == False:
                insert_query = f""" INSERT INTO view_profiles (fk_id_user, id_profile_vk) 
                                VALUES 
                                ({id_user}, {profile})"""
                cursor.execute(insert_query)
                connection.commit()
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()




    def out_data_user(self, user_id_vk):

        user_data = []
        try:
            connection = psycopg2.connect(user="postgres",
                                        password=password_db,
                                        host="127.0.0.1",
                                        port="5432",
                                        database=self.name_db)
            cursor = connection.cursor()
            select_query = f"select id_user from users where user_id_vk = {user_id_vk}"
            cursor.execute(select_query)
            id_user = cursor.fetchone()[0]
            select_query = f"select * from users_data where fk_id_user = {id_user}"
            cursor.execute(select_query)
            user_data = cursor.fetchone()
        except (Exception, Error) as error:
            db_error = f"Ошибка при работе с PostgreSQL, {error}"
        finally:
            if connection:
                cursor.close()
                connection.close()
                
        return user_data



vkinder = DataBase("vkinder")

vkinder.new_dbase()

vkinder.new_table(create_table_query = '''CREATE TABLE users
                                (id_user serial PRIMARY KEY,
                                user_id_vk  integer  unique NOT NULL); ''')

vkinder.new_table(create_table_query = '''CREATE TABLE users_data
                                (id_user_data serial PRIMARY KEY,
                                user_data_sex  integer  NOT NULL,
                                user_data_relation  integer  NOT NULL,
                                user_data_city  integer  NOT NULL,
                                user_data_age  integer  NOT NULL,
                                fk_id_user  integer  NOT NULL references users(id_user)); ''')

vkinder.new_table(create_table_query = '''CREATE TABLE view_profiles
                       (id_profile serial PRIMARY KEY,
                       fk_id_user  integer  NOT NULL references users(id_user),
                       id_profile_vk  integer unique NOT NULL); ''')