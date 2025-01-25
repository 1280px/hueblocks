def compute_filter(lines, names, title = ''):
    if lines is None:
        print('Warning -- This filter doesn\'t have any lines specified!\n')
        return {}

    # If "title" is provided, show all the debug info
    if title:
        print(f'Filter "{title}":')

    # Sequentially computes a filter; returns LIST OF PAIRS of filtered
    # block names and filter type metadata, which will be used later for
    # prioritization of regular filter rules over wildcard filter rules.
    rules = {}
    if title:
        print(f'  - Computing filter from {len(lines)} lines...')

    for line in lines:
        # Exclude wildcard-only filter, just in case
        if line == '$':
            print('Wildcard filter "$" is not allowed -- like, why would you want to remove EVERYTHING from blockset?')
            continue
        
        line_star = line.find('$')

        if line_star == -1: # No wildcard
            rules[line] = 'R'

        elif line_star == len(line)-1: # Prefix wildcard
            for name in names:
                if name.startswith(line.split('$')[0]):
                    # Prioritize regular filters over wildcard!
                    if name not in rules or rules[name] != 'R':
                        rules[name] = 'W'

        elif line_star == 0: # Suffix wildcard
            for name in names:
                if name.endswith(line.split('$')[1]):
                    # Prioritize regular filters over wildcard!
                    if name not in rules or rules[name] != 'R':
                        rules[name] = 'W'

    if title:
        print(f'  - Finished computation into {len(rules)} rules.\n')
    return rules
