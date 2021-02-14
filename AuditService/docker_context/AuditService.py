from socket import socket, AF_INET, SOCK_STREAM, error as socketError
from AuditHandler import AuditHandler
from AuditThread import AuditThread
import pickle

AUDIT_SERVICE_IP, AUDIT_SERVICE_PORT = 'audit-1', 6500
SERVICE_NAME = 'auditService'

audit_socket = socket(AF_INET, SOCK_STREAM)
audit_handler = AuditHandler()


def sendSuccess(conn, status=200):
    success = {
        'status': status
    }
    conn.sendall(pickle.dumps(success))


def sendError(conn, status=400, reason='', content=None):
    error = {
        'status': status,
        'reason': reason,
        'content': content
    }
    conn.sendall(pickle.dumps(error))


def decodeData(data):
    try:
        event = pickle.loads(data)
    except Exception as err:
        sendError(
            conn,
            reason=f'AuditService: Failed to decode data. {err}'
        )
        return None
    return event


def isDumplog(event):
    if event.xmlName == 'userCommand' and event.command == 'DUMPLOG':
        audit_handler.dumplog(event.filename)


def logEvent(conn, event):
    if event:
        res = audit_handler.logEvent(event)
        if not res:
            sendError(
                conn,
                status=500,
                reason=f'AuditService: Failed to log event \n{event}'
            )
        else:
            isDumplog(event)
            sendSuccess(conn)
    else:
        sendError(
            conn,
            status=500,
            reason=f'AuditService: Failed to log event \n{event}'
        )


if __name__ == '__main__':
    audit_socket.bind((AUDIT_SERVICE_IP, AUDIT_SERVICE_PORT))
    audit_socket.listen(5)
    counter = 0
    threads = []
    while True:
        print(f'Listening on ({AUDIT_SERVICE_IP}, {AUDIT_SERVICE_PORT})')
        conn, address = audit_socket.accept()
        counter += 1
        print(f'Connection from {address}')

        try:
            thread = AuditThread(conn, audit_handler, counter)
            threads.append(thread)
            thread.start()
        except socketError:
            print(f'Audit service lost connection from {address}')
        # while True:

            # data = conn.recv(4096)
            # if not data:
            #     break
            #
            # event = decodeData(data)
            # print(event)
            # if event:
            #     logEvent(conn, event)
