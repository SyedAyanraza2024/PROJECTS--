def cscan(requests, head, disk_size=200):
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
        total_seek_time += abs(head - (disk_size - 1))
        head = 0
        sequence.append(disk_size - 1)
        sequence.append(head)

        for r in left:
            total_seek_time += abs(head - r)
            head = r
            sequence.append(head)

    return sequence, total_seek_time
