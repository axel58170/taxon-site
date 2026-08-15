import tempfile
import unittest
from pathlib import Path

from scripts.support_media_timing import TimingError, load_markers, load_timeline, timeline_filter


class SupportMediaTimingTests(unittest.TestCase):
    def csv(self, contents: str) -> Path:
        handle = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
        handle.write(contents)
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        return Path(handle.name)

    def timeline(self) -> Path:
        return self.csv(
            "phase,source_start,source_end,output_duration\n"
            "share-sheet,10,12,1\n"
            "result,14,18,2\n"
        )

    def test_timeline_records_output_offsets(self):
        phases = load_timeline(self.timeline())

        self.assertEqual(phases[0].output_start, 0)
        self.assertEqual(phases[1].output_start, 1)
        self.assertIn("split=2", timeline_filter(phases))
        self.assertIn("concat=n=2", timeline_filter(phases))

    def test_marker_must_fit_inside_named_phase(self):
        phases = load_timeline(self.timeline())
        markers = self.csv(
            "marker,phase,start,duration,center_x,center_y,radius_x,radius_y,stroke,fill,stroke_width\n"
            "taxon-tap,share-sheet,0.8,0.4,158,637,24,24,#b74b40,#b74b4030,3\n"
        )

        with self.assertRaisesRegex(TimingError, "extends beyond phase"):
            load_markers(markers, phases)

    def test_marker_rejects_unknown_phase(self):
        phases = load_timeline(self.timeline())
        markers = self.csv(
            "marker,phase,start,duration,center_x,center_y,radius_x,radius_y,stroke,fill,stroke_width\n"
            "taxon-tap,missing,0,0.3,158,637,24,24,#b74b40,#b74b4030,3\n"
        )

        with self.assertRaisesRegex(TimingError, "unknown phase"):
            load_markers(markers, phases)

    def test_timeline_rejects_non_finite_numbers(self):
        timeline = self.csv(
            "phase,source_start,source_end,output_duration\n"
            "result,0,inf,1\n"
        )

        with self.assertRaisesRegex(TimingError, "must be finite"):
            load_timeline(timeline)
