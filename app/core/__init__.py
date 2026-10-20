"""Design-neutral code behind the #REP app.

Copied from ui_variants/shared when design_01 became the app, so that app/
depends on nothing outside itself except the data and result files it reads.
It holds the property schema, copy, validation, the single model interface and
session state. Nothing in here decides how the app looks.
"""
