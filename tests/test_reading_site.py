from copy import deepcopy
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import make_site
from build_sota import rank_best


class ReadingSiteTests(unittest.TestCase):
    def test_publication_and_collection_use_seven_calendar_days(self):
        paper = yaml.safe_load((make_site.ITEMS / "papers/2606.20847.yaml").read_text())
        items = []
        for day in ["2025-12-25", "2025-12-26", "2026-01-01", "2026-01-02"]:
            item = deepcopy(paper)
            item["time"] = {"published": day, "collected": "2026-01-01"}
            items.append(item)
        with TemporaryDirectory() as directory, patch.object(make_site, "ROOT", Path(directory)):
            kb = Path(directory) / "kb"
            kb.mkdir()
            (kb / "timeline.yaml").write_text("facts: []")
            data = make_site.build_data(items, date(2026, 1, 1))
        self.assertEqual(data["cutoff"], "2025-12-26")
        self.assertEqual((data["stats"]["week"], data["stats"]["collected"]), (2, 4))

    def test_best_requires_known_direction_and_identical_complete_conditions(self):
        protocol = dict(dataset="CTC B", anchor="fixed QP", unit="%", setup="VVenC 1.7.0 RA faster",
                        basis="YUV-PSNR", statistic="class mean")
        for name, expected in [("BD-Rate", 0), ("码率节省", 4), ("未知指标", None)]:
            entries = [{"value": v, "conditions": dict(protocol, metric=name)} for v in (4, 0, 4)]
            self.assertEqual(rank_best(entries, name), expected)
            entries[1]["conditions"]["statistic"] = "peak"
            self.assertIsNone(rank_best(entries, name))
            for entry in entries:
                entry["conditions"].pop("basis")
                entry["conditions"]["statistic"] = "class mean"
            self.assertIsNone(rank_best(entries, name))
