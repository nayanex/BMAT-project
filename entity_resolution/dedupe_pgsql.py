import dedupe
import os
import re
import collections
import time

import psycopg2 as psy
import psycopg2.extras
from unidecode import unidecode

settings_file = 'entity_resolution/postgres_settings'
training_file = 'entity_resolution/postgres_training.json'

start_time = time.time()

con = psy.connect(database='works_single_view',
                  user='postgres',
                  host='localhost')

con2 = psy.connect(database='works_single_view',
                   user='postgres', 
                   host='localhost')

cur = con.cursor(cursor_factory=psy.extras.RealDictCursor)

SONG_MDT_SELECT = 'SELECT id, title, contributors, iswc FROM\
                   works_single_view_app_songmetadata'


def preProcess(column):
    if type(column) is list:
        column = '|'.join(column)
        print("JOOOOIN")
        
    if isinstance(column, int) or column is None:
        return column
        
    try:
        column = column.decode('utf8')
    except AttributeError:
        pass
    print("AAAQUIIIII")
    print(column)
    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    if not column:
        column = None
    return column


print('importing data ...')
cur.execute(SONG_MDT_SELECT)
data = cur.fetchall()
data_d = {}
for row in data:
    
    clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
    row_id = int(row['id'])
    data_d[row_id] = dict(clean_row)
    print("data DDDDDDDDDDDDDDD pooooorra")
    print(data_d)
    print("data ACCAAABOU pooooorra")

if os.path.exists(settings_file):
    print('reading from', settings_file)
    with open(settings_file) as sf:
        deduper = dedupe.StaticDedupe(sf)
    

else:
    fields = [
        {'field': 'title', 'type': 'String'},
        {'field': 'contributors', 'type': 'String'},
        {'field': 'iswc', 'type': 'Exact', 'has missing': True},
    ]

    deduper = dedupe.Dedupe(fields)

    deduper.sample(data_d, 150000)

    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file) as tf:
            deduper.readTraining(tf)

    print('starting active labeling...')

    dedupe.consoleLabel(deduper)

    deduper.train()

    with open(training_file, 'w') as tf:
        deduper.writeTraining(tf)

    with open(settings_file, 'wb') as sf:
        deduper.writeSettings(sf)

print('blocking...')

threshold = deduper.threshold(data_d, recall_weight=2)

print('clustering...')
clustered_dupes = deduper.match(data_d, threshold)

print('# duplicate sets', len(clustered_dupes))

cur2 = con2.cursor()
cur2.execute('SELECT * FROM works_single_view_app_songmetadata')
data = cur2.fetchall()

full_data = []

cluster_membership = collections.defaultdict(lambda: 'x')
for cluster_id, (cluster, score) in enumerate(clustered_dupes):
    for record_id in cluster:
        for row in data:
            if record_id == int(row[0]):
                row = list(row)
                row.insert(0, cluster_id)
                row = tuple(row)
                full_data.append(row)

columns = "SELECT column_name FROM information_schema.columns WHERE\
          table_name = 'works_single_view_app_songmetadata'"

cur2.execute(columns)
column_names = cur2.fetchall()
column_names = [x[0] for x in column_names]
column_names.insert(0, 'cluster_id')

cur2.execute('DROP TABLE IF EXISTS deduped_table')
field_string = ','.join('%s varchar(200)' % name for name in column_names)
cur2.execute('CREATE TABLE deduped_table (%s)' % field_string)
con2.commit()

num_cols = len(column_names)
mog = "(" + ("%s,"*(num_cols - 1)) + "%s)"
args_str = ','.join(cur2.mogrify(mog, x).decode('utf-8') for x in full_data)
values = "(" + ','.join(x for x in column_names) + ")"
cur2.execute("INSERT INTO deduped_table %s VALUES %s" % (values, args_str))
con2.commit()
con2.close()
con.close()

print('ran in', time.time() - start_time, 'seconds')
