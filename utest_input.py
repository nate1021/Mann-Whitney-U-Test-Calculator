import sys

def get_input():
    def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")



    while True:
        sample_set_names = []
        print('Enter the names of your sample sets, separated by newlines, enter a blank line when done.')
        print('For example, if you wanted to compare a few sorting algorithms, type: QuickSort <enter> InsertSort <enter> MergeSort <enter> <enter>')
        print('You will then be asked to enter the sample values for each of these sample sets.')
        print('Names:')
        while True:
            value = input()
            if value == '':
                break
            if value in sample_set_names:
                print('Names must be unique.')
                continue
            if value.lower() == 'vs':
                print('\'vs\' is a keyword which cannot be used.')
                continue
            sample_set_names.append(value.lower())

        if len(sample_set_names) < 2:
            print('Enter at least 2 sample sets.')
            print('Previous sample sets cleared.')
            continue

        print('Sample sets: ' + str(sample_set_names))
        if query_yes_no('Proceed with these sample sets?', default='yes'):
            break
        else:
            print('Previous sample sets cleared.')

    samples = {}
    for name in sample_set_names:
        while True:
            lst = []
            print('Enter sample values for sample set \'%s\', separated by newlines, enter a blank line when done: ' % name)
            while True:
                value = input()
                if value == '':
                    break
                try:
                    value = float(value)
                    lst.append(value)
                except ValueError:
                    print('\'%s\' cannot be formatted as a number.' % value)

            if len(lst) < 2:
                print('Enter at least 2 samples.')
                print('Previous samples cleared.')
                continue

            print('Sample values: ' + str(lst))
            if query_yes_no('Proceed with these values?', default='yes'):
                samples[name] = lst
                break
            else:
                print('Previous values for this sample set cleared.')


    while True:
        comparisons = []
        print('Which samples sets would you like to compare?')
        print('Enter the comparisons in this format: sampleSet1 vs sampleSet2')
        print('Use the wildcard \'*\' to compare against all other sample sets.')
        print('The following would compare quick sort to insert sort: QuickSort vs InsertSort <enter> <enter>')
        print('The following would compare merge sort to insert sort and quick sort: MergeSort vs * <enter> <enter>')
        print('The following would compare all sorts to all other sorts: * vs * <enter> <enter>')
        print('Enter comparisons, separated by newlines, enter a blank line when done:')
        while True:
            value = input()
            if value == '':
                break
            try:
                data = value.split(' vs ')
                if data[0] not in samples.keys() and data[0] != '*':
                    print('\'%s\' is not the name of a sample set.' % data[0])
                if data[1] not in samples.keys() and data[1] != '*':
                    print('\'%s\' is not the name of a sample set.' % data[1])
                name0 = data[0].lower()
                name1 = data[1].lower()
                if name0 == '*' and name1 == '*':
                    for name0s in samples.keys():
                        for name1s in samples.keys():
                            if name0s != name1s:
                                pair = (name0s, name1s)
                                if pair not in comparisons and (pair[1], pair[0]) not in comparisons:
                                    comparisons.append(pair)
                elif name0 == '*':
                    for name in samples.keys():
                        if name != name1:
                            pair = (name, name1)
                            if pair not in comparisons and (pair[1], pair[0]) not in comparisons:
                                comparisons.append(pair)
                elif name1 == '*':
                    for name in samples.keys():
                        if name != name0:
                            pair = (name0, name)
                            if pair not in comparisons and (pair[1], pair[0]) not in comparisons:
                                comparisons.append(pair)
                else:
                    pair = (name0, name1)
                    if pair not in comparisons and (pair[1], pair[0]) not in comparisons:
                        comparisons.append(pair)
            except:
                print('Could not parse the comparison. Please use this format: sampleSet1 vs sampleSet2')

        if len(comparisons) < 1:
            print('Enter at least 1 comparison.')
            print('Previous comparisons cleared.')
            continue

        print('Comparison pairs: ' + str(comparisons))
        if query_yes_no('Proceed with these comparisons?', default='yes'):
            break
        else:
            print('Previous comparisons cleared.')

    while True:
        alpha = input('Enter the overall significance value (alpha) you would like to use (0.05 is common): ')
        try:
            alpha = float(alpha)
            if alpha > 1 or alpha <= 0:
                print('Not a valid significance value.')
                continue
            if query_yes_no('Proceed with this significance value?', default='yes'):
                break
        except ValueError:
            print('Not a valid number.')

    return samples, comparisons, alpha
