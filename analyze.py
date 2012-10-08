import os
import sys
import time
import cPickle as pickle
import frame

def main():
    fname = sys.argv[1]
    args = sys.argv[1:]

    id_filter = None
    skip_same = True
    while args:
        a = args.pop(0)
        if a == '-id':
            id_filter = int(args.pop(0), 16)
        if a == '-ss':
            skip_same = False

    frames = pickle.load(open(fname, 'rb'))
    for frame in frames:
        frame.data = tuple(frame.data)
        # frame.data = tuple(map(hex,frame.data))

    last_id = {}
    skipped = 0
    for frame in frames:
        if id_filter is not None and id_filter != frame.id:
            continue

        last = last_id.get(frame.id)
        last_id[frame.id] = frame
        if skip_same and last and (last.data == frame.data):
            skipped += 1
            continue

        if skipped:
            print '(skipped %d duplicate frames)' % skipped

        skipped = 0
        print frame

    if skipped:
        print '(skipped %d duplicate frames)' % skipped

    for i in sorted(last_id.keys()):
        print '%03X' % i

    print len(last_id)

if __name__ == '__main__':
    main()
