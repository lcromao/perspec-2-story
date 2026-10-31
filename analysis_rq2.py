#!/usr/bin/env python3
"""Reconstruct RQ2 tables, preference charts, reports and recorded thematic draft.

Run from the repository: .venv/bin/python analysis_rq2.py
Use --output-dir for a separate reconstruction. No external API/model calls.
"""
from rq2.rebuild import main

if __name__=='__main__':
    main()
