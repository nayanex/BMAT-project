import pandas as pd

clustered_metada_file = 'data/works_metadata_output.csv'
clustered_metada_df = pd.read_csv(clustered_metada_file)

useless_collumns = ['prim_key', 'canonical_prim_key', 'canonical_title',
                    'canonical_contributors', 'canonical_iswc', 
                    'canonical_source', 'canonical_id']

clustered_metada_df.drop(useless_collumns, axis=1, inplace=True)

confident_duplicated_df = clustered_metada_df[clustered_metada_df['confidence_score'].notnull()]

non_confident_duplicated_df = clustered_metada_df[clustered_metada_df['confidence_score'].isnull()]


def treat_iswc(iswc_list):
    iswc_list = [x for x in group['iswc'].tolist() if str(x) != 'nan']
    return iswc_list[0] if iswc_list else None


for _, group in confident_duplicated_df.groupby('Cluster ID'): 
    title = max(group['title'].tolist(), key=len).split('|')
    contributors = max(group['contributors'].tolist(), key=len).split('|')
    iswc = treat_iswc(group['iswc'])
    sources = group['source'].tolist()
    source_identifiers = group['id'].tolist()
    print(contributors)