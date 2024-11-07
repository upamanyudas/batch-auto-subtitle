# Batch Auto Subtitle Generator

A powerful Python script to automate the generation, downloading, and synchronization of subtitles for video files. This tool leverages external tools like `subliminal` for subtitle downloads, `subsync` for subtitle synchronization, and `auto_subtitle` for auto-generating subtitles if none are available. It’s ideal for users who want a reliable subtitle management solution in batch processing mode.

## Features

- **Batch Video Processing**: Scan a directory and process video files in bulk.
- **Auto Subtitle Generation**: Generate subtitles automatically if none exist for the video.
- **Download Subtitles**: Download subtitles in the specified language if they aren’t available locally.
- **Subtitle Synchronization**: Synchronize existing or downloaded subtitles to match the video timing.
- **Detailed CLI Options**: Configure language, directories, inclusion/exclusion filters, and more.

## Prerequisites

This script requires several external tools to function effectively. Please ensure the following dependencies are installed:

1. **Python** - Tested on Python 3.8 and above.
2. **ffmpeg** and **ffprobe** - For video analysis.
3. **subliminal** - For subtitle downloads.
4. **subsync** - For subtitle synchronization.
5. **auto_subtitle** - For auto-generating subtitles.

### Installing Dependencies

- **ffmpeg**:
    - macOS: `brew install ffmpeg`
    - Linux: `sudo apt install ffmpeg`
    - Windows: Install via Chocolatey: `choco install ffmpeg`

- **subliminal**:
    ```bash
    pip install subliminal
    ```

- **subsync**:
    - macOS: [Download from the official website](https://subsync.online/)
    - Linux: Available as a flatpak: `flatpak install subsync`
    - Windows: [Download from the official website](https://subsync.online/)

- **auto_subtitle**:
    ```bash
    pip install auto_subtitle
    ```

## Usage

### Clone the Repository

```bash
git clone https://github.com/yourusername/batch-auto-subtitle-generator.git
cd batch-auto-subtitle-generator
```

### Run the Script

```bash
python batch_auto_subtitle.py --base-dir /path/to/your/video/files --output-subtitle-language en --model medium --verbose
```

### Command-line Arguments

- `--base-dir`: Base directory to search for video files (required).
- `--output_dir`: Output directory for subtitles (defaults to beside the video file).
- `--output-subtitle-language`: Language for output subtitles (default: `en`).
- `--model`: Whisper model for `auto_subtitle` (default: `medium`).
- `--include-folder`: Specify folders to include in processing (optional).
- `--exclude-folder`: Specify folders to exclude from processing (optional).
- `--include-lang`: Only process videos with specified audio languages (optional).
- `--exclude-lang`: Skip videos with specified audio languages (optional).
- `--verbose`: Enable verbose output.
- `--version`: Display the script version.

## Example

To process videos in the `/videos` directory, downloading or generating subtitles in English, and excluding any videos in `/videos/extras`:

```bash
python batch_auto_subtitle.py --base-dir /videos --output-subtitle-language en --exclude-folder extras --verbose
```

## Detailed Workflow

1. **Dependency Check**: Ensures all required dependencies are installed.
2. **Video File Retrieval**: Scans the specified directory for video files, filtering based on inclusion/exclusion folders.
3. **Subtitle Management**:
   - **Subtitle Check**: Verifies if a compatible subtitle file exists for each video.
   - **Download Subtitles**: If no subtitle exists, `subliminal` attempts to download a subtitle file in the specified language.
   - **Synchronize Subtitles**: Uses `subsync` to sync existing or downloaded subtitles. Success is marked by "done" and "writing output to" in the output.
   - **Auto-Generate Subtitles**: If download and existing subtitle checks fail, `auto_subtitle` generates subtitles.

## License

This project is licensed under the MIT License.

---

For any questions, feedback, or contributions, please feel free to open an issue or submit a pull request!
