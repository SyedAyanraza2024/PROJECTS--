def scan(requests, head, direction='right', disk_size=200):
    requests = sorted(requests)
    sequence = [head]
    total_seek_time = 0

    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == 'right':
        for r in right:
            total_seek_time += abs(head - r)
            head = r
            sequence.append(head)
        if left:
            total_seek_time += abs(head - (disk_size - 1))
            head = disk_size - 1
            sequence.append(head)
            for r in reversed(left):
                total_seek_time += abs(head - r)
                head = r
                sequence.append(head)
    else:
        for r in reversed(left):
            total_seek_time += abs(head - r)
            head = r
            sequence.append(head)
        if right:
            total_seek_time += abs(head - 0)
            head = 0
            sequence.append(head)
            for r in right:
                total_seek_time += abs(head - r)
                head = r
                sequence.append(head)

    return sequence, total_seek_time
