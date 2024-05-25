import aiofiles
from convert import convert
from fastapi import FastAPI, UploadFile, Form
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse
from tempfile import mkstemp
import os



app = FastAPI()

@app.get('/')
def index():
    return {'status': 200}

@app.post('/api/')
async def api(background_tasks: BackgroundTasks,
              file: UploadFile, 
              target_ext: str=Form(...)):
    target_ext = os.extsep + target_ext
    _, input_path = mkstemp()
    _, output_path = mkstemp(suffix=target_ext)

    async with aiofiles.open(input_path, 'wb') as input_file:
        await input_file.write(await file.read())

    await convert(input_path, output_path)

    os.remove(input_path)
    background_tasks.add_task(lambda: os.remove(output_path))
    
    return FileResponse(output_path)