def clook(requests, head):
    requests = sorted(requests)
    sequence = [head]
    total_seek_time = 0

    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    for r in right:
        total_seek_time += abs(head - r)
        head = r
        sequence.append(head)

    if left:
        total_seek_time += abs(head - left[0])
        head = left[0]
        sequence.append(head)

        for r in left[1:]:
            total_seek_time += abs(head - r)
            head = r
            sequence.append(head)

    return sequence, total_seek_time
