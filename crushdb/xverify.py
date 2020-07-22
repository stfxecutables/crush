from balance import connect, createdb

def verify_transaction(conn, context=False):
    if context:
        return verify_transaction_with_context(conn)
    return verify_transaction_no_context(conn)


def verify_transaction_with_context(conn):
    with conn.cursor() as curs:
        # Execute command that raises a constraint
        try:
            curs.execute("UPDATE accounts SET balance=%s", (-130.935,))
        except Exception as e:
            print(e) # Constraint exception

    with conn.cursor() as curs:
        try:
            curs.execute("SELECT id, type FROM accounts WHERE owner_id=%s", (1,))
        except pg.InternalError as e:
            print(e)


def verify_transaction_no_context(conn):
    curs = conn.cursor()

    try:
        # Execute a command that will raise a constraint
        curs.execute("UPDATE accounts SET balance=%s", (-130.935,))
    except Exception as e:
        print(e) # Constraint exception

    # Execute another command, but because of the previous exception:
    curs = conn.cursor()
    try:
        curs.execute("SELECT id, type FROM accounts WHERE owner_id=%s", (1,))
    except pg.InternalError as e:
        print(e)


if __name__ == '__main__':
    conn = connect()
    createdb(conn)

    # Verify transactions
    verify_transaction(conn, True)
