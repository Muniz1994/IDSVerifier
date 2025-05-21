import streamlit as st
import ifcopenshell
from ifctester import ids, reporter
from io import StringIO
from report import render_validation_report

# Read IFC file
ifc_file = ifcopenshell.open("testfiles/CursoBIM.Municipios.ModeloComInfo.Georref-IFC4X3.ifc")


ids_obj = ids.open("testfiles/Licenciamento.ids")


results = ids_obj.validate(ifc_file)

report = reporter.Json(ids_obj).report()

print(report)