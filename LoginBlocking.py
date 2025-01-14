import sys

class LoginBlocker:
    def __init__(self, failed_attempts_limit, time_interval, initial_block_duration, max_block_duration) -> None:
        self.failed_attempts_limit = failed_attempts_limit
        self.time_interval = time_interval
        self.initial_block_duration = initial_block_duration
        self.max_block_duration = max_block_duration

        self.current_block_duration = initial_block_duration
        self.failed_attempts = []

    def record_attempt(self, attempt_time: int) -> None:
        if current_time - attempt_time <= 2 * self.max_block_duration:
            self.failed_attempts.append(attempt_time)

    def organize_attempts(self) -> None:
        self.failed_attempts.sort()

    def calculate_block_duration(self) -> (bool, int):
        previously_blocked = False
        last_failure_time = 0
        index = 0

        while index <= len(self.failed_attempts) - self.failed_attempts_limit:
            if (self.failed_attempts[index + self.failed_attempts_limit - 1] - self.failed_attempts[index] >= self.time_interval):
                index += 1
                continue

            if previously_blocked:
                self.current_block_duration = min(self.current_block_duration * 2, self.max_block_duration)

            index += self.failed_attempts_limit
            last_failure_time = self.failed_attempts[index - 1]
            previously_blocked = True

        can_access = last_failure_time + self.current_block_duration < current_time or not previously_blocked

        return can_access, last_failure_time


def main():
    parameters = input()
    if not parameters:
        return

    global current_time
    failed_attempts_limit, time_interval, start_block_duration, max_block_duration, current_time = map(int, parameters.split())

    blocker = LoginBlocker(failed_attempts_limit, time_interval, start_block_duration, max_block_duration)

    for line in sys.stdin:
        if not line.strip():
            continue
        blocker.record_attempt(int(line.strip()))

    blocker.organize_attempts()

    can_access, last_failure_time = blocker.calculate_block_duration()
    print(last_failure_time + blocker.current_block_duration if not can_access else "ok")


if __name__ == "__main__":
    main()


# сложность по времени:
# нам надо пройтись по всем неудачным попыткам ввода что в худшем случае займеть O(n)
# соритровка тогда будет O(nlogn)
# итоговая сложность по времени составит O(nlogn)

# сложность по памяти
# мы используем список для неудачных попыток
# в худшем случае если все попытки закончатся неудачей, то сложность по памяти будет O(n)
