
class DbmHandler:

    def __init__(self, dbm_ip, dbm_port, loop):
        self.dbm_url = f'http://{dbm_ip}:{dbm_port}'
        # TODO setup client
        self.audit_events = {'system': []}  # Temporary till we have DBM setup

    def saveAuditEvent(self, event):
        # TODO change this logic to send post request to DBM instead
        user_id = event.get('user_id', '')
        if not user_id:
            self.audit_events['system'].append(event)
            return

        if user_id in self.audit_events:
            self.audit_events[user_id].append(event)
        else:
            self.audit_events[user_id] = [event]

    def fetchAuditEvents(self, user_id=''):
        # TODO change so this logic fetches from DBM
        events = []
        if user_id:
            events = self.audit_events[user_id]
        else:
            for key in self.audit_events.keys():
                events.extend(self.audit_events[key])

        return events

    def fetchAccountSummary(self, user_id):
        # TODO change so this fetches from DBM
        return {
            'user_id': user_id,
            'funds': 405.54,
            'stock_holdings': {'ABC': (12, 50), 'DEF': (42, 0)},  # (balance, reserved
            'active_buy_triggers': {'TT': (123.30, 34.21, -1)},  # (amount, price, trans_num)
            'active_sell_triggers': {'WW': (44.54, 12.30, -1)}  # (amount, price, trans_num)
        }, 200
