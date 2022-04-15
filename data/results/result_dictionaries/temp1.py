import re

with open('./ReviewFeatures_Polarity_Reports.txt', 'r') as f:
    lines = f.readlines()

i, N = 0, len(lines)
while i < N:
    if lines[i].startswith('===') and lines[i].find('_eq_') == -1:
        la, _, le, _ = lines[i][4:-4].split('_')
        cur_lang = {'eng':'English','any':'Multilingual'}[la]
        cur_len = {'any':'Any','long':'Long','short':'Short'}[le]
        def f(i, j):
            return re.sub('\s\s+', ' ', lines[i]).split()[j]
        bla, blp, blr, blf = f(i + 6, 1), f(i + 7, 2), f(i + 7, 3), f(i + 7, 4)
        blp2, blr2, blf2 = f(i + 8, 2), f(i + 8, 3), f(i + 8, 4)
        cma, cmp, cmr, cmf = f(i + 15, 1), f(i + 16, 2), f(i + 16, 3), f(i + 16, 4)
        cmp2, cmr2, cmf2 = f(i + 17, 2), f(i + 17, 3), f(i + 17, 4)
        bea, bep, ber, bef = f(i + 24, 1), f(i + 25, 2), f(i + 25, 3), f(i + 25, 4)
        bep2, ber2, bef2 = f(i + 26, 2), f(i + 26, 3), f(i + 26, 4)
        print(
            '%s&%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
                cur_lang, cur_len, 'BF',
                bla, blp, blr, blf, blp2, blr2, blf2)
        )
        print(
            '%s&%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
                cur_lang, cur_len, 'COMP',
                cma, cmp, cmr, cmf, cmp2, cmr2, cmf2)
        )
        print(
            '%s&%s&%s&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$&$%s$\\\\' % (
                cur_lang, cur_len, 'BERT',
                bea, bep, ber, bef, bep2, ber2, bef2)
        )
    i += 28
