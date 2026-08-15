import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "scripts" / "prepare_support_media.sh"


class PrepareSupportMediaTests(unittest.TestCase):
    def test_rejects_zero_opening_duration_before_rendering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mov"
            opening = root / "opening.png"
            timeline = root / "timeline.csv"
            source.touch()
            opening.touch()
            timeline.write_text(
                "phase,source_start,source_end,output_duration\nresult,0,1,1\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [str(SCRIPT), str(source), "sample", "0.5", str(root / "output"),
                 str(timeline), str(opening), "0"],
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Opening duration must be a positive number", result.stderr)

    @unittest.skipUnless(
        all(shutil.which(tool) for tool in ("ffmpeg", "ffprobe", "cwebp", "magick")),
        "support-media rendering tools are unavailable",
    )
    def test_propagates_invalid_marker_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mp4"
            opening = root / "opening.png"
            timeline = root / "timeline.csv"
            markers = root / "markers.csv"
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                 "-i", "color=size=402x874:rate=30:duration=1", str(source)],
                check=True,
            )
            subprocess.run(
                ["magick", "-size", "402x874", "xc:white", str(opening)],
                check=True,
            )
            timeline.write_text(
                "phase,source_start,source_end,output_duration\nresult,0,0.8,0.5\n",
                encoding="utf-8",
            )
            markers.write_text(
                "marker,phase,start,duration,center_x,center_y,radius_x,radius_y,stroke,fill,stroke_width\n"
                "translation,missing,0,0.2,200,300,20,20,#b74b40,#00000000,3\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [str(SCRIPT), str(source), "sample", "0.2", str(root / "output"),
                 str(timeline), str(opening), "0.2", str(markers)],
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown phase", result.stderr)
