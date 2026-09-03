from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "scripts" / "build_site.py"
text = path.read_text(encoding="utf-8")
marker = "# ---- current v1.0 builder ----"
if marker not in text:
    raise SystemExit("current builder marker missing")
prefix, suffix = text.split(marker, 1)
old_group = "('Assessment & diagnosis', ['adult-adhd-assessment-england', 'adult-autism-assessment-england'])"
assessment_ids = [
    'adult-adhd-assessment-england', 'adult-autism-assessment-england',
    'adult-adhd-assessment-scotland', 'adult-autism-assessment-scotland',
    'adult-adhd-assessment-wales', 'adult-autism-assessment-wales',
    'adult-adhd-assessment-northern-ireland', 'adult-autism-assessment-northern-ireland',
    'child-adhd-assessment-england', 'child-autism-assessment-england',
    'child-adhd-assessment-scotland', 'child-autism-assessment-scotland',
    'child-adhd-assessment-wales', 'child-autism-assessment-wales',
    'child-adhd-assessment-northern-ireland', 'child-autism-assessment-northern-ireland',
    'private-autism-adhd-assessment-uk', 'waiting-for-autism-adhd-assessment-uk',
    'assessment-refused-or-disagree-uk', 'after-autism-adhd-assessment-uk',
    'assessment-communication-sensory-adjustments-uk',
    'co-occurring-autism-adhd-assessment-uk', 'other-neurodevelopmental-assessments-uk',
]
new_group = "('Assessment & diagnosis', [" + ", ".join(repr(item) for item in assessment_ids) + "])"
if old_group not in suffix:
    raise SystemExit("current Assessment question group not found")
suffix = suffix.replace(old_group, new_group, 1)
if "V10_ROUTE_COUNT = 238" not in suffix:
    raise SystemExit("V10 route count anchor missing")
suffix = suffix.replace("V10_ROUTE_COUNT = 238", "V10_ROUTE_COUNT = 274", 1)
if "_compat09__V09_ROUTE_COUNT = 176" not in suffix:
    raise SystemExit("current pre-Evidence route count anchor missing")
suffix = suffix.replace("_compat09__V09_ROUTE_COUNT = 176", "_compat09__V09_ROUTE_COUNT = 212", 1)
path.write_text(prefix + marker + suffix, encoding="utf-8")

# Remove the one-shot mutation machinery from the candidate tree.
(root / "scripts" / "_patch_assessment_builder_once.py").unlink(missing_ok=True)
(root / ".github" / "workflows" / "assessment-builder-one-shot.yml").unlink(missing_ok=True)
