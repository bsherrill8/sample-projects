#this file contains all of the functions for accessing or modifying the database
import sqlite3, customer, furniture, order

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    #function executes slightly different SQL commands based on what is searched for    
    def fetch(self, table, id, alt_lookup):
        if table == "Customers":
            if id != "":
                self.cur.execute("SELECT * FROM Customers where cust_id = ?", (id,))
            else:
                self.cur.execute("SELECT * FROM Customers where cust_phone = ?", (alt_lookup,))
        if table == "Furniture":
            self.cur.execute("SELECT * FROM Furniture where furn_id = ?", (id,))
        if table == "Orders":
            self.cur.execute("SELECT * FROM Orders where ord_id = ?", (id,))
        rows = self.cur.fetchall()
        return rows        
    
    #similar to above, function receives an object and then saves it into the appropriate db table
    def insert(self, data):
        if isinstance(data, customer.Customer):
            self.cur.execute("INSERT INTO Customers VALUES (NULL, ?, ?, ?, ?)", (data.name, data.phone, data.addr, data.dist))
        if isinstance(data, furniture.Furniture):
            self.cur.execute("INSERT INTO Furniture VALUES (NULL, ?, ?, ?)", (data.desc, data.price, data.stock))
        if isinstance(data, order.Order):
            for item in data.furn_set:
                self.cur.execute("INSERT INTO Orders VALUES (?, ?, ?, ?)",(data.id, item.id, data.customer.id, data.furn_set[item]))
        self.conn.commit()

    #as above, but for removing entries from tables
    def remove(self, data):
        if isinstance(data, customer.Customer):
            self.cur.execute("DELETE FROM Customers WHERE cust_id = ?", (data.id))
        if isinstance(data, furniture.Furniture):
            self.cur.execute("DELETE FROM Furniture WHERE furn_id = ?", (data.id))

        self.conn.commit()

    #as above but for updating db information
    def update(self, data):
        if isinstance(data, customer.Customer):
            self.cur.execute("UPDATE Customers SET cust_name = ?, cust_phone = ?, cust_addr = ?, cust_dist = ? WHERE cust_id = ?",
                (data.name, data.phone, data.addr, data.dist, data.id))                
        if isinstance(data, furniture.Furniture):
            self.cur.execute("UPDATE Furniture SET furn_desc = ?, furn_price = ?, furn_stock = ? WHERE furn_id = ?",
                (data.desc, data.price, data.stock, data.id))                
        self.conn.commit()
    
    #Since the Orders table has two PKs, it could not autoincrement
    #This function gets the next available ID# to help in adding an order to the db
    def next_id(self):
        self.cur.execute("SELECT MAX(ord_id) from ORDERS")
        result = self.cur.fetchone()
        return result[0] + 1
        