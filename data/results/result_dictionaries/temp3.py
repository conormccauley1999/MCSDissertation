import ast

with open('./PredictiveUsers_Optimal.txt', 'r') as f:
    res = ast.literal_eval(f.read())

samples = [
    'eng_160k_6', 'any_160k_6',
    'eng_160k_3', 'any_160k_3',
]
for sample in samples:
    la, _, cls = sample.split('_')
    cur_lang = {'eng':'English','any':'Multilingual'}[la]
    def f(v): return round(float(v), 3)
    bl = f(res[sample]['bl'])
    mnb = f(res[sample]['mnb'])
    cnb = f(res[sample]['cnb'])
    sgd = f(res[sample]['sgd'])
    lsvc = f(res[sample]['lsvc'])
    bert = f(res[sample]['bert'])
    print(
        '%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
            cur_lang, cls, bl, mnb, cnb, sgd, lsvc, bert
        )
    )
