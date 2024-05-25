from ffmpeg.asyncio import FFmpeg


async def convert(input_path, output_path):
    ffmpeg = (
        FFmpeg().
        option('y').
        input(input_path).
        output(output_path)
    )
    await ffmpeg.execute()
    return 

