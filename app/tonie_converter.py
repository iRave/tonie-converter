import reflex as rx
import os
from .converter_utils import convert_to_mp3

class ConverterState(rx.State):
    file_path: str = ""
    bitrate: str = "192k"
    samplerate: str = "44100"
    channels: str = "2"
    normalize: bool = False
    message: str = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_path = os.path.join("uploads", file.filename)
            with open(upload_path, "wb") as f:
                f.write(await file.read())
            self.file_path = upload_path
        self.message = f"Datei '{file.filename}' erfolgreich hochgeladen."

    async def convert_file(self):
        if not self.file_path:
            self.message = "Bitte zuerst eine Datei hochladen."
            return
        try:
            output_path = convert_to_mp3(
                self.file_path,
                bitrate=self.bitrate,
                samplerate=self.samplerate,
                channels=self.channels,
                normalize=self.normalize
            )
            self.message = f"✅ Konvertierung erfolgreich: {os.path.basename(output_path)}"
        except Exception as e:
            self.message = f"❌ Fehler: {e}"

def index() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("🎧 Tonie Converter", size="8"),
                rx.text("Konvertiere Audio-Dateien (FLAC/WAV/M4A) in MP3 – direkt für deine Creative-Tonies."),
                rx.divider(),
                rx.upload(
                    rx.button("Datei auswählen", color_scheme="blue", variant="solid"),
                    id="upload",
                    accept="audio/*",
                    on_upload=ConverterState.handle_upload,
                ),
                rx.text(ConverterState.message, color="green"),
                rx.hstack(
                    rx.vstack(
                        rx.text("Bitrate"),
                        rx.select(["128k", "192k", "256k", "320k"], value=ConverterState.bitrate, on_change=ConverterState.set_bitrate),
                    ),
                    rx.vstack(
                        rx.text("Sampling Rate"),
                        rx.select(["44100", "48000"], value=ConverterState.samplerate, on_change=ConverterState.set_samplerate),
                    ),
                    rx.vstack(
                        rx.text("Kanäle"),
                        rx.select([("1", "Mono"), ("2", "Stereo")], value=ConverterState.channels, on_change=ConverterState.set_channels),
                    ),
                    rx.vstack(
                        rx.text("Normalisieren"),
                        rx.switch(is_checked=ConverterState.normalize, on_change=ConverterState.set_normalize),
                    ),
                ),
                rx.button("➡️ Konvertieren", color_scheme="green", on_click=ConverterState.convert_file),
                rx.text(ConverterState.message, color="gray"),
            ),
            width="700px",
            padding="30px",
            shadow="md",
            border_radius="lg",
            background_color="white",
        ),
        bg="gray.100",
        padding="50px",
        height="100vh",
    )

app = rx.App()
app.add_page(index, title="Tonie MP3 Converter")