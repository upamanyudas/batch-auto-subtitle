import os
import subprocess
import argparse
import shutil
import sys
from tqdm import tqdm

def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = ['ffmpeg', 'ffprobe', 'auto_subtitle', 'subliminal']
    for dep in dependencies:
        if shutil.which(dep) is None:
            print(f"'{dep}' is not installed.")
            install_command = {
                'linux': f"sudo apt install {dep}",
                'darwin': f"brew install {dep}",
                'win32': f"choco install {dep}"
            }
            platform = sys.platform
            if platform in install_command:
                print(f"To install '{dep}', run: {install_command[platform]}")
            else:
                print(f"Please install '{dep}' manually.")
            sys.exit(1)

def get_video_files(base_dir, include_folders=None, exclude_folders=None):
    """Get a list of video files in the specified base directory."""
    video_files = []
    for root, dirs, files in os.walk(base_dir):
        if include_folders and not any(folder in root for folder in include_folders):
            continue
        if exclude_folders and any(folder in root for folder in exclude_folders):
            continue

        for file in files:
            if file.endswith(('.mkv', '.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(root, file))
    return video_files

def check_existing_subtitles(video_path):
    """Check if subtitles exist using ffprobe."""
    command_ffprobe = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=index,codec_type',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(command_ffprobe, capture_output=True, text=True)
    return 'subtitle' in result.stdout

def check_embedded_subtitles(video_path):
    """Check if the video has embedded subtitles using ffprobe."""
    command_ffprobe = [
        'ffprobe', '-v', 'error',
        '-select_streams', 's',
        '-show_entries', 'stream=index',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(command_ffprobe, capture_output=True, text=True)
    return len(result.stdout.strip()) > 0

def check_sync_with_subsync(video_path):
    """Check if subtitles are in sync using subsync."""
    print(f"Checking sync for: {video_path}")

    # Find the subtitle file
    subtitle_files = [f for f in os.listdir(os.path.dirname(video_path)) if f.endswith(('.srt', '.sub', '.vtt'))]

    # Use the first found subtitle file for sync checking (modify as needed)
    subtitle_file = next((f for f in subtitle_files if os.path.splitext(f)[0] in os.path.basename(video_path)), None)

    if subtitle_file:
        # Construct the full path to the subtitle file
        subtitle_path = os.path.join(os.path.dirname(video_path), subtitle_file)

        # Define the output path for the synchronized subtitles
        output_subtitle_path = os.path.splitext(subtitle_path)[0] + '.1.srt'

        # Run subsync in headless mode
        result = subprocess.run(['subsync', 'sync', '-c', '--sub', subtitle_path, '--ref', video_path, '--out', output_subtitle_path], capture_output=True, text=True)

        # Check for success based on output
        if '[+] done, saved to' in result.stdout:
            print("Subsync completed successfully.")

            # If the output file has the .1 suffix, delete the original subtitle file
            if output_subtitle_path.endswith('.1.srt'):
                os.remove(subtitle_path)
                # Rename the new file to the original subtitle file name
                os.rename(output_subtitle_path, subtitle_path)
            else:
                # Just rename the new file if it didn't have the .1 suffix
                os.rename(output_subtitle_path, subtitle_path)

            return True  # Sync successful
        else:
            print("Subsync failed.")
            return False  # Sync failed
    else:
        print(f"No subtitle file found for syncing with '{video_path}'.")
        return False  # No subtitle file found

def download_subtitles(video_path, language):
    """Download subtitles using subliminal and return success status."""
    print(f"Downloading subtitles for: {video_path}")

    # Run the subliminal command and capture the output
    result = subprocess.run(['subliminal', 'download', '-l', language, video_path], capture_output=True, text=True)

    # Check the output for success or failure
    if "Downloaded 1 subtitle" in result.stdout:
        return True  # Success
    else:
        return False  # Failure

def generate_subtitles(video_path, language):
    """Generate subtitles using auto_subtitle."""
    # Get the directory where the video is located
    video_dir = os.path.dirname(video_path)

    # Extract the video file name without the extension
    video_filename = os.path.splitext(os.path.basename(video_path))[0]

    # Construct the output subtitle path
    output_subtitle_path = os.path.join(video_dir, f"{video_filename}.srt")

    # Prepare the auto_subtitle command with the video directory as output_dir
    auto_subtitle_command = [
        'auto_subtitle',
        '--output_srt', 'True',
        '--srt_only', 'True',
        '--task', 'transcribe',
        '--language', language,
        '--output_dir', video_dir,  # Use video file's directory as the output directory
        video_path
    ]

    print(f"Running auto_subtitle for: {video_path}")
    subprocess.run(auto_subtitle_command)

    # Check if the output file was created
    if os.path.exists(output_subtitle_path):
        print(f"Subtitles successfully generated at: {output_subtitle_path}")
        return True
    else:
        print("Failed to generate subtitles.")
        return False

def check_existing_subtitle_files(video_path):
    """Check if any subtitle files exist for the given video."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_extensions = ('.srt', '.sub', '.vtt')

    # Check for subtitle files in the same directory
    directory = os.path.dirname(video_path)
    for ext in subtitle_extensions:
        for file in os.listdir(directory):
            if file.startswith(video_name) and file.endswith(ext):
                return True
    return False

def process_video(video_path, options):
    """Process a single video file to check subtitles and generate them if necessary."""
    if check_embedded_subtitles(video_path):
        print(f"Skipping '{video_path}' due to embedded subtitles.")
        return

    # Check for existing subtitle files
    if check_existing_subtitle_files(video_path):
        if check_sync_with_subsync(video_path): # Check sync if subtitles exist
            print(f"Synced subtitles for '{video_path}'")
        print(f"Progressing to next video.")
    else:
        if download_subtitles(video_path, options['output_subtitle_language']):
            print(f"Downloaded subtitles for '{video_path}'")
            if check_sync_with_subsync(video_path): # Check sync if subtitles exist
                print(f"Synced subtitles for '{video_path}'")
        else:
            generate_subtitles(video_path, options['output_subtitle_language'])
            if check_sync_with_subsync(video_path): # Check sync if subtitles exist
                print(f"Synced subtitles for '{video_path}'")
            print(f"Progressing to next video.")

def main():
    """Main function to parse arguments and process videos."""
    parser = argparse.ArgumentParser(description="Batch Auto Subtitle Generator (2024) by Upa Das")
    parser.add_argument('--base-dir', required=True, help='Base directory to search for video files')
    parser.add_argument('--output_dir', required=False, default='.', help='Output directory for subtitles (default beside video file)')
    parser.add_argument('--output-subtitle-language', required=False, default='en', help='Language for output subtitles (default: en)')
    parser.add_argument('--model', choices=['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo'], default='medium', help='Whisper model to use (default: small)')
    parser.add_argument('--include-folder', action='append', help='Folders to include in processing')
    parser.add_argument('--exclude-folder', action='append', help='Folders to exclude from processing')
    parser.add_argument('--include-lang', action='append', help='Languages to include')
    parser.add_argument('--exclude-lang', action='append', help='Languages to exclude')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='Batch Auto Subtitle Generator (2024) by Upa Das v1.12', help='Show the version of the script')

    options = vars(parser.parse_args())

    # Check for dependencies
    check_dependencies()

    # Get video files
    video_files = get_video_files(options['base_dir'], options['include_folder'], options['exclude_folder'])

    # Process each video file
    for video_path in tqdm(video_files, desc="Processing videos", unit="file"):
        process_video(video_path, options)

if __name__ == "__main__":
    main()
