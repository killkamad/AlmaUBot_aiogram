import json

import aiofiles


async def json_data():
    async with aiofiles.open('utils/data.json', encoding='utf8', mode='r') as dataFile:
        dataF = await dataFile.read()
        dataFile = json.loads(dataF)
        return dataFile
