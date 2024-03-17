import os
from typing import Dict, Union, Literal

def parse_env_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return dict(map(lambda x: x.strip().split('='), lines))

dir_name = os.path.dirname(os.path.realpath(__file__))
env_file_path = os.path.join(dir_name, '.env')

Vars = Dict[Union[Literal['VOYAGE_API_KEY'], Literal['COLLECTION_NAME'], Literal['BATCH_SIZE'], Literal['MODEL_NAME']], str]
env_vars: Vars = {}
dot_env_file = {}
try:
    dot_env_file = parse_env_file(env_file_path)
except FileNotFoundError:
    pass
if os.environ.get('VOYAGE_API_KEY'):
    VOYAGE_API_KEY = os.environ.get('VOYAGE_API_KEY')
    assert isinstance(VOYAGE_API_KEY, str)
    env_vars['VOYAGE_API_KEY'] = VOYAGE_API_KEY
elif 'VOYAGE_API_KEY' in dot_env_file:
    env_vars['VOYAGE_API_KEY'] = dot_env_file['VOYAGE_API_KEY']
else:
    raise ValueError('VOYAGE_API_KEY not found in .env file or environment variables')

if os.environ.get('COLLECTION_NAME'):
    COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
    assert isinstance(COLLECTION_NAME, str)
    env_vars['COLLECTION_NAME'] = COLLECTION_NAME
elif 'COLLECTION_NAME' in dot_env_file:
    env_vars['COLLECTION_NAME'] = dot_env_file['COLLECTION_NAME']
else:
    raise ValueError('COLLECTION_NAME not found in .env file or environment variables')

if os.environ.get('BATCH_SIZE'):
    BATCH_SIZE = os.environ.get('BATCH_SIZE')
    assert isinstance(BATCH_SIZE, str)
    env_vars['BATCH_SIZE'] = BATCH_SIZE
elif 'BATCH_SIZE' in dot_env_file:
    env_vars['BATCH_SIZE'] = dot_env_file['BATCH_SIZE']
else:
    env_vars['BATCH_SIZE'] = '8'

if os.environ.get('MODEL_NAME'):
    MODEL_NAME = os.environ.get('MODEL_NAME')
    assert isinstance(MODEL_NAME, str)
    env_vars['MODEL_NAME'] = MODEL_NAME
elif 'MODEL_NAME' in dot_env_file:
    env_vars['MODEL_NAME'] = dot_env_file['MODEL_NAME']
else:
    raise ValueError('MODEL_NAME not found in .env file or environment variables')
