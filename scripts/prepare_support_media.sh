#!/bin/bash

set -euo pipefail

usage() {
  echo "Usage: scripts/prepare_support_media.sh INPUT_VIDEO OUTPUT_STEM POSTER_SECONDS OUTPUT_DIRECTORY" >&2
}

if [[ $# -ne 4 ]]; then
  usage
  exit 2
fi

input_video=$1
output_stem=$2
poster_seconds=$3
output_directory=$4

if [[ ! -f "$input_video" ]]; then
  echo "Input video does not exist: $input_video" >&2
  exit 1
fi

if [[ ! "$output_stem" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "Output stem must contain lowercase letters, numbers, and hyphens only." >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1 || ! command -v cwebp >/dev/null 2>&1; then
  echo "ffmpeg, ffprobe, and cwebp are required." >&2
  exit 1
fi

mkdir -p "$output_directory"

gif_output="$output_directory/$output_stem.gif"
poster_output="$output_directory/$output_stem-poster.webp"
poster_source="$output_directory/$output_stem-poster.png"

cleanup() {
  rm -f "$poster_source"
}
trap cleanup EXIT

ffmpeg -hide_banner -loglevel error -y \
  -i "$input_video" \
  -filter_complex "fps=6,scale=402:-2:flags=lanczos,split[frames][palette_source];[palette_source]palettegen=max_colors=128:stats_mode=diff[palette];[frames][palette]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle" \
  "$gif_output"

ffmpeg -hide_banner -loglevel error -y \
  -ss "$poster_seconds" \
  -i "$input_video" \
  -frames:v 1 \
  -vf "scale=402:-2:flags=lanczos" \
  "$poster_source"

cwebp -quiet -q 82 "$poster_source" -o "$poster_output"

gif_size=$(ffprobe -v error -show_entries format=size -of default=noprint_wrappers=1:nokey=1 "$gif_output")
max_size=$((1500 * 1024))

if (( gif_size > max_size )); then
  echo "GIF is $gif_size bytes, above the 1.5 MB limit. Shorten idle time or reduce the frame rate or dimensions." >&2
  exit 1
fi

ffprobe -v error \
  -show_entries stream=width,height,nb_frames,r_frame_rate,duration \
  -show_entries format=size \
  -of json \
  "$gif_output"

echo "Created $gif_output"
echo "Created $poster_output"
