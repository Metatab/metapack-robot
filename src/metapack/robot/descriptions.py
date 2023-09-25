"""Generate text descriptions of datasets, data fiels and columns for use in
search engines and databases."""

from metapack import Resource, MetapackDoc
from typing import Union

def dataset_description(d: MetapackDoc):
    """Generate a description for a dataset, using the title and description"""

    return f"Dataset Name: {d.name}\nDataset Description: {d.description}\n"


def table_description(r: Resource):
    """Generate a description for a table, using the schema and the title"""

    return f"Table Name: {r.name}\nTable Description: {r.description}\n"


def column_description(c):
    from itertools import islice

    o = f"""Variable Name: {c['name']} 
Datatype: {c['datatype']}
Description: {c.get('description', '')}"""

    if 'labels' in c:
        l = '\n'.join([f'    {v}' for k, v in islice(c['labels'].items(), 20)])
        o += f"\nValues:\n{l}"

    o += "\n\n"
    return o


def description_context(r: Resource):
    return {
        'dataset_name': r.doc.name,
        'dataset_title': r.doc.get_value('Root.Title'),
        'dataset_description': r.doc.description,
        'table_name': r.name,
        'table_description': r.description,
        'columns': list(r.columns())
    }


desc_template = """Dataset Name: {dataset_name}
Dataset Title: {dataset_title}
Dataset Description: {dataset_description}
Table Name: {table_name}
Table Description: {table_description}
"""



def resource_description(r: Union[Resource, dict]):

    if isinstance(r, dict):
        c = r
    else:
        c = description_context(r)

    pre = desc_template.format(**c)

    col_text = []
    try:
        cols = r.columns()
    except AttributeError:
        cols = c['columns']

    for c in cols:
        col_text.append(pre + column_description(c))

    return col_text
