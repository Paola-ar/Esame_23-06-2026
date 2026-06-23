from database.DB_connect import DBConnect
from model.user import User

class Dao:
    def __init__(self):
        pass

    @staticmethod
    def read_all_users():
        print("Executing read from database using SQL query")

        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT * FROM Users """

        cursor.execute(query)

        for row in cursor:
            user = User(
                row["user_id"],
                row["votes_funny"],
                row["votes_useful"],
                row["votes_cool"],
                row["name"],
                row["average_stars"],
                row["review_count"]
            )

            results.append(user)

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def get_users_min_bus(n_min_bus,id_user_map):
        print("Executing read from database using SQL query")
        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ select distinct user_id
                    from reviews r 
                    group by r.user_id 
                    having count(distinct r.review_id ) >= %s """

        cursor.execute(query, (n_min_bus,))

        for row in cursor:
                results.append(row["user_id"])

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def get_user_bus():
        print("Executing read from database using SQL query")
        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ select u.user_id, b.business_id
                    from users u, reviews r, business b
                    where u.user_id = r.user_id and r.business_id = b.business_id 
                    group by u.user_id,b.business_id """

        cursor.execute(query,)

        for row in cursor:
            results.append((row["user_id"], row["business_id"]))

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def get_tot_bus_rew(user_id):
        print("Executing read from database using SQL query")
        results = {}
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ select distinct u.user_id, count(r.business_id ) as tot
                    from users u, reviews r 
                    where u.user_id = %s
                        and u.user_id = r.user_id
                    group by u.user_id """

        cursor.execute(query,(user_id,) )

        for row in cursor:
            results[row["user_id"]] = row["tot"]

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def get_connessioni(id_user_map, nodes):
        print("Executing read from database using SQL query")
        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ select distinct u1.user_id as p1, u2.user_id as p2
                    from users u1, users u2, reviews r1, reviews r2, business b1, business b2
                    where u1.user_id = r1.user_id and r1.business_id = b1.business_id 
                    and u2.user_id = r2.user_id and r2.business_id = b2.business_id 
                    and b1.business_id = b2.business_id and u1.user_id <> u2.user_id
                    group by u1.user_id, u2.user_id """

        cursor.execute(query, )

        for row in cursor:
            if row["p1"] in nodes and row["p2"] in nodes:
                results.append((row["p1"],row["p2"]))

        cursor.close()
        cnx.close()

        return results


