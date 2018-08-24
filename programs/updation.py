import csv
import os
import thread
import time
import threading
import geoip2.database
import socket
#import gexf
#mport networkx as nx
#import matplotlib.pyplot as plt
import sys
import MySQLdb

def update():
    db = MySQLdb.connect("localhost",user="root",db="category_info")
    cursor = db.cursor()
    sql="select * from category"    
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
        for row in rows:
            if not row[1].islower():
                update_id=0
                x=row[1].lower()
                sql1="select * from category where category_name='%s'"%(x)
                cnt=0
                try:
                
                    cursor.execute(sql1)
                    result=cursor.fetchone()
                    if result[0]>0:
                        update_id=result[0]
                        cnt=result[2]+row[2]
                        sql2="update category set count='%s' where category_name='%s'"%(cnt,x)
                        try:
                            cursor.execute(sql2)
                            sql3="update children set parent_id='%s' where parent_id='%s'"%(update_id,row[0])
                            try:
                                cursor.execute(sql3)
                                db.commit()
                                #db.commit()
                            except:
                                print "error"
                                db.rollback()
                            sql_d="delete from category where category_id='%s'"%(row[0])
                            try:
                                cursor.execute(sql_d)
                                #db.commit()
                            except:
                                print "error"
                                db.rollback()
                        except:
                            print "print error"
                            db.rollback()
                        
                    else:
                        sql_u="update category set category_name='%s' where category_name='%s'"%(x,row[1])
                        try:
                            cursor.execute(sql_u)
                            db.commit()
                        except:
                            print "print error"
                            db.rollback()
                        
                except:
                    print "error"
                    db.rollback()

    except:
        print "main error"
        db.rollback()
    db.close()
                    
update()                  
                    
                
                
            
            
            
        
    
