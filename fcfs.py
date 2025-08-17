def fcfs(requests, head):
    sequence = [head] + requests
    total_seek_time = sum(abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence)))
    return sequence, total_seek_time
