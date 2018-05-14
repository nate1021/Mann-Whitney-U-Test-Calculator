import utest_input
import numpy as np
import textbook_tables

samples, comparisons, alpha = utest_input.get_input()
alpha_per_test = alpha / (len(comparisons) * 2)
print('Two one-tailed U-tests will be run on each comparison, one in each direction. This is equivalent as running a single two-tailed U-test on each comparison.')
print('After applying Bonferroni correction, the significance value per one-tailed U-test will be %f.' % alpha_per_test)
print('When ranking the data, if there are ties in the data, the average rank will be assigned to data with ties.')
print('Many other software packages use an normal distribution approximation for larger (>20) sample set sizes. This program always uses the U-critical value tables regardless of the size of the sample set.')
print('\nRunning tests:')

for comp in comparisons:
    s1_name = comp[0]
    s1 = samples[s1_name]
    s2_name = comp[1]
    s2 = samples[s2_name]

    s_total = s1 + s2
    s_total.sort()

    rank_lookup = {}
    for i in range(0, len(s_total)):
        o_value = s_total[i]
        if o_value not in rank_lookup.keys():
            o_value_ranks = [i + 1]
            for j in range(i + 1, len(s_total)):
                if o_value == s_total[j]:
                    o_value_ranks.append(j + 1)
                else:
                    break
            o_value_average_rank = np.mean(o_value_ranks)
            rank_lookup[o_value] = o_value_average_rank

    s1_ranks = [rank_lookup[i] for i in s1]
    s2_ranks = [rank_lookup[i] for i in s2]

    n = len(s1)
    m = len(s2)
    u_stat1 = np.sum(s1_ranks) - ((n * (n + 1)) / 2)
    u_stat2 = np.sum(s2_ranks) - ((m * (m + 1)) / 2)

    #unit test:
    if (u_stat1 + u_stat2) != n * m:
        raise Exception('Unit test failed.')

    u_crit = textbook_tables.u_cirt(n=n, m=m, alpha=alpha_per_test)

    s1_larger_than_s2 = u_stat2 <= u_crit
    s2_larger_than_s1 = u_stat1 <= u_crit
    contradiction = s1_larger_than_s2 and s2_larger_than_s1

    null_s2 = 'H0: P(%s_item > %s_item) = 0.5' % (s1_name, s2_name)
    alt_s2 = 'H1: P(%s_item > %s_item) > 0.5' % (s1_name, s2_name)
    null_s1 = 'H0: P(%s_item > %s_item) = 0.5' % (s2_name, s1_name)
    alt_s1 = 'H1: P(%s_item > %s_item) > 0.5' % (s2_name, s1_name)
    contradiction_symbol = '*' if contradiction else ''

    print('For %s vs %s, U_critical: %s' % (s1_name, s2_name, str(u_crit) if u_crit >= 0 else ' not existent.'))
    if s1_larger_than_s2:
        print('    With U_stat: %s, the U-test rejected the null hypothesis, %s %s' % (u_stat2, null_s2, contradiction_symbol))
        print('    The alternative hypothesis, %s, can be accepted. %s' % (alt_s2, contradiction_symbol))
        print('    %s is stochastically larger than %s. %s' % (s1_name, s2_name, contradiction_symbol))
    else:
        print('    With U_stat: %s, the U-test failed to reject the null hypothesis, %s %s' % (u_stat2, null_s2, contradiction_symbol))
        print('    The alternative hypothesis, %s, cannot be accepted. %s' % (alt_s2, contradiction_symbol))
        print('    %s is not stochastically larger than %s. %s' % (s1_name, s2_name, contradiction_symbol))
    print('')

    if s2_larger_than_s1:
        print('    With U_stat: %s, the U-test rejected the null hypothesis, %s %s' % (u_stat1, null_s1, contradiction_symbol))
        print('    The alternative hypothesis, %s, can be accepted. %s' % (alt_s1, contradiction_symbol))
        print('    %s is stochastically larger than %s. %s' % (s2_name, s1_name, contradiction_symbol))
    else:
        print('    With U_stat: %s, the U-test failed to reject the null hypothesis, %s %s' % (u_stat1, null_s1, contradiction_symbol))
        print('    The alternative hypothesis, %s, cannot be accepted. %s' % (alt_s1, contradiction_symbol))
        print('    %s is not stochastically larger than %s. %s' % (s2_name, s1_name, contradiction_symbol))
    print('')
    if contradiction: #I don't think this could ever occur. It is just an emergency backup.
        print('    * marks tests which are contradicting one another. A type 1 error has occurred. The significance value was too high.')


print('\nProgram terminated.')