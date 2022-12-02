from psycopg2 import connect, Error

user = "postgres"
password = "6868"
host = "localhost"
port = "5432"
database = "article_db"


def insert_to_stage(records):
    global conn
    try:
        conn = connect(host=host, user=user, password=password, database=database, port=port)
        cursor = conn.cursor()
        conn.autocommit = True
        sql = """ INSERT INTO article_app_stage (name) VALUES (%s) """

        cursor.executemany(sql, records)
        print(cursor.rowcount, "Record inserted successfully into stage table")

    except (Exception, Error) as error:
        print("Failed inserting record into stage table {}".format(error))

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def insert_to_article_status(records):
    try:
        conn = connect(host=host, user=user, password=password, database=database, port=port)
        cursor = conn.cursor()
        conn.autocommit = True
        sql = """ INSERT INTO article_app_articlestatus (name, stage_id) VALUES (%s, %s) """

        cursor.executemany(sql, records)
        print(cursor.rowcount, "Record inserted successfully into articlestatus table")

    except (Exception, Error) as error:
        print("Failed inserting record into articlestatus table {}".format(error))

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def insert_to_role(records):
    try:
        conn = connect(host=host, user=user, password=password, database=database, port=port)
        cursor = conn.cursor()
        conn.autocommit = True
        sql = """ INSERT INTO user_app_role (name) VALUES (%s) """

        cursor.executemany(sql, records)
        print(cursor.rowcount, "Record inserted successfully into role table")

    except (Exception, Error) as error:
        print("Failed inserting record into role table {}".format(error))

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def insert_to_auth_group(records):
    try:
        conn = connect(host=host, user=user, password=password, database=database, port=port)
        cursor = conn.cursor()
        conn.autocommit = True
        sql = """ INSERT INTO auth_group (name) VALUES (%s) """

        cursor.executemany(sql, records)
        print(cursor.rowcount, "Record inserted successfully into group table")

    except (Exception, Error) as error:
        print("Failed inserting record into group table {}".format(error))

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def insert_to_notificationstatus(records):
    try:
        conn = connect(host=host, user=user, password=password, database=database, port=port)
        cursor = conn.cursor()
        conn.autocommit = True
        sql = """ INSERT INTO article_app_notificationstatus (name) VALUES (%s) """

        cursor.executemany(sql, records)
        print(cursor.rowcount, "Record inserted successfully into article_app_notificationstatus table")

    except (Exception, Error) as error:
        print("Failed inserting record into article_app_notificationstatus table {}".format(error))

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def insert_to_reviewstatus(records):
    try:
        conn = connect(host=host, user=user, password=password, database=database, port=port)
        cursor = conn.cursor()
        conn.autocommit = True
        sql = """ INSERT INTO user_app_statusreview (name) VALUES (%s) """

        cursor.executemany(sql, records)
        print(cursor.rowcount, "Record inserted successfully into user_app_statusreview table")

    except (Exception, Error) as error:
        print("Failed inserting record into user_app_statusreview table {}".format(error))

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    stages = [
        ('submission',),
        ('review',),
        ('publication',)
    ]
    article_status = [
        ('submit', 1),
        ('accept', 3),
        ('declined', 1),
        ('submit', 2),
        ('submit', 3),
        ('incomplete', 1),
        ('resubmit', 1),
        ('resubmit', 2),
    ]
    roles = [
        ('Admin',),
        ('Editor',),
        ('Reviewer',),
        ('Author',),
    ]
    groups = [
        ('Admin',),
        ('Editor',),
        ('Reviewer',),
        ('Author',),
    ]

    notif_status = [
        ('Unread',),
        ('Reading',),
        ('Read',),
    ]

    review_status = [
        ('Came',),
        ('Is seeing',),
        ('Confirmed',),
        ('Denied',),
        ('Resubmit',),
    ]

    # insert_to_stage(stages)
    # insert_to_article_status(article_status)
    # insert_to_role(roles)
    # insert_to_auth_group(groups)
    # insert_to_notificationstatus(notif_status)
    # insert_to_reviewstatus(review_status)
