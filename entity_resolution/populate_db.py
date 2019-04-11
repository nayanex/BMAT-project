import pandas as pd
import psycopg2

clustered_metada_file = 'data/works_metadata_output.csv'
clustered_metada_df = pd.read_csv(clustered_metada_file)

useless_collumns = ['prim_key', 'canonical_prim_key', 'canonical_title',
                    'canonical_contributors', 'canonical_iswc', 
                    'canonical_source', 'canonical_id']

clustered_metada_df.drop(useless_collumns, axis=1, inplace=True)

confident_duplicated_df = clustered_metada_df[clustered_metada_df['confidence_score'].notnull()]

non_confident_duplicated_df = clustered_metada_df[clustered_metada_df['confidence_score'].isnull()]

con = psycopg2.connect(database='works_single_view',
                       user='postgres',
                       host='localhost')


def treat_iswc(iswc_list):
    iswc_list = [x for x in iswc_list if str(x) != 'nan']
    return iswc_list[0] if iswc_list else None


def import2database(con):

    cur = con.cursor()

    print('Importing song metadata to works_single_view database...')

    for _, group in confident_duplicated_df.groupby('Cluster ID'): 
        title = max(group['title'].tolist(), key=len).split('|')[0]
        contributors = max(group['contributors'].tolist(), key=len).split('|')
        iswc = treat_iswc(group['iswc'])
        sources = group['source'].tolist()
        source_ids = group['id'].tolist()

        cur.execute("INSERT INTO song_metadata (title, contributors, iswc, \
            sources, source_ids) VALUES (%s, %s, %s, %s, %s)",
                    (title, contributors, iswc, sources, source_ids))

    con.commit()
    con.close()


try:
    import2database(con)
finally:
    con.close()

