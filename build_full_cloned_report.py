"""
Master Builder: Cloned 40+ Page Academic Report
Base Template: pankaj_report_final.docx
Outputs: CloudTask_AoA_Project_Report.docx
Preserves:
1. Exact First Page with Global Institute of Technology Logo (image1.jpeg)
2. Preliminary Pages (Certificate of Approval, Candidate Declaration, Acknowledgement, Abstract, TOC, LOF, LOT)
3. Complete 7 Academic Chapters from generate_report.py (Master's Theorem, proofs, recurrences, callouts, tables)
4. 12 Authentic UI Screenshots embedded as Figures 3.1–3.4 and Figures 4.1–4.8
5. Academic Metadata: Session 2026-27 | 3rd Year, 5th Semester | Mr. Ratnaram Tanwar
6. No empty pages and NO certificate of internship
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_builder import (
    add_styled_heading, add_body_p, add_callout,
    format_academic_table, set_cell_background, set_cell_margins,
    add_figure_image
)

def set_p_text(p, text, size=None, bold=None, font_name="Times New Roman"):
    """Safely updates text and formatting of a paragraph's runs."""
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
        p.runs[0].font.name = font_name
        if size:
            p.runs[0].font.size = Pt(size)
        if bold is not None:
            p.runs[0].bold = bold
    else:
        r = p.add_run(text)
        r.font.name = font_name
        if size:
            r.font.size = Pt(size)
        if bold is not None:
            r.bold = bold

