def look(requests, head, direction='right'):
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
        for r in reversed(left):
            total_seek_time += abs(head - r)
            head = r
            sequence.append(head)
    else:
        for r in reversed(left):
            total_seek_time += abs(head - r)
            head = r
            sequence.append(head)
        for r in right:
            total_seek_time += abs(head - r)
            head = r
            sequence.append(head)

    return sequence, total_seek_time
