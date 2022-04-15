import re

with open('./PredictiveUsers_Reports.txt', 'r') as f:
    lines = f.readlines()

i, N = 0, len(lines)
while i < N:
    if lines[i].startswith('==='):
        la, _, cl = lines[i][4:-4].split('_')
        cur_lang = {'eng':'English','any':'Multilingual'}[la]
        def f(i, j):
            return re.sub('\s\s+', ' ', lines[i]).split()[j]
        if cl[0] == '6': k, l, m = 10, 23, 36
        else: k, l, m = 7, 17, 27
        bla, blp, blr, blf = f(i + k, 1), f(i + k + 1, 2), f(i + k + 1, 3), f(i + k + 1, 4)
        blp2, blr2, blf2 = f(i + k + 2, 2), f(i + k + 2, 3), f(i + k + 2, 4)
        cma, cmp, cmr, cmf = f(i + l, 1), f(i + l + 1, 2), f(i + l + 1, 3), f(i + l + 1, 4)
        cmp2, cmr2, cmf2 = f(i + l + 2, 2), f(i + l + 2, 3), f(i + l + 2, 4)
        bea, bep, ber, bef = f(i + m, 1), f(i + m + 1, 2), f(i + m + 1, 3), f(i + m + 1, 4)
        bep2, ber2, bef2 = f(i + m + 2, 2), f(i + m + 2, 3), f(i + m + 2, 4)
        print(
            '%s&%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
                cur_lang, cl[0], 'BF',
                bla, blp, blr, blf, blp2, blr2, blf2)
        )
        print(
            '%s&%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
                cur_lang, cl[0], 'COMP',
                cma, cmp, cmr, cmf, cmp2, cmr2, cmf2)
        )
        print(
            '%s&%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
                cur_lang, cl[0], 'BERT',
                bea, bep, ber, bef, bep2, ber2, bef2)
        )
    i += 40 if cl[0] == '6' else 31
