from pathlib import Path
import gradio as gr
from zipfile import ZipFile
import os
import shutil

INPUT_DIR = os.path.join(os.path.dirname(__file__), "IN")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "OUT")


def clean_dir(directory):
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))


def make_zip(files):
    zip_path = os.path.join(OUTPUT_DIR, "extracted.zip")

    with ZipFile(zip_path, "w") as zip:
        for file in files:
            zip.write(os.path.join(INPUT_DIR, file), file)

    return zip_path


def upload_file(files):
    clean_dir(INPUT_DIR)
    clean_dir(OUTPUT_DIR)

    for file in files:
        shutil.move(file, INPUT_DIR)

    zip = make_zip(os.listdir(INPUT_DIR))

    return [
        gr.Files(visible=False),
        gr.DownloadButton(label="Download", value=zip, visible=True)
    ]


def download_file():
    return [
        gr.Files(value=None, visible=True),
        gr.DownloadButton(visible=False)
    ]


with gr.Blocks() as demo:
    gr.Markdown("Upload a file to extract the manuscripts.")
    with gr.Row():
        up = gr.Files(label="Upload manuscripts")
        down = gr.DownloadButton("Download the file", visible=False)

    up.upload(upload_file, up, [up, down], show_progress=True)
    down.click(download_file, None, [up, down])


if __name__ == "__main__":
    if not os.path.exists(INPUT_DIR):
        os.mkdir(INPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    
    demo.queue().launch()
	