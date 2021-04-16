import re

import boto3


def get_raw_text(response):
    # Print detected text
    returnable = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            returnable += " " + item["Text"]
    return returnable


def get_kv_map(img_bytes):
    # process using image bytes
    client = boto3.client('textract')
    response = client.analyze_document(Document={'Bytes': img_bytes}, FeatureTypes=['FORMS'])

    # Get the text blocks
    blocks = response['Blocks']

    # get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block

    return key_map, value_map, block_map, get_raw_text(response)


def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key] = val
    return kvs


def find_value_block(key_block, value_map):
    global value_block
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text(result, blocks_map):
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


def search_value(kvs, search_key):
    for key, value in kvs.items():
        if re.search(search_key, key, re.IGNORECASE):
            return value


def retrieve_from_file_name(file_name):
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        return get_kv_map(bytes_test)


def execute(file_name):
    key_map, value_map, block_map, raw_text = retrieve_from_file_name(file_name)

    returnable = {}

    # Get Key Value relationship
    kvs = get_kv_relationship(key_map, value_map, block_map)
    returnable['raw_text'] = raw_text
    returnable['key_value_pairs'] = kvs

    if len(returnable) == 0:
        return None

    return returnable


if __name__ == '__main__':
    print(execute('./HKID_Ritvik.png'))
