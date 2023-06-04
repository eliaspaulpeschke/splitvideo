import sys, os, argparse, ffmpeg, math

parser = argparse.ArgumentParser(prog="Video Splitter", description="splits a video in parts and puts it in a neat folder structure using ffmpeg")

parser.add_argument('filename')
parser.add_argument('-d', '--duration', type=int, default=600)
parser.add_argument('-m', '--margin', type=float, default=1.0)
parser.add_argument('-b', '--folder-size', type=int, default=144)
args = parser.parse_args()

def main():
    video_metadata = ffmpeg.probe(args.filename)
    video_duration = float(video_metadata["format"]["duration"])
    number_of_videos = math.ceil(video_duration/args.duration)
    number_of_folders = math.ceil(number_of_videos/args.folder_size)
    main_folder_name = os.path.splitext(args.filename)[0]
    print(video_duration, number_of_videos, number_of_folders)
    
    os.mkdir(main_folder_name)
    actual_duration = args.duration+args.margin
    for i in range(number_of_videos):
        print(f"{i+1} of {number_of_videos}")
        folder = main_folder_name + "/" + str(math.floor((i+1) / args.folder_size) + 1)
        if (not os.path.exists(folder)):
            os.mkdir(folder)
        outfile = folder + "/" + f"{i}.mkv"
        start = (args.duration * i) - args.margin
        if (i == 0):
            start = 0
        if (i + 1 == number_of_videos):
            actual_duration = args.duration
        ffmpeg.input(args.filename, ss=start, t=actual_duration).output(outfile, vcodec="copy", acodec="copy").run(quiet=True)





if __name__ == "__main__":
    main()
