import semantic_form
from random import randrange

credentials={
    'userid': 'aa',
    'password': 'aa',
    'confirmPassword': 'aa', # used for register
}
domain = 'http://mmmfest.fr:9000'
sfc = semantic_form.Client(domain, credentials=credentials)
sfc.register()

ids = []
#ids.append('3550829514-1613069278')
#ids.append('2158487616-9853182500')
ids.append('8972448636-1920551385')
ids.append('2944811907-3432472209')
ids.append('7564891712-5310575657')
ids.append('2097345638-3032702657')

for id in ids:
    print('{}/ldp/{}'.format(domain, id))
    sfc.drop(id)