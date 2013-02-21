import os
import pickle
import sqlite3

import time_series

class SQLiteTimeSeries(time_series.TimeSeriesInterface):
    name_pattern = '.*'

    def __init__(self):
        super(SQLiteTimeSeries, self).__init__()
        self.conn = None

    def open(self, filename):
        exists = os.path.isfile(filename) and os.path.getsize(filename) != 0
        self.conn = sqlite3.connect(filename)
        self.curs = self.conn.cursor()
        if not exists:
            self.create()
            self.size = 0
        else:
            self.curs.execute('''SELECT count(*) FROM data''')
            self.size = self.curs.fetchone()[0]

    def __len__(self):
        return self.size

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create(self):
        self.curs.executescript('''CREATE TABLE data (
                id INTEGER PRIMARY KEY,
                ts REAL,
                data TEXT
            );
            CREATE INDEX id_idx ON data (id);
            CREATE INDEX timestamp_idx ON data (ts);
        ''')


    def append(self, ts, data):
        bytes = pickle.dumps(data)
        self.curs.execute('''INSERT INTO data (id, ts, data)
            VALUES (?, ?, ?)''',
            (self.size, ts, bytes))
        self.size += 1

    def get(self, i):
        self.curs.execute('''SELECT id, ts, data FROM data
            WHERE (id = ?)''', (i,))
        i, ts, bytes = self.curs.fetchone()
        data = pickle.loads(bytes)
        return ts, data

    def get_range(self, start, end=1e10):
        self.curs.execute('''SELECT max(id) FROM data WHERE ts <= ?''', (start,))
        r = self.curs.fetchone()
        s = r[0] or 0
        self.curs.execute('''SELECT id, ts, data FROM data
            WHERE id >= ? AND ts < ?''', (s, end))

        result = []
        for i, ts, bytes in self.curs.fetchall():
            data = pickle.loads(bytes)
            result.append((ts,  data))

        return result


def test():
    time_series.test(SQLiteTimeSeries, iter(xrange(50, 100)))


if __name__ == '__main__':
    test()

