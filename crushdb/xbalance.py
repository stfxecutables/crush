#!/usr/bin/env python3

import os
import logging
import psycopg2 as pg

from decimal import Decimal
from functools import wraps
from psycopg2.pool import ThreadedConnectionPool

from contextlib import contextmanager

LOG_FORMAT = "%(asctime)s %(message)s"
MAX_DEPOSIT_LIMIT = 1000.00

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger('balance')
#postgresql://user@localhost:5432/dbname

def connect(env="CRUSH_DATABASE_URL", connections=2):
    """
    Connect to the database using an environment variable.
    """
    url = os.getenv(env)
    if not url:
        raise ValueError("no database url specified")

    minconns = connections
    maxconns = connections * 2
    return ThreadedConnectionPool(minconns, maxconns, url)

pool = connect()

def createdb(conn, schema="schema.sql"):
    """
    Execute DROP and CREATE TABLE statements in the specified SQL file.
    """
    with open(schema, 'r') as f:
        sql = f.read()

    try:
        with conn.cursor() as curs:
            curs.execute(sql)
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


@contextmanager
def transaction(name="transaction", **kwargs):
    # Get the session parameters from the kwargs
    options = {
        "isolation_level": kwargs.get("isolation_level", None),
        "readonly": kwargs.get("readonly", None),
        "deferrable": kwargs.get("deferrable", None),
    }

    try:
        conn = pool.getconn()
        conn.set_session(**options)
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        log.error("{} error: {}".format(name, e))
    finally:
        conn.reset()
        pool.putconn(conn)


def transact(func):
    """
    Creates a connection per-transaction, committing when complete or
    rolling back if there is an exception. It also ensures that the conn is
    closed when we're done.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        print("there")
        with transaction(name=func.__name__) as conn:
            ret = func(conn, *args, **kwargs)
        print(f"inner: {ret}")
        return ret
    return inner


def authenticate(conn, user, pin, account=None):
    """
    Returns an account id if the name is found and if the pin matches.
    """
    with conn.cursor() as curs:
        sql = "SELECT 1 AS authd FROM users WHERE username=%s AND pin=%s"
        curs.execute(sql, (user, pin))
        if curs.fetchone() is None:
            raise ValueError("could not validate user via PIN")
        return True

    if account:
        # Verify account ownership if account is provided
        verify_account(conn, user, account)


def verify_account(conn, user, account):
    """
    Verify that the account is held by the user.
    """
    with conn.cursor() as curs:
        sql = (
            "SELECT 1 AS verified FROM accounts a "
            "JOIN users u on u.id = a.owner_id "
            "WHERE u.username=%s AND a.id=%s"
        )
        curs.execute(sql, (user, account))

        if curs.fetchone() is None:
            raise ValueError("account belonging to user not found")
        return True


def ledger(conn, account, record, amount):
    """
    Add a ledger record with the amount being credited or debited.
    """
    # Perform the insert
    with conn.cursor() as curs:
        sql = "INSERT INTO ledger (account_id, type, amount) VALUES (%s, %s, %s)"
        curs.execute(sql, (account, record, amount))

    # If we are crediting the account, perform daily deposit verification
    if record == "credit":
        check_daily_deposit(conn, account)


def check_daily_deposit(conn, account):
    """
    Raise an exception if the deposit limit has been exceeded.
    """
    with conn.cursor() as curs:
        sql = (
            "SELECT amount FROM ledger "
            "WHERE date=now()::date AND type='credit' AND account_id=%s"
        )
        curs.execute(sql, (account,))
        total = sum(row[0] for row in curs.fetchall())
        if total > MAX_DEPOSIT_LIMIT:
            raise Exception("daily deposit limit has been exceeded!")


def update_balance(conn, account, amount):
    """
    Add the amount (or subtract if negative) to the account balance.
    """
    amount = Decimal(amount)
    with conn.cursor() as curs:
        current = balance(conn, account)
        sql = "UPDATE accounts SET balance=%s WHERE id=%s"
        curs.execute(sql, (current+amount, account))


def balance(conn, account):
    with conn.cursor() as curs:
        curs.execute("SELECT balance FROM accounts WHERE id=%s", (account,))
        return curs.fetchone()[0]


@transact
def withdraw(conn, user, pin, account, amount):
    # Step 1: authenticate the user via pin and verify account ownership
    authenticate(conn, user, pin, account)

    # Step 2: add the ledger record with the debit
    ledger(conn, account, "debit", amount)

    # Step 3: update the account value by subtracting the amount
    update_balance(conn, account, amount * -1)

    # Fetch the current balance in the account and log it
    record = "withdraw ${:0.2f} from account {} | current balance: ${:0.2f}"
    log.info(record.format(amount, account, balance(conn, account)))


@transact
def deposit(conn, user, pin, account, amount):
    # Step 1: authenticate the user via pin and verify account ownership
    authenticate(conn, user, pin, account)

    # Step 2: add the ledger record with the credit
    ledger(conn, account, "credit", amount)

    # Step 3: update the account value by adding the amount
    update_balance(conn, account, amount)

    # Fetch the current balance in the account and log it
    record = "withdraw ${:0.2f} from account {} | current balance: ${:0.2f}"
    log.info(record.format(amount, account, balance(conn, account)))


def sequential():
    # Successful deposit
    deposit('alice', 1234, 1, 785.0)

    # Unsuccessful authenticate
    withdraw('bob', 8881, 2, 180.00)

    # Successful withdrawal
    withdraw('alice', 1234, 1, 230.0)

    # Unsuccessful deposit
    deposit('alice', 1234, 1, 489.0)

    # Successful deposit
    deposit('bob', 9999, 2, 220.23)


if __name__ == '__main__':
    import time
    import random
    import threading

    conn = pool.getconn()
    createdb(conn)
    pool.putconn(conn)

    def op1():
        time.sleep(random.random())
        withdraw('alice', 1234, 1, 300.0)

    def op2():
        time.sleep(random.random())
        deposit('alice', 1234, 1, 75.0)
        withdraw('alice', 1234, 1, 25.0)


    threads = [
        threading.Thread(target=op1),
        threading.Thread(target=op2),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
