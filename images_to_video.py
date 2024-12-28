import argparse
import ffmpeg
import os


def images_to_video(image_dir, file_prefix, output_video, framerate):
    """
    Convert images with a specific prefix to a video using ffmpeg, optimized for post-editing.

    Args:
        image_dir (str): Directory containing the images (e.g., '/path/to/images').
        file_prefix (str): Prefix of the image files (e.g., 'frame').
        output_video (str): Path for the output video file (e.g., 'output.mp4').
        framerate (int): Frame rate for the video.
    """
    input_pattern = f"{image_dir}/{file_prefix}_%04d.png"

    if not os.path.exists(image_dir):
        print(f"Error: Image directory '{image_dir}' does not exist.")
        return

    try:
        (
            ffmpeg
            .input(input_pattern, framerate=framerate)
            .output(
                output_video,
                vcodec="libx264",         # H.264 codec for compatibility
                crf=18,                  # High-quality compression
                preset="slow",           # Balanced encoding speed
                pix_fmt="yuv420p",       # Ensure compatibility
                r=framerate,             # Set frame rate
                maxrate="15M",           # Max video bitrate
                bufsize="30M",           # Buffer size for bitrate control
                an=None                  # Disable audio stream
            )
            .run(overwrite_output=True)
        )
        print(f"Video saved to {output_video}")
    except ffmpeg.Error as e:
        print(f"Error during video generation: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Convert a sequence of images to a video.")
    parser.add_argument("--image_dir", type=str, required=True, help="Directory containing the image sequence.")
    parser.add_argument("--file_prefix", type=str, required=True, help="Prefix of the image files (e.g., 'frame').")
    parser.add_argument("--output_video", type=str, required=True, help="Path to the output video file (e.g., 'output.mp4').")
    parser.add_argument("--framerate", type=int, default=24, help="Frame rate of the output video (default: 24).")

    args = parser.parse_args()

    images_to_video(
        image_dir=args.image_dir,
        file_prefix=args.file_prefix,
        output_video=args.output_video,
        framerate=args.framerate,
    )


if __name__ == "__main__":
    main()
