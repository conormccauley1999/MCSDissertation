import ast

with open('./ReviewFeatures_Votes_Optimal.txt', 'r') as f:
    res = ast.literal_eval(f.read())

samples = [
    'eng_any_any_100000', 'eng_any_long_100000', 'eng_any_short_100000',
    'any_any_any_100000', 'any_any_long_100000', 'any_any_short_100000',
]
for type in ['mse', 'r2']:
    mul = -1 if type == 'mse' else 1
    for sample in samples:
        la, _, le, _ = sample.split('_')
        cur_lang = {'eng':'English','any':'Multilingual'}[la]
        cur_len = {'any':'Any','long':'Long','short':'Short'}[le]
        def f(v, m):
            x = round(float(v) * m, 2)
            if x == abs(x): return abs(x)
            else: return x
        rbl = f(res[sample]['bl'][type], mul)
        rsg = f(res[sample]['sgd'][type], mul)
        rri = f(res[sample]['ridge'][type], mul)
        rls = f(res[sample]['lsvr'][type], mul)
        rbe = f(res[sample]['bert'][type], mul)
        print(
            '%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
                cur_lang, cur_len, rbl, rsg, rri, rls, rbe
            )
        )
