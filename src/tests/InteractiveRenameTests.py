import os
import re

regexp = re.compile('^test([0-9]+).p$')

variants = {'p': 'parsing', 'r': 'runtime', 't': 'typecheck', 'sc': 'scanner', 'st': 'symboltable'}
invertedVariants = {v: k for k, v in variants.items()}
variantsStr = ', '.join([f'{k} = {v}' for k, v in variants.items()])
existingVariants = dict()

for v in variants:
    existingVariants[v] = 0

for fileName in os.listdir('.'):
    if not os.path.isfile(fileName) or not fileName.endswith('.p'):
        continue

    for v in invertedVariants.keys():
        if fileName.startswith(v):
            existingVariants[invertedVariants[v]] += 1

print('Initial count sets:')
print(existingVariants)
print()

def nextName():
    ret = None
    while ret not in variants:
        print(f'Enter test variant; {variantsStr}')
        ret = input()
    return ret

print('Starting!')
for fileName in os.listdir('.'):
    if not os.path.isfile(fileName):
        continue

    matches = regexp.match(fileName)

    if matches is None:
        continue

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(f'Renaming: {fileName}')
    trg = nextName()
    print(variants[trg])
    try:
        os.rename(fileName, variants[trg] + str(existingVariants[trg]) + '.p')
        if os.path.exists(fileName + '.expect'):
            os.rename(fileName + '.expect', variants[trg] + str(existingVariants[trg]) + '.p.expect')
    except:
        print(f'failed to rename: {fileName}')
        exit(1)
    existingVariants[trg] += 1

print('No more found for renaming!')
print()
print('Post count sets:')
print(existingVariants)
