import streamlit as st
from datetime import datetime
import pandas as pd

def render_validation_report(report):
    st.title("🧪 IDS Validation Report")
    
    # Report Metadata
    st.subheader("📋 Summary")
    st.write(f"**Title:** {report.get('title', 'N/A')}")
    st.write(f"**Date:** {datetime.strptime(report.get('date'), '%Y-%m-%d %H:%M:%S')}")
    
    for spec in report["specifications"]:
        with st.expander(f"📌 {spec['name']} - {'✅ Passed' if spec['status'] else '❌ Failed'}"):
            st.markdown(f"- **Description:** {spec['description'] or '*No description*'}")
            st.markdown(f"- **Instructions:** {spec['instructions'] or '*No instructions*'}")
            st.markdown(f"- **Applicable To:** `{', '.join(spec['applicability'])}`")
            st.markdown(
                f"- **Checks Passed:** {spec['total_checks_pass']} / {spec['total_checks']} "
                f"({spec['percent_checks_pass']}%)"
            )
            
            st.subheader("📝 Requirements")
            for req in spec["requirements"]:
                status_emoji = "✅" if req["status"] else "❌"
                st.markdown(f"#### {status_emoji} Requirement: {req['label']}")
                st.markdown(f"**Description:** {req['description']}")
                st.markdown(f"- **Facet Type:** {req['facet_type']}")
                st.markdown(f"- **Cardinality:** `{req['metadata'].get('@cardinality', 'N/A')}`")
                st.markdown(f"- **Status:** {'Passed' if req['status'] else 'Failed'}")

                # Passed Entities
                if req.get("passed_entities"):
                    st.markdown(f"**✔️ Passed Entities ({len(req['passed_entities'])}):**")
                    passed_data = []
                    for e in req["passed_entities"]:
                        passed_data.append({
                            "Class": e.get("class", "N/A"),
                            "Name": e.get("name", "N/A"),
                            "Global ID": e.get("global_id", "N/A"),
                            "ID": e.get("id", "N/A")
                        })
                    st.dataframe(pd.DataFrame(passed_data))
                
                # Failed Entities
                if req.get("failed_entities"):
                    st.markdown(f"**❌ Failed Entities ({len(req['failed_entities'])}):**")
                    failed_data = []
                    for e in req["failed_entities"]:
                        # Handle both direct entity and nested 'element' cases
                        entity = e.get("element", e)
                        failed_data.append({
                            "Class": entity.is_a(),
                            "Name": entity.Name,
                            "Reason": e.get("reason", "N/A")
                        })
                    st.dataframe(pd.DataFrame(failed_data))
                
                st.markdown("---")  # Add a separator between requirements