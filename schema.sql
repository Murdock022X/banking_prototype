DROP TABLE IF EXISTS Accounts;

CREATE TABLE Accounts (acc_no INTEGER PRIMARY KEY AUTOINCREMENT,
        bal REAL NOT NULL, min_bal REAL NOT NULL, interest_rate REAL NOT NULL,
        acc_type TEXT NOT NULL, username TEXT NOT NULL);

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (username TEXT PRIMARY KEY, password TEXT NOT NULL,
        first_name TEXT NOT NULL, last_name TEXT NOT NULL);

DROP TABLE IF EXISTS Transactions;

CREATE TABLE Transactions (transaction_no INTEGER PRIMARY KEY AUTOINCREMENT,
        fr_acc_no INTEGER NOT NULL, to_acc_no INTEGER NOT NULL,
        date_time TEXT NOT NULL);

DROP TABLE IF EXISTS Bank_Settings;

CREATE TABLE Bank_Settings (savings_rate REAL NOT NULL,
        savings_min REAL NOT NULL, checkings_rate REAL NOT NULL,
        checkings_min REAL NOT NULL);