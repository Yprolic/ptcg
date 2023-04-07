
x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
y = 'vkXupMNUJjiAGbwYnoclCFfQsKxyrETDWdVegPatzmLHhZIOqRBS'

encoder = str.maketrans(x, y)
decoder = str.maketrans(y, x)


def encode(s):
    return s.translate(encoder)
