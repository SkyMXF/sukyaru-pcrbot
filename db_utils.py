import os
import sqlite3

import config

class DatabaseUtil():

    def __init__(self, db_name):
        self.db_path = os.path.join(config.DATABASE_PATH, "%s.db"%(db_name))
        self.conn = sqlite3.connect(self.db_path)

    def db_init(self):
        cursor = self.conn.cursor()

        # user auth
        sql = "CREATE TABLE user_auth (\
            authID INT PRIMARY KEY NOT NULL,\
            authName VARCHAR(32) NOT NULL\
            )"
        cursor.execute(sql)

        # user info
        sql = "CREATE TABLE member (\
            uID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,\
            mName VARCHAR(30) NOT NULL,\
            mQQ VARCHAR(15),\
            password VARCHAR(64) NOT NULL,\
            userAuth INT NOT NULL,\
            activeUser TINYINT(1) NOT NULL,\
            regTime DATETIME NOT NULL,\
            ADD CONSTRAINT fk_auth FOREIGN KEY (userAuth) REFERENCES user_auth(authName)\
            )"
        cursor.execute(sql)

        # battle history
        sql = "CREATE TABLE battle (\
            battleID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,\
            battleName VARCHAR(40) NOT NULL,\
            presentBattle TINYINT(1) NOT NULL\
            )"
        cursor.execute(sql)

        # battle date
        sql = "CREATE TABLE battle_date (\
            battleID INT,\
            battleDate DATE PRIMARY KEY NOT NULL,\
            ADD CONSTRAINT fk_battle FOREIGN KEY (battleID) REFERENCES battle(battleID)\
            )"
        cursor.execute(sql)

        # SL table
        sql = "CREATE TABLE sl (\
            uID INT,\
            battleDate DATE,\
            ADD CONSTRAINT fk_user FOREIGN KEY (uID) REFERENCES member(uID),\
            ADD CONSTRAINT fk_date FOREIGN KEY (battleDate) REFERENCES battle_date(battleDate)\
            )"
        cursor.execute(sql)

        # boss info
        sql = "CREATE TABLE boss_info (\
            infoID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,\
            battleID INT,\
            stage INT NOT NULL,\
            number INT NOT NULL,\
            name INT NOT NULL,\
            totalHealth INT NOT NULL,\
            scoreFac DOUBLE NOT NULL,\
            ADD CONSTRAINT fk_battle FOREIGN KEY (battleID) REFERENCES battle(battleID)\
            )"
        cursor.execute(sql)

        # boss status
        sql = "CREATE TABLE boss_status (\
            statusID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,\
            infoID INT NOT NULL,\
            round INT NOT NULL,\
            health INT NOT NULL\
            )"
        cursor.execute(sql)

        # battle record
        sql = "CREATE TABLE battle_record (\
            recordDatetime DATETIME,\
            recordDate DATE,\
            uID INT,\
            bossStatusID INT,\
            damage INT,\
            finalKill TINYINT(1),\
            compRecord TINYINT(1)\
            )"
        cursor.execute(sql)

    def __del__(self):
        self.conn.close()