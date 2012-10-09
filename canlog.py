from frame import Frame
length = Frame.format_len

class CANLog(object):
    '''
    Append-only log format for CAN frames
    '''
    def __init__(self, logfile):
        self.file = open(logfile, 'a+b')
        self.file.seek(0, 2)
        self.len = self.file.tell() / length
        self.buffer = []

    def append(self, frame):
        self.buffer.append(frame)
        if len(self.buffer) > 10240:
            self.flush()

    def __getitem__(self, i):
        if i < self.len:
            self.file.seek(i * length, 0)
            return Frame(self.file.read(length))
            self.file.seek(0, 2)
        return self.buffer[i - self.len]

    def __len__(self):
        return self.len + len(self.buffer)

    def close(self):
        self.flush()
        self.file.close()

    def flush(self):
        l = len(self.buffer)
        self.file.seek(0, 2)
        for i in xrange(l):
            self.file.write(self.buffer[i].tostring())
            self.len += 1
        self.buffer[:l] = []
        # self.file.flush()

    def __del__(self):
        self.close()