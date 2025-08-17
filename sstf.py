def sstf(requests, head):
    requests = requests[:]
    sequence = [head]
    total_seek_time = 0

    while requests:
        distances = [(abs(head - r), r) for r in requests]
        distances.sort()
        closest = distances[0][1]
        total_seek_time += abs(head - closest)
        head = closest
        sequence.append(head)
        requests.remove(closest)

    return sequence, total_seek_time
