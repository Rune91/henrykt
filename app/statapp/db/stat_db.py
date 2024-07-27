import mysql.connector


class myDB:
    def __init__(self):
        self.configuration = {
            "host": "db",
            "port": 3306,
            "user": "root",
            "password": "password",
            "database": "stat"
        }
    
    def __enter__(self):
        try:
            # Establish a database connection and create a cursor
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor(dictionary=True)
            return self
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        try:
            # Commit changes if no exception occurred, otherwise rollback
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            # Close the cursor and connection
            self.cursor.close()
            self.conn.close()

    def query(self, sql_query, *args, **kwargs) -> None:
        # Execute a query
        if len(kwargs) > 0:
            self.cursor.execute(sql_query, kwargs)
        else:
            self.cursor.execute(sql_query, args)
    
    def get_previous_insert_id(self):
        sql_query = "SELECT LAST_INSERT_ID() AS id;"
        self.query(sql_query)
        res = self.cursor.fetchone()['id']
        print(f"Result is {res}")
        return res


    # User
    def get_user_by_id(self, user_id):
        sql_query = """
            SELECT * FROM User
            WHERE UserId = %s
            """
        self.query(sql_query, user_id)
        return self.cursor.fetchone()
    
    def get_user_by_login(self, name):
        sql_query = """
            SELECT * FROM User
            WHERE UserLogin = %s
            """
        self.query(sql_query, name)
        return self.cursor.fetchone()

    # Events
    def get_event_by_id(self, event_id):
        sql_query = """
            SELECT E.EventId, E.EventName, COUNT(EV.EventId)
            FROM Event AS E
            LEFT JOIN Evaluation AS EV ON E.EventId = EV.EventId
            WHERE E.EventId = %s
            GROUP BY E.EventId, E.EventName
            """
        self.query(sql_query, event_id)
        return self.cursor.fetchone()

    def get_all_events_by_user(self, user_id):
        sql_query = """
            SELECT E.EventId, E.EventName, COUNT(EV.EventId)
            FROM Event AS E
            LEFT JOIN Evaluation AS EV ON E.EventId = EV.EventId
            WHERE E.UserId = %s
            GROUP BY E.EventId, E.EventName
            ORDER BY E.CreateTime
            """
        self.query(sql_query, user_id)
        return self.cursor.fetchall()

    def insert_event(self, user_id, event_name):
        sql_query = """
            INSERT INTO Event (UserId, EventName)
            VALUES
                (%s, %s);
            """
        self.query(sql_query, user_id, event_name)
        return True

    def change_name_for_event(self, event_id, new_event_name):
        sql_query = """
            UPDATE Event
            SET EventName = %s
            WHERE EventId = %s;
            """
        self.query(sql_query, new_event_name, event_id)
        return True

    # Operators
    def get_operator_by_id(self, operator_id):
        sql_query = """
            SELECT O.OperatorId, O.OperatorName, COUNT(EV.EventId)
            FROM Operator AS O
            LEFT JOIN Evaluation AS EV ON O.OperatorId = EV.OperatorId
            WHERE O.OperatorId = %s
            GROUP BY O.OperatorId, O.OperatorName
            """
        self.query(sql_query, operator_id)
        return self.cursor.fetchone()

    def get_all_operators_by_user(self, user_id):
        sql_query = """
            SELECT O.OperatorId, O.OperatorName, COUNT(EV.EventId)
            FROM Operator AS O
            LEFT JOIN Evaluation AS EV ON O.OperatorId = EV.OperatorId
            WHERE O.UserId = %s
            GROUP BY O.OperatorId, O.OperatorName
            """
        self.query(sql_query, user_id)
        return self.cursor.fetchall()
    
    def insert_operator(self, user_id, operator_name):
        sql_query = """
            INSERT INTO Operator (UserId, OperatorName)
            VALUES
                (%s, %s);
            """
        self.query(sql_query, user_id, operator_name)
        return True

    def change_name_for_operator(self, operator_id, new_operator_name):
        sql_query = """
            UPDATE Operator
            SET OperatorName = %s
            WHERE OperatorId = %s;
            """
        self.query(sql_query, new_operator_name, operator_id)
        return True

    # Evaluation
    def insert_evaluation(self, event_id, operator_id, value):
        sql_query = """
            INSERT INTO Evaluation (EventId, OperatorId, EvalValue)
            VALUES
                (%s, %s, %s);
            """
        self.query(sql_query, event_id, operator_id, value)
        return True

    def get_all_evaluations_by_userid(self, user_id):
        sql_query = """
            SELECT Event.EventName, O.OperatorName, Eval.EvalValue, Eval.EvalTime
            FROM Evaluation as Eval
            INNER JOIN Event ON Event.EventId = Eval.EventId
            INNER JOIN Operator as O on O.OperatorId = Eval.OperatorId
            WHERE Event.UserId = %s
            ORDER BY Event.EventId, Eval.EvalTime DESC;
            """
        self.query(sql_query, user_id)
        return self.cursor.fetchall()
    
    def get_all_evaluations_by_eventid(self, event_id):
        sql_query = """
            SELECT Event.EventName, O.OperatorName, Eval.EvalValue, Eval.EvalTime
            FROM Evaluation as Eval
            INNER JOIN Event ON Event.EventId = Eval.EventId
            INNER JOIN Operator as O on O.OperatorId = Eval.OperatorId
            WHERE Event.EventId = %s
            ORDER BY Eval.EvalTime DESC;
            """
        self.query(sql_query, event_id)
        return self.cursor.fetchall()
    
    def get_evaluation_sets_by_userid(self, user_id):
        sql_query = """
            SELECT
                Event.EventId,
                Event.EventName,
                SUM(CASE WHEN Eval.EvalValue = 1 THEN 1 ELSE 0 END) AS Count1s,
                SUM(CASE WHEN Eval.EvalValue = 2 THEN 1 ELSE 0 END) AS Count2s,
                SUM(CASE WHEN Eval.EvalValue = 3 THEN 1 ELSE 0 END) AS Count3s,
                SUM(CASE WHEN Eval.EvalValue = 4 THEN 1 ELSE 0 END) AS Count4s,
                SUM(CASE WHEN Eval.EvalValue = 5 THEN 1 ELSE 0 END) AS Count5s
            FROM Event
            LEFT JOIN Evaluation AS Eval ON Event.EventId = Eval.EventId
            WHERE Event.UserId = %s
            GROUP BY Event.EventId, Event.EventName
            ORDER BY Event.EventId;
            """
        self.query(sql_query, user_id)
        return self.cursor.fetchall()
