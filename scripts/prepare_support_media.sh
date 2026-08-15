#!/bin/bash

set -euo pipefail

usage() {
  echo "Usage: scripts/prepare_support_media.sh INPUT_VIDEO OUTPUT_STEM POSTER_SECONDS OUTPUT_DIRECTORY [TIMELINE_CSV [OPENING_IMAGE OPENING_SECONDS [MARKERS_CSV]]]" >&2
}

if [[ $# -lt 4 || $# -gt 8 || $# -eq 6 ]]; then
  usage
  exit 2
fi

input_video=$1
output_stem=$2
poster_seconds=$3
output_directory=$4
timeline=${5:-}
opening_image=${6:-}
opening_seconds=${7:-}
markers=${8:-}
script_directory=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [[ ! -f "$input_video" ]]; then
  echo "Input video does not exist: $input_video" >&2
  exit 1
fi

if [[ ! "$output_stem" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "Output stem must contain lowercase letters, numbers, and hyphens only." >&2
  exit 1
fi

if [[ -n "$timeline" && ! -f "$timeline" ]]; then
  echo "Timeline does not exist: $timeline" >&2
  exit 1
fi

if [[ -n "$opening_image" && ! -f "$opening_image" ]]; then
  echo "Opening image does not exist: $opening_image" >&2
  exit 1
fi

if [[ -n "$opening_seconds" && ! "$opening_seconds" =~ ^([1-9][0-9]*([.][0-9]+)?|0[.][0-9]*[1-9][0-9]*)$ ]]; then
  echo "Opening duration must be a positive number of seconds." >&2
  exit 1
fi

if [[ -n "$markers" && ! -f "$markers" ]]; then
  echo "Markers file does not exist: $markers" >&2
  exit 1
fi

if [[ -n "$markers" && -z "$timeline" ]]; then
  echo "Markers require a timeline so their named phases can be resolved." >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1 || ! command -v cwebp >/dev/null 2>&1; then
  echo "ffmpeg, ffprobe, and cwebp are required." >&2
  exit 1
fi

if [[ -n "$markers" ]] && ! command -v magick >/dev/null 2>&1; then
  echo "ImageMagick's magick command is required for marker overlays." >&2
  exit 1
fi

mkdir -p "$output_directory"

gif_output="$output_directory/$output_stem.gif"
poster_output="$output_directory/$output_stem-poster.webp"
poster_source="$output_directory/$output_stem-poster.png"
timed_source="$output_directory/$output_stem-timed.mp4"
timeline_source="$output_directory/$output_stem-timeline.mp4"
marker_directory=""

cleanup() {
  rm -f "$poster_source" "$timed_source" "$timeline_source"
  if [[ -n "$marker_directory" && -d "$marker_directory" ]]; then
    find "$marker_directory" -type f -delete
    rmdir "$marker_directory"
  fi
}
trap cleanup EXIT

render_source=$input_video
if [[ -n "$timeline" ]]; then
  timeline_filter=$(python3 "$script_directory/support_media_timing.py" timeline-filter "$timeline")

  ffmpeg -hide_banner -loglevel error -y \
    -i "$input_video" \
    -filter_complex "$timeline_filter" \
    -map "[timed]" \
    -an -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
    "$timeline_source"
  render_source=$timeline_source
fi

if [[ -n "$opening_image" ]]; then
  ffmpeg -hide_banner -loglevel error -y \
    -loop 1 -t "$opening_seconds" -i "$opening_image" \
    -i "$render_source" \
    -filter_complex "[0:v]fps=30,format=yuv420p[opening];[1:v]fps=30,format=yuv420p[body];[opening][body]concat=n=2:v=1:a=0[timed]" \
    -map "[timed]" \
    -an -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
    "$timed_source"
  render_source=$timed_source
fi

if [[ -n "$markers" ]]; then
  marker_directory=$(mktemp -d "${TMPDIR:-/tmp}/taxon-support-markers.XXXXXX")
  marker_inputs=(-i "$render_source")
  marker_filter="[0:v]fps=6,scale=402:-2:flags=lanczos[marked0]"
  marker_index=0
  marker_prefix=${opening_seconds:-0}
  marker_rows="$marker_directory/markers.tsv"
  python3 "$script_directory/support_media_timing.py" markers "$timeline" "$markers" \
    --prefix-seconds "$marker_prefix" > "$marker_rows"
  while IFS=$'\t' read -r marker_name marker_start marker_end center_x center_y radius_x radius_y stroke fill stroke_width; do
    marker_index=$((marker_index + 1))
    marker_image="$marker_directory/$marker_name.png"
    magick -size 402x874 xc:none \
      -stroke "$stroke" -strokewidth "$stroke_width" -fill "$fill" \
      -draw "ellipse $center_x,$center_y $radius_x,$radius_y 0,360" \
      "$marker_image"
    marker_inputs+=(-loop 1 -i "$marker_image")
    previous=$((marker_index - 1))
    marker_filter+=";[$marker_index:v]fps=6[overlay$marker_index];[marked$previous][overlay$marker_index]overlay=enable='between(t,$marker_start,$marker_end)':shortest=1:eof_action=pass[marked$marker_index]"
  done < "$marker_rows"
  marker_filter+=";[marked$marker_index]split[frames][palette_source];[palette_source]palettegen=max_colors=128:stats_mode=diff[palette];[frames][palette]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[gif]"
  ffmpeg -hide_banner -loglevel error -y \
    "${marker_inputs[@]}" \
    -filter_complex "$marker_filter" \
    -map "[gif]" -loop -1 \
    "$gif_output"
else
  ffmpeg -hide_banner -loglevel error -y \
    -i "$render_source" \
    -filter_complex "fps=6,scale=402:-2:flags=lanczos,split[frames][palette_source];[palette_source]palettegen=max_colors=128:stats_mode=diff[palette];[frames][palette]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle" \
    -loop -1 \
    "$gif_output"
fi

ffmpeg -hide_banner -loglevel error -y \
  -ss "$poster_seconds" \
  -i "$render_source" \
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
