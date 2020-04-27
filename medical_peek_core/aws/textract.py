import logging
from typing import List

import boto3

logger = logging.getLogger(__name__)


def _get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}

                    # get the text value
                    rows[row_index][col_index] = _get_text(cell, blocks_map)
    return rows


def _get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '
    return text


def _clean_text(txt):
    new_text = str(txt).replace(',', '')
    new_text = str(new_text).replace('"', '')
    return new_text


def _generate_table_csv(table_result, blocks_map):
    rows = _get_rows_columns_map(table_result, blocks_map)

    output = []

    for row_index, cols in rows.items():
        output.append([])
        for col_index, text in cols.items():
            new_text = _clean_text(text)
            output[row_index - 1].append(new_text)

    return output


def extract_tables_from_byte_array(byte_array: bytearray) -> List[List[str]]:
    client = boto3.client('textract')
    response = client.analyze_document(Document = {'Bytes': byte_array}, FeatureTypes = ['TABLES'])

    blocks = response['Blocks']
    logger.debug(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return []

    csv = []
    for index, table in enumerate(table_blocks):
        csv += _generate_table_csv(table, blocks_map)

    return csv
