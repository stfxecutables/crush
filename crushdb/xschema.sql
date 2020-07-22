
--
-- Reset the database by dropping existing tables, then create the tables
-- required by the balance.py Python script.
--

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    pin SMALLINT NOT NULL
);


DROP TYPE IF EXISTS account_type CASCADE;
CREATE TYPE account_type AS ENUM ('checking', 'savings');

DROP TABLE IF EXISTS accounts CASCADE;
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    type account_type,
    owner_id INTEGER NOT NULL,
    balance NUMERIC DEFAULT 0.0,
    CONSTRAINT positive_balance CHECK (balance >= 0),
    FOREIGN KEY (owner_id) REFERENCES users (id)
);

DROP TYPE IF EXISTS ledger_type CASCADE;
CREATE TYPE ledger_type AS ENUM ('credit', 'debit');

DROP TABLE IF EXISTS ledger;
CREATE TABLE ledger (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    type ledger_type NOT NULL,
    amount NUMERIC NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);

--
-- Seed the database with some owner and account information
--

INSERT INTO users (id, username, pin) VALUES
    (1, 'alice', 1234),
    (2, 'bob', 9999);

INSERT INTO accounts (id, type, owner_id, balance) VALUES
    (1, 'checking', 1, 250.0),
    (2, 'savings', 1, 5.00),
    (3, 'checking', 2, 100.0),
    (4, 'savings', 2, 2342.13);
