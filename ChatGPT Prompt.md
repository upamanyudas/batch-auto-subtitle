write me a python terminal script for a subtitle generator.

- it mostly likely will be run from inside a folder. it will ask for confirmation for the same. if not it will ask for the complete path for the 'base folder'
- check if ffmpeg, ffprobe, auto_subtitle and any other dependancies used in the script are installed. if not help the user install them for the specific platform.
- when run it will process video files inside all the sub-folders and sub-sub-folders only inside the folder the script is run from.
- it only generates an `.srt` file instead of a video file with overlay.
- it will have the following available options

(OPTIONAl) --help will print script name (Batch Auto Subtilte Generator) and year and script writers name and open source libraries used first. and print all the options available and other things that are generally present in help.

(REQUIRED) --base-dir DIR. Tab supported in terminal.

(OPTIONAL) --output_dir OUTPUT_DIR. Tab supported in terminal. default beside each video file.

(OPTIONAL) --output-subtitle-language LANG_CODE. .translate only if input video laguage not equals --output-subtitle-language. default output language english.

(OPTIONAL) --model MODEL {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large-v3,large,large-v3-turbo,turbo}. name of the Whisper model to use (default: small)

(OPTIONAL) --include-folder or --exclude-folder FOLDER_NAME accept (spaces allowed) folder names to include or exclude. the folders names can be a sub folder or a sub sub folder or at any level of the directory inside the folder the script is run from. it can accept the names for folders like `Folder name` or a path inside like `4K/Folder Name` or `./4K/Folder name` or `full/path/to/Folder Names`. default is all folders are included. only include or exclude can be used at a time. multiple only includes or only exludes are accepted

(OPTIONAL) --include-lang LANG_CODE or --exclude-lang LANG_CODE for languages to include or exclude (af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh). default all languages are processd. only --include-lang or --exclude-lang can be used at a time. multiple only includes or only exludes are accepted

(OPTIONS) --verbose will output everything. each command structure as its executed and the outputs.

- files are processed one by one inside the sub-folders. based on --include-folder or --exclude-folder if they are used.
- once the details are entered first `ffprobe` (and file check) will be used to determine if the file has a subtitle. check the relevant ffprobe docs here : https://ffmpeg.org/ffprobe.html.
- if subtitle exists use `subsync` to check if the existing subtitle is in sync. if not sync up
- after that if a subtitle doesn't exist, download subtitle using `filebot` cli (https://www.filebot.net/cli.html) to download subtitles if available online
- use `subsync` again to check if the downloaded subtitle is in sync. if not sync up
- then file is passed to `auto_subtitle`.
- the the file is processed using `auto_subtitle` https://github.com/m1guelpf/auto-subtitle. the docs for `auto_subtitle`
usage: auto_subtitle [-h]
                     [--model {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large-v3,large,large-v3-turbo,turbo}]
                     [--output_dir OUTPUT_DIR] [--output_srt OUTPUT_SRT] [--srt_only SRT_ONLY]
                     [--verbose VERBOSE] [--task {transcribe,translate}]
                     [--language {auto,af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}]
                     video [video ...]

positional arguments:
  video                 paths to video files to transcribe

options:
  -h, --help            show this help message and exit
  --model {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large-v3,large,large-v3-turbo,turbo}
                        name of the Whisper model to use (default: small)
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        directory to save the outputs (default: .)
  --output_srt OUTPUT_SRT
                        whether to output the .srt file along with the video files (default: False)
  --srt_only SRT_ONLY   only generate the .srt file and not create overlayed video (default: False)
  --verbose VERBOSE     whether to print out the progress and debug messages (default: False)
  --task {transcribe,translate}
                        whether to perform X->X speech recognition ('transcribe') or X->English translation
                        ('translate') (default: transcribe)
  --language {auto,af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh}
                        What is the origin language of the video? If unset, it is detected automatically.
                        (default: auto)

- also pass the relevant options from my script to `auto_subtitle`.
- `auto_subtitle` prints `Detected language: XXX` before generating the subtitle. it will stop here for the file based on the --include/--exclude-lang options from my script
- process the next file
- show a overall progress bar like so 
1%|█                                                    | 342756/351756
