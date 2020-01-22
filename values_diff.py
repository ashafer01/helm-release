import sys
import yaml
from glob import glob
from jsonpatch import JsonPatch

def yaml_display_format(obj, indent=0, prefix=''):
    formatted = yaml.dump(obj, default_flow_style=False).rstrip('\n.')
    if indent:
        newline = '\n' + prefix + (' ' * indent)
        formatted = formatted.replace('\n', newline) + '\n'
    elif '\n' in formatted:
        formatted += '\n'
    return formatted


def abort():
    sys.exit(2)


old_values_fn, new_values_fn, user_values_fn = sys.argv[1:4]

with open(old_values_fn) as f:
    old_values = yaml.safe_load(f)

with open(new_values_fn) as f:
    new_values = yaml.safe_load(f)

with open(user_values_fn) as f:
    user_values = yaml.safe_load(f)

chart_values_diff = JsonPatch.from_diff(old_values, new_values)

# Process diffs

apply_patch = []
edit_notes = []

add_ops = []
remove_ops = []
replace_ops = []

_missing = object()

for op in chart_values_diff._ops:
    op_name = op.operation['op']
    op_value = op.operation['value']
    user_value = op.pointer.resolve(user_values, _missing)
    if op_name == 'remove':
        if user_value is not _missing:
            remove_ops.append(op)
    elif op_name == 'add':
        if user_value is not _missing:
            op.operation['op'] = 'replace'
        if op_value != user_value:
            add_ops.append(op)
    elif op_name == 'replace':
        if user_value is _missing:
            op.operation['op'] = 'add'
        if op_value != user_value
            replace_ops.append(op)

# Handle values removed from default

if remove_ops:
    print('Default parameters have been removed from the')
    print('chart values.yaml since the last release:')
    for op in remove_ops:
        print('  {path}'.format(**op.operation))
    print('Choose an option:')
    print('  1) Remove all from release values.yaml')
    print('  2) Choose which to keep/remove in release values.yaml')
    print('  3) Keep all in release values.yaml')
    print('  x) Abort without writing any changes')
    while True:
        sel = input('Enter choice (1): ')
        if sel == '1' or not sel:
            for op in remove_ops:
                apply_patches.append(op.operation)
        elif sel == '2':
            keep_all = False
            remove_all = False
            print()
            for op in remove_ops:
                current_value = op.pointer.resolve(user_values, _missing)
                if remove_all:
                    apply_patches.append(op.operation)
                else:
                    print(op.pointer.path)
                    print('  | Current value: ', end='')
                    print(yaml_display_format(current_value, indent=15, prefix='  | '))
                    print('  | Choose an option:')
                    print('  |   1) Remove value')
                    print('  |   2) Keep value')
                    print('  |   3) Remove this value and all the rest')
                    print('  |   4) Keep this value and all the rest')
                    print('  |   5) Keep and remind me to edit after upgrade is complete')
                    print('  |   x) Abort without writing any changes')
                    while True:
                        subsel = input('  | Enter choice (1): ')
                        if subsel == '1' or not subsel:
                            apply_patches.append(op.operation)
                        elif subsel == '2':
                            pass
                        elif subsel == '3':
                            apply_patches.append(op.operation)
                            remove_all = True
                        elif subsel == '4':
                            keep_all = True
                            break
                        elif subsel == '5':
                            edit_notes.append(op.pointer.path)
                        elif subsel == 'x':
                            abort()
                        else:
                            print('  | Unknown selection')
                            continue
                        break
                    if keep_all:
                        break
        elif sel == '3':
            pass
        elif sel == 'x':
            abort()
        else:
            print('Unknown selection')
            continue
        break
    print()
    print('All removed parameters have been handled!')
    print()
    print('--')
    print()


# Handle values added to default

if add_ops:
    print('Default parameters have been added to the')
    print('chart values.yaml since the last release.')
    print()
    null_values = []
    default_value_ops = []
    for op in add_ops:
        if op.operation['value'] is None:
            null_values.append(op.pointer.path)
            edit_notes.append(op.pointer.path)
        else:
            default_value_ops.append(op)

    if null_values:
        print('The following parameters have a new default')
        print("value of `null` and you'll be reminded to edit")
        print('them after the upgrade is complete:')
        for path in null_values:
            print('  {}'.format(path))
        print()

    if default_value_ops:
        print('That leaves the following new parameters that')
        print('have a new specified default:')
        for op in default_value_ops:
            print('  {}'.format(op.pointer.path))
        print('What do you want to do with them?')
        print('  1) Add all the new defaults to values.yaml')
        print('  2) Add all new defaults and remind me to edit them all after the upgrade')
        print('  3) Pick which ones to remind me about')
        print('  x) Abort without writing any changes')
        while True:
            sel = input('Enter choice (1): ')
            if sel == '1' or not sel:
                for op in default_value_ops:
                    apply_patches.append(op.operation)
            elif sel == '2':
                for op in default_value_ops:
                    apply_patches.append(op.operation)
                    edit_notes.append(op.pointer.patch)
            elif sel == '3':
                for op in default_value_ops:
                    user_value = op.pointer.resolve(user_values, _missing)
                    if user_value is _missing:
                        user_value_display = '<No value currently set>'
                    else:
                        user_value_display = yaml_display_format(user_value, indent=20, prefix='  | ')
                    print(op.pointer.path)
                    print('  | Current user value: ', end='')
                    print(user_display_value)
                    print('  |  New default value: ', end='')
                    print(yaml_display_format(current_value, indent=20, prefix='  | '))
                    print('  | Choose an option:')
                    if user_value is _missing:
                        print('  |   1) [Cannot keep value unset]')
                        default_sel = '2'
                    else:
                        print('  |   1) Keep current user value')
                        default_sel = '1'
                    print('  |   2) Use new default value')
                    print('  |   3) Use new default value and add edit reminder after upgrade')
                    while True
                        subsel = input('  | Enter choice ({}): '.format(default_sel))
                        if subsel == '1' or (not subsel and default_sel == '1'):
                            if user_value is _missing:
                                continue
                            else:
                                pass
                        elif subsel == '2' or (not subsel and default_sel == '2'):
                            apply_patches.append(op.operation)
                        elif subsel == '3':
                            apply_patches.append(op.operation)
                            edit_notes.append(op.pointer.path)
                        else:
                            print('  | Unknown selection')
                            continue
                        break
                        
            else:
                print('Unknown selection')
                continue
            break
        print()
    print('All newly added parameters have been handled!')
    print()
    print('--')
    print()

# Handle default replacements

if replace_ops:
    # TODO
    pass
