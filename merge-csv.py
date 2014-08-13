from glob import glob

with open('x/un-locode.csv', 'a') as mf:
    for filename in glob('*.csv'):
        with open(filename) as f:
            mf.write(f.read())
