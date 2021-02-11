import threading
import pickle


class AuditThread(threading.Thread):

    def __init__(self, conn, audit_handler, counter):
        self.conn = conn
        self.audit_handler = audit_handler
        self.number = counter
        threading.Thread.__init__(self)

    def run(self):
        connected = True
        print(f'Auditing thread # {self.number} started.')
        while connected:
            data = self.conn.recv(4096)
            if data:
                event = self.decodeData(data)
                print(f'Auditing thread # {self.number} received {event}')
                self.logEvent(event)

    def decodeData(self, data):
        try:
            event = pickle.loads(data)
        except Exception as err:
            self.sendError(
                reason=f'Auditing thread # {self.number}: Failed to decode data. {err}'
            )
            return None
        return event

    def sendError(self, status=400, reason='', content=None):
        error = {
            'status': status,
            'reason': reason,
            'content': content
        }
        self.conn.sendall(pickle.dumps(error))

    def sendSuccess(self, status=200):
        success = {
            'status': status
        }
        self.conn.sendall(pickle.dumps(success))

    def isDumplog(self, event):
        if event.xmlName == 'userCommand' and event.command == 'DUMPLOG':
            self.audit_handler.dumplog(event.filename)

    def logEvent(self, event):
        if event:
            res = self.audit_handler.logEvent(event)
            if not res:
                self.sendError(
                    status=500,
                    reason=f'AuditService: Failed to log event \n{event}'
                )
            else:
                self.isDumplog(event)
                self.sendSuccess()
        else:
            self.sendError(
                status=500,
                reason=f'AuditService: Failed to log event \n{event}'
            )
