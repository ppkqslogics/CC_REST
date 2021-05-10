import string
import random

id_size = 12
tag_id_size = 8
otp_size = 6
post_id_size = 20
# random chardigit (eg.a2j4kk7)


def random_generator(size=id_size):
    '''
    Generate the random id for cc_id
    Input : digits + string
    Output : random id
    Return : random_id
    '''
    random_char = string.digits + string.ascii_letters
    random_id = ''.join(random.choice(random_char) for index in range(size))
    # ''.join(random.choice(random_char) for index in range(size))
    return random_id


# random char + random digits (eg.cDeA1234)
""" def random_generator(size = id_size):
    random_digit = string.digits
    random_id_digit = ''.join(random.choice(random_digit) for index in range(size/2))
    random_char = string.ascii_letters
    random_id_char = ''.join(random.choice(random_char) for index in range(size/2))
    random_id = random_id_char + random_id_digit
    return random_id """


def tag_id_generator(size=tag_id_size):
    random_digit = string.digits
    random_tag_id = ''.join(random.choice(random_digit)
                            for index in range(size))
    return random_tag_id


def otp_generator(size=otp_size):
    random_digit = string.digits
    random_otp = ''.join(random.choice(random_digit) for index in range(size))
    return random_otp


def post_id_generator(size=post_id_size):
    random_char = string.digits + string.ascii_letters
    random_id = ''.join(random.choice(random_char) for index in range(size))
    return random_id