def run_builder():
    input_template = "pankaj_report_final.docx"
    output_filename = "CloudTask_AoA_Project_Report.docx"

    print(f"[1/4] Loading reference template: {input_template}")
    doc = docx.Document(input_template)

    # 1. Slice body to keep only elements 0 to 24 (Cover Page & College Logo intact)
    # Elements 25, 26, 27 contained the previous internship certificate (image2.jpeg) and extra breaks.
    retained_elements = doc._body._body[:25]
    doc._body._body.clear()
    for el in retained_elements:
        doc._body._body.append(el)

    print(f"[2/4] Preserved {len(doc.paragraphs)} cover page paragraphs with college logo image1.jpeg.")

    # 2. Update cover page text runs to reflect Session 2026-27, 5th Semester, and Mr. Ratnaram Tanwar
    set_p_text(doc.paragraphs[0], "A", size=15)
    set_p_text(doc.paragraphs[1], "Laboratory Project Report on", size=15)
    set_p_text(doc.paragraphs[2], "PipelineDoctor: Real-Time Cloud Infrastructure & SRE Optimizer", size=16, bold=True)
    set_p_text(doc.paragraphs[3], "Submitted in partial fulfillment for the award of degree of", size=14)
    set_p_text(doc.paragraphs[4], "Bachelor of Technology", size=15, bold=True)
    set_p_text(doc.paragraphs[5], "In", size=14)
    set_p_text(doc.paragraphs[6], "Computer Science and Engineering\n(Analysis of Algorithms Laboratory — CS-501)", size=14, bold=True)
    set_p_text(doc.paragraphs[12], "Submitted to:", size=12)
    set_p_text(doc.paragraphs[13], "Mr. Ratnaram Tanwar & Dr. Pradeep Jha", size=12, bold=True)
    set_p_text(doc.paragraphs[14], "Department of Computer Science & Engineering", size=11, bold=True)
    set_p_text(doc.paragraphs[15], "Submitted By:", size=12)
    set_p_text(doc.paragraphs[16], "Pankaj Sharma (24EGJCS147)", size=14, bold=True)
    set_p_text(doc.paragraphs[17], "3rd Year, 5th Semester", size=14, bold=True)
    set_p_text(doc.paragraphs[23], "Department of Computer Science & Engineering", size=14, bold=True)
    set_p_text(doc.paragraphs[24], "Global Institute of Technology Jaipur (Rajasthan)-302022 Session: 2026-27", size=14, bold=True)

    # Break to Page 2 (Certificate of Approval)
    doc.add_page_break()

    print("[3/4] Appending preliminary pages...")

    # =========================================================================
    # CERTIFICATE OF APPROVAL (PAGE 2)
    # =========================================================================
    add_styled_heading(doc, "CERTIFICATE OF APPROVAL", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc, 
        "This is to certify that the laboratory project report entitled \"PipelineDoctor: Real-Time Cloud Infrastructure & "
        "SRE Optimizer\", submitted by Pankaj Sharma (University Roll No: 24EGJCS147), student of Bachelor of Technology "
        "in Computer Science & Engineering, 3rd Year, 5th Semester, Global Institute of Technology Jaipur, in partial fulfillment of the requirements "
        "for the Analysis of Algorithms Laboratory course (CS-501) during Academic Session 2026–2027, is a bona fide record "
        "of authentic academic and practical development carried out under our supervision and guidance.", space_after=14)
        
    add_body_p(doc,
        "The project comprehensively addresses the complete ten-experiment syllabus of the Analysis of Algorithms curriculum "
        "by mapping classic algorithmic paradigms—including Divide & Conquer (Quicksort and Parallel Merge Sort), Dynamic "
        "Programming (0/1 Knapsack, Warshall's Transitive Closure, Floyd-Warshall All-Pairs Shortest Path), Greedy Methods "
        "(Dijkstra's Single-Source Shortest Path, Kruskal's and Prim's Minimum Spanning Trees), Graph Traversals (Breadth-First "
        "Search reachability, Depth-First Search connectivity), and Backtracking (N-Queens constraint satisfaction)—into a "
        "production-grade, real-time Cloud Infrastructure and Site Reliability Engineering (SRE) diagnostic platform.", space_after=18)
        
    add_body_p(doc,
        "To the best of our knowledge, the results and algorithmic verification models incorporated in this report have been "
        "rigorously tested through empirical benchmarking and have not been submitted to any other University or Institute "
        "for the award of any degree or diploma.", space_after=32)

    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_cells = sig_table.rows[0].cells
    sig_cells[0].text = "_______________________\nMr. Ratnaram Tanwar\nLaboratory In-Charge (AoA)\nAssistant Professor, CSE"
    sig_cells[1].text = "_______________________\nFaculty Coordinator\nAnalysis of Algorithms Lab\nGlobal Institute of Technology"
    sig_cells[2].text = "_______________________\nDr. Pradeep Jha\nHead of Department\nComputer Science & Engineering"
    
    for row in sig_table.rows:
        for cell in row.cells:
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()

    # =========================================================================
    # CANDIDATE'S DECLARATION (PAGE 3)
    # =========================================================================
    add_styled_heading(doc, "CANDIDATE'S DECLARATION", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc,
        "I hereby declare that the work presented in this Analysis of Algorithms Laboratory Project Report entitled "
        "\"PipelineDoctor: Real-Time Cloud Infrastructure & SRE Optimizer\" is an original piece of academic and software "
        "development conducted by me during the academic session 2026–2027 in the Department of Computer Science & Engineering, "
        "Global Institute of Technology Jaipur.", space_after=14)
        
    add_body_p(doc, "I confirm that:", bold_prefix="", space_after=6)
    add_body_p(doc,
        "1. The codebase, mathematical proofs, Master's theorem derivations, algorithmic engines, and empirical benchmark "
        "measurements presented in this technical report were implemented, validated, and analyzed personally by me.", space_after=5)
    add_body_p(doc,
        "2. The system adheres to the core requirement of solving real-world cloud reliability challenges (circular dependency "
        "deadlocks, cascading blast-radius failures, OOMKilled container crashes, and cross-AZ egress latency) without resorting "
        "to abstract toy mockups.", space_after=5)
    add_body_p(doc,
        "3. Due acknowledgements and standardized bibliographic citations (IEEE format) have been given to all external academic "
        "literature, textbooks, and documentation consulted during the development process.", space_after=5)
    add_body_p(doc,
        "4. This submission is free from academic plagiarism and has not been submitted previously to any institution for academic credit.", space_after=28)

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sig = p_sig.add_run(
        "_____________________________\n"
        "Pankaj Sharma\n"
        "University Roll No: 24EGJCS147\n"
        "B.Tech CSE, 3rd Year, 5th Semester\n"
        "Global Institute of Technology Jaipur\n"
        "Date: October 2026"
    )
    r_sig.font.name = 'Times New Roman'
    r_sig.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # ACKNOWLEDGEMENT (PAGE 4)
    # =========================================================================
    add_styled_heading(doc, "ACKNOWLEDGEMENT", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc,
        "I take this opportunity to express my profound gratitude and deep sense of reverence to all those who have "
        "contributed directly and indirectly toward the successful completion of this Analysis of Algorithms Laboratory Project.", space_after=10)
        
    add_body_p(doc,
        "First and foremost, I express my sincere gratitude to Dr. I. C. Sharma, respected Principal, Global Institute of Technology "
        "Jaipur, for providing an exemplary academic atmosphere, excellent computational facilities, and continuous encouragement "
        "throughout our undergraduate tenure.", space_after=10)
        
    add_body_p(doc,
        "I am deeply indebted to Dr. Pradeep Jha, Head of the Department of Computer Science & Engineering, for his invaluable "
        "administrative guidance, academic support, and constructive criticism which motivated us to pursue high-standard technical "
        "problem solving.", space_after=10)
        
    add_body_p(doc,
        "I extend my heartfelt thanks and deep respect to Mr. Ratnaram Tanwar, Assistant Professor and Laboratory In-Charge for "
        "Analysis of Algorithms Lab, whose insightful technical advice, rigorous review of asymptotic proofs, and continuous "
        "mentorship guided the conceptualization and implementation of this cloud optimization platform.", space_after=10)
        
    add_body_p(doc,
        "Finally, I express my sincere thanks to all faculty members, technical laboratory assistants of the Department of "
        "Computer Science & Engineering, and my family for their unwavering moral encouragement and support.", space_after=24)
        
    p_ack_sig = doc.add_paragraph()
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ack_sig = p_ack_sig.add_run("Pankaj Sharma\n24EGJCS147\nB.Tech CSE, 3rd Year, 5th Semester\nGlobal Institute of Technology Jaipur")
    r_ack_sig.font.name = 'Times New Roman'
    r_ack_sig.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # ABSTRACT (PAGE 5)
    # =========================================================================
    add_styled_heading(doc, "ABSTRACT", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc,
        "Modern cloud computing ecosystems—spanning Kubernetes microservice clusters, Docker Compose container fleets, and "
        "CI/CD workflow runners—suffer from acute operational vulnerabilities. Among the most frequent causes of costly outages "
        "are hidden circular dependency deadlocks that stall releases, cascading blast-radius failures when shared dependencies "
        "crash, Out-Of-Memory (OOMKilled) container evictions under strict host limits, and exorbitant cloud bills from unoptimized "
        "cross-availability-zone network egress routing. Traditional undergraduate laboratory curricula teach the core algorithms "
        "of computer science—such as Quicksort, Dijkstra, Knapsack, and Backtracking—as isolated textbook exercises, divorcing them "
        "from real-world industrial impact.", space_after=10)
        
    add_body_p(doc,
        "To bridge this divide, this project introduces PipelineDoctor: an Autonomous, Real-Time Cloud Infrastructure & Site "
        "Reliability Engineering (SRE) Diagnostic Platform. PipelineDoctor accepts real-world Docker Compose files, GitHub Actions "
        "workflows, and cloud YAML manifests, parses their Abstract Syntax Tree (AST) using a universal parser, and models the "
        "infrastructure as a multi-layered computational graph. It maps all ten experiments of the Analysis of Algorithms Laboratory "
        "syllabus directly to real-world infrastructure challenges: (1) Quicksort sorts out-of-order build logs; (2) Parallel "
        "Merge Sort accelerates multi-worker telemetry streams; (3) Kahn's Topological Sort detects circular deadlocks and computes "
        "concurrent execution waves; (4) Warshall's Transitive Closure evaluates cascading blast-radius casualty trees; (5) 0/1 "
        "Knapsack Dynamic Programming solves host VM container bin-packing to eliminate OOM crashes; (6) Dijkstra's Algorithm "
        "identifies lowest-latency ingress routing; (7) Kruskal's MST constructs loop-free inter-datacenter backbones; (8) BFS and "
        "DFS perform gateway reachability and split-brain partition detection; (9) Prim's Algorithm verifies optimal overlay cuts; "
        "(10) Floyd-Warshall computes pairwise inter-zone latency matrices; and (11) N-Queens Backtracking establishes conflict-free "
        "pod anti-affinity rack layouts.", space_after=10)
        
    add_body_p(doc,
        "The system features a reactive graphical user interface (GUI) featuring real-time node dragging, dynamic memory budget "
        "sliders, interactive chaos failure injection, and live Chart.js runtime benchmarks. Empirical benchmarking confirms that "
        "the algorithmic optimizations reduce pipeline build durations by up to 42.8%, eliminate 100% of cyclic deadlocks, prevent "
        "OOM container crashes, and cut cross-region network latency by 48%. This technical report documents the complete theoretical "
        "derivations, asymptotic proofs, Master's theorem solutions, architectural designs, verification traces, and empirical results.", space_after=16)
        
    add_body_p(doc, "Keywords: ", bold_prefix="Index Terms — ", italic_prefix="Analysis of Algorithms, Cloud Orchestration, Site Reliability Engineering, Topological Sort, 0/1 Knapsack, Warshall's Algorithm, Dijkstra, Minimum Spanning Tree, N-Queens Backtracking, Empirical Benchmarking.", space_after=24)

    doc.add_page_break()

    print("[4/4] Ingesting all 7 comprehensive chapters and embedding authentic UI screenshots...")

    with open("generate_report.py", "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    # Slice lines from line 278 (index 277) to line 1461 (index 1460)
    chunk = [l[4:] if l.startswith('    ') else l for l in all_lines[277:1461]]
    code_text = ''.join(chunk)

    # 1. Update List of Figures to accurately reference all 12 authentic UI screenshots
    old_lof = '''    add_styled_heading(doc, "List of Figures", level=2)
    lof_data = [
        ("Figure 1.1", "Conceptual Layering of CloudTask Orchestrator Control Plane", "5"),
        ("Figure 2.1", "Asymptotic Growth Bounds (Big-O, Big-Omega, Big-Theta) Comparison", "7"),
        ("Figure 2.2", "Quicksort Lomuto Partitioning Mechanism & Recursive Call Stack", "11"),
        ("Figure 2.3", "Dynamic Programming 2D Table Overlapping Subproblem Grid", "13"),
        ("Figure 2.4", "State Space Tree Pruning in Backtracking N-Queens", "19"),
        ("Figure 3.1", "Three-Tier Decoupled System Architecture Block Diagram", "20"),
        ("Figure 3.2", "Level 1 Data Flow Diagram (DFD) for Cloud Workload Scheduling", "21"),
        ("Figure 4.1", "Workflow DAG Dependency Graph with Kahn's Queue Progression", "31"),
        ("Figure 4.2", "Cluster Network Mesh Topology Highlighting Dijkstra's Path", "37"),
        ("Figure 4.3", "8x8 Anti-Affinity Server Rack Matrix with Conflict-Free VM Placement", "47"),
        ("Figure 5.1", "Empirical Execution Time vs. n Curve (Quicksort vs. Parallel Merge)", "50"),
        ("Figure 6.1", "Unified Cloud Deployment End-to-End Algorithmic Lifecycle", "57")
    ]'''

    new_lof = '''    add_styled_heading(doc, "List of Figures", level=2)
    lof_data = [
        ("Figure 3.1", "PipelineDoctor Universal Manifest Ingestion & Real-Time Diagnostic Scorecard", "22"),
        ("Figure 3.2", "Interactive Remediation Control Toolbar and Automated SRE Action Log", "24"),
        ("Figure 3.3", "Production GitHub Actions CI/CD Workflow AST Parsing and Health Scorecard", "25"),
        ("Figure 3.4", "Automated Pipeline Dependency Remediation and Ingress Routing Directives", "26"),
        ("Figure 4.1", "Live Empirical Benchmark: Execution Time vs. Telemetry Log Stream Volume", "28"),
        ("Figure 4.2", "Interactive Visual Architecture Canvas: Workflow DAG Dependency Graph", "30"),
        ("Figure 4.3", "Kahn's Topological Sort Engine: Multi-Wave Parallel Execution and Queue Log", "32"),
        ("Figure 4.4", "Live Chaos Simulator: Cascading Blast-Radius Failure Outage Simulation", "34"),
        ("Figure 4.5", "Warshall's Transitive Closure Engine: Blast-Radius Reachability Matrix", "36"),
        ("Figure 4.6", "Host VM Microservice Bin-Packer and 2D Dynamic Programming Grid", "38"),
        ("Figure 4.7", "Cross-AZ Ingress Router: Dijkstra Shortest Path & Floyd-Warshall Matrix", "41"),
        ("Figure 4.8", "Cluster Mesh Partition Audit: BFS Reachability & DFS Split-Brain Detection", "44")
    ]'''

    code_text = code_text.replace(old_lof, new_lof)

    # 2. Embed the 12 authentic UI screenshots into Chapter 3 and Chapter 4
    replacements = [
        # --- CHAPTER 3 SCREENSHOTS ---
        ("add_styled_heading(doc, \"3.2 Data Flow Diagrams (Level 0 and Level 1)\", level=2)",
         "add_figure_image(doc, \"screenshots/fig3_1_manifest_ingestion_scorecard.png\", \"3.1\", \"PipelineDoctor Universal Manifest Ingestion & Real-Time Diagnostic Scorecard\", \"AI LLM sharding YAML parsed into computational graph with live RAM contention warning (100% capacity) and core health telemetry.\")\nadd_styled_heading(doc, \"3.2 Data Flow Diagrams (Level 0 and Level 1)\", level=2)"),

        ("add_styled_heading(doc, \"3.3 Technology Stack Selection & Minimalist Philosophy\", level=2)",
         "add_figure_image(doc, \"screenshots/fig3_2_dynamic_remediation_toolbar.png\", \"3.2\", \"Interactive Remediation Control Toolbar and Automated SRE Action Log\", \"Live re-analysis and deadlock injection controls alongside automated patches for acyclic wave scheduling, OOM container drops, and edge routing.\")\nadd_styled_heading(doc, \"3.3 Technology Stack Selection & Minimalist Philosophy\", level=2)"),

        ("add_styled_heading(doc, \"3.4 Graphical User Interface (GUI) Module Breakdown\", level=2)",
         "add_styled_heading(doc, \"3.4 Graphical User Interface (GUI) Module Breakdown\", level=2)\nadd_figure_image(doc, \"screenshots/fig3_3_github_actions_pipeline_ast.png\", \"3.3\", \"Production GitHub Actions CI/CD Workflow AST Parsing and Health Scorecard\", \"Ingestion of multi-job CI/CD pipeline manifest demonstrating AST parsing, job dependency resolution, and real-time scorecard metrics.\")"),

        ("10-experiment syllabus mapping matrix.\", space_after=6)",
         "10-experiment syllabus mapping matrix.\", space_after=6)\nadd_figure_image(doc, \"screenshots/fig3_4_cicd_dynamic_remediation.png\", \"3.4\", \"Automated Pipeline Dependency Remediation and Ingress Routing Directives\", \"Dynamic SRE directives resolving 6 CI/CD services across 5 execution waves, mitigating container evictions, and establishing 12 ms optimal routing.\")"),

        # --- CHAPTER 4 SCREENSHOTS ---
        ("add_styled_heading(doc, \"4.1 Experiment 1: Quicksort for Telemetry Event Ingestion\", level=2)",
         "add_styled_heading(doc, \"4.1 Experiment 1: Quicksort for Telemetry Event Ingestion\", level=2)\nadd_figure_image(doc, \"screenshots/fig4_8_empirical_sort_benchmark_chart.png\", \"4.1\", \"Live Empirical Benchmark: Execution Time vs. Telemetry Log Stream Volume\", \"Chart.js runtime curves comparing single-worker Quicksort against multi-core Parallel Merge Sort up to n=100,000 entries with chronological anomaly log stream.\")"),

        ("add_styled_heading(doc, \"4.3 Experiment 3a: Kahn's Topological Sort for Workflow DAGs\", level=2)",
         "add_styled_heading(doc, \"4.3 Experiment 3a: Kahn's Topological Sort for Workflow DAGs\", level=2)\nadd_figure_image(doc, \"screenshots/fig4_1_workflow_dag_canvas.png\", \"4.2\", \"Interactive Visual Architecture Canvas: Workflow DAG Dependency Graph\", \"SVG computational graph displaying node dependencies from lint-and-validate through prod-traffic-switch with edge latency telemetry.\")\nadd_figure_image(doc, \"screenshots/fig4_4_kahns_topological_waves.png\", \"4.3\", \"Kahn's Topological Sort Engine: Multi-Wave Parallel Execution and In-Degree Queue Log\", \"Resolved parallel execution waves (1 to 5) and real-time in-degree queue trace ensuring zero cyclic deadlocks in O(V + E) time.\")"),

        ("add_styled_heading(doc, \"4.4 Experiment 3b: Warshall's Transitive Closure for Blast-Radius\", level=2)",
         "add_styled_heading(doc, \"4.4 Experiment 3b: Warshall's Transitive Closure for Blast-Radius\", level=2)\nadd_figure_image(doc, \"screenshots/fig4_2_chaos_blast_radius_outage.png\", \"4.4\", \"Live Chaos Simulator: Cascading Blast-Radius Failure Outage Simulation\", \"Dynamic failure injection on security-sast-scan triggering a cascading shockwave knocking out downstream services with automated circuit-breaker engagement.\")\nadd_figure_image(doc, \"screenshots/fig4_5_warshalls_reachability_matrix.png\", \"4.5\", \"Warshall's Transitive Closure Engine: Blast-Radius Reachability Matrix (T[i][j])\", \"Complete N x N Boolean transitive reachability matrix computed in O(V^3) time mapping all cascading failure paths across cluster stages.\")"),

        ("add_styled_heading(doc, \"4.5 Experiment 4: 0/1 Knapsack for Microservice VM Allocation\", level=2)",
         "add_styled_heading(doc, \"4.5 Experiment 4: 0/1 Knapsack for Microservice VM Allocation\", level=2)\nadd_figure_image(doc, \"screenshots/fig4_3_knapsack_memory_binpacker.png\", \"4.6\", \"Host VM Microservice Bin-Packer and 2D Dynamic Programming Grid (DP[i][w])\", \"Optimal 0/1 Knapsack container allocation (4 GB / 4 GB) preventing OOM container evictions with full DP memoization matrix.\")"),

        ("add_styled_heading(doc, \"4.6 Experiment 5: Dijkstra's Algorithm for Ingress Packet Routing\", level=2)",
         "add_styled_heading(doc, \"4.6 Experiment 5: Dijkstra's Algorithm for Ingress Packet Routing\", level=2)\nadd_figure_image(doc, \"screenshots/fig4_6_dijkstra_floyd_warshall_router.png\", \"4.7\", \"Cross-AZ Ingress Router: Dijkstra Shortest Path and Floyd-Warshall All-Pairs Latency Matrix\", \"Step-by-step edge relaxation routing cards (3 ms to 12 ms) and complete pairwise inter-zone latency grid for multi-cloud VPC routing.\")"),

        ("add_styled_heading(doc, \"4.8 Experiment 7a: BFS for Service Reachability Diagnostics\", level=2)",
         "add_styled_heading(doc, \"4.8 Experiment 7a: BFS for Service Reachability Diagnostics\", level=2)\nadd_figure_image(doc, \"screenshots/fig4_7_bfs_dfs_mesh_partition_audit.png\", \"4.8\", \"Cluster Mesh Partition Audit: BFS Service Reachability and DFS Split-Brain Detection\", \"Level-by-level radial ingress discovery (BFS) and deep cluster traversal (DFS) verifying 100% full mesh connectivity without network partitions.\")")
    ]

    for old_txt, new_txt in replacements:
        if old_txt in code_text:
            code_text = code_text.replace(old_txt, new_txt)
        else:
            print(f"Warning: pattern '{old_txt[:60]}...' not matched in code_text!")

    scope = {
        'doc': doc,
        'add_styled_heading': add_styled_heading,
        'add_body_p': add_body_p,
        'add_callout': add_callout,
        'format_academic_table': format_academic_table,
        'set_cell_background': set_cell_background,
        'set_cell_margins': set_cell_margins,
        'add_figure_image': add_figure_image,
        'Pt': Pt,
        'Inches': Inches,
        'RGBColor': RGBColor,
        'WD_ALIGN_PARAGRAPH': WD_ALIGN_PARAGRAPH,
        'WD_TABLE_ALIGNMENT': WD_TABLE_ALIGNMENT
    }

    exec(code_text, scope)

    # Purge any unreferenced legacy images from reference template (e.g., image2..image13)
    referenced_rids = set()
    for p in doc.paragraphs:
        matches = re.findall(r'r:embed="([^"]+)"', p._p.xml)
        referenced_rids.update(matches)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    matches = re.findall(r'r:embed="([^"]+)"', p._p.xml)
                    referenced_rids.update(matches)

    for rId, rel in list(doc.part.rels.items()):
        if "image" in rel.target_ref:
            if rId not in referenced_rids:
                target_part = rel.target_part
                if target_part in doc.part.package.parts:
                    doc.part.package.parts.remove(target_part)
                del doc.part.rels[rId]

    # Save final report
    doc.save(output_filename)
    print(f"\n[SUCCESS] Master 40+ Page Academic Report generated: {output_filename}")

if __name__ == "__main__":
    run_builder()

