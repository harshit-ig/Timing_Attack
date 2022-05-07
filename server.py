import random, time
password_database = {}
with open('database.txt') as database:
    for line in database:
        temp = line.split(':')
        password_database[temp[0].strip()]= temp[1].strip()
def check_password(user, guess):
    if user not in password_database.keys():
        return 'User Not Found!!'
    if guess is None:
        return False
    actual = password_database[user]
    # time.sleep(float(random.randint(0,100)/random.randint(10000,100000)))
    if len(guess) != len(actual):
        return False

    for i in range(len(actual)):
        if guess[i] != actual[i]:
            return False
    return True
