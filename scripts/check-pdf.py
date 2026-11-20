#!/usr/bin/env python3
# SlidesTexTemplate - Copyright (C) 2026 Giulio Salvi
# GNU GPL version 3 or any later version; without warranty. See LICENSE.
# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify the example's PDF pages, frame counters and native transitions."""

import re
import sys
from pypdf import PdfReader


def check(path):
    pdf = PdfReader(path)
    expected_frames = [1, 2, 3, 3, 3, 4, 4, 5, 5, 6, 7, 8]
    expected_transitions = [
        '/Fade', '/Fade', '/Wipe', '/R', '/R', '/Dissolve',
        '/R', '/Push', '/R', '/Fade', '/Fade', '/Fade',
    ]
    assert len(pdf.pages) == len(expected_frames), (
        f'Expected 12 PDF pages for 8 frames, got {len(pdf.pages)}'
    )
    assert pdf.page_labels == [str(i) for i in range(1, 13)], (
        'PDF labels must count physical pages independently from frames'
    )
    for index, (page, frame, transition) in enumerate(
        zip(pdf.pages, expected_frames, expected_transitions), start=1
    ):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        assert abs(width / height - 16 / 9) < 0.01, 'Expected a 16:9 page'
        if frame != 1:
            text = page.extract_text()
            assert re.search(rf'\b{frame}\s*/\s*8\b', text), (
                f'Page {index} must show frame {frame} / 8'
            )
        actual = page.get('/Trans', {}).get('/S', '/R')
        assert actual == transition, (
            f'Page {index}: transition {actual}, expected {transition}'
        )
    print('PDF contract passed: 8 frames, 12 physical pages, stable overlay '
          'counters, physical page labels and per-frame transitions.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: check-pdf.py EXAMPLE.pdf')
    check(sys.argv[1])
