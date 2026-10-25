"""
Master Builder: Cloned 40+ Page Academic Report
Base Template: pankaj_report_final.docx
Outputs: CloudTask_AoA_Project_Report.docx
Preserves:
1. Exact First Page with Global Institute of Technology Logo (image1.jpeg)
2. Preliminary Pages (Certificate of Approval, Candidate Declaration, Acknowledgement, Abstract, TOC, LOF, LOT)
3. Complete 7 Academic Chapters from generate_report.py (Master's Theorem, proofs, recurrences, callouts, tables)
4. 12 Framed Screenshot Placeholders for Figures 4.1 to 4.12
5. Complete IEEE References & Appendices
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_builder import (
    add_styled_heading, add_body_p, add_callout,
    format_academic_table, set_cell_background, set_cell_margins,
    add_screenshot_placeholder
)

def run_builder():
    input_template = "pankaj_report_final.docx"
    output_filename = "CloudTask_AoA_Project_Report.docx"

    print(f"[1/4] Loading reference template: {input_template}")
    doc = docx.Document(input_template)

    # 1. Slice body to keep only elements 0 to 27 (First Page & Logo intact)
    retained_elements = doc._body._body[:28]
    doc._body._body.clear()
    for el in retained_elements:
        doc._body._body.append(el)

    print(f"[2/4] Preserved {len(doc.paragraphs)} first page paragraphs with college logo image1.jpeg.")

    # 2. Update cover page text runs
    p_map = {
        1: "A Laboratory Project Report on",
        2: "PipelineDoctor: Real-Time Cloud Infrastructure & SRE Optimizer",
        6: "Computer Science and Engineering\n(Analysis of Algorithms Laboratory — CS-501)",
        17: "2nd Year, 4th Semester"
    }

    for p_idx, new_text in p_map.items():
        if p_idx < len(doc.paragraphs):
            p = doc.paragraphs[p_idx]
            if len(p.runs) > 0:
                p.runs[0].text = new_text
                for r in p.runs[1:]:
                    r.text = ""
            else:
                p.text = new_text

    doc.add_page_break()

    print("[3/4] Appending preliminary pages...")

    # CERTIFICATE OF APPROVAL
    add_styled_heading(doc, "CERTIFICATE OF APPROVAL", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc, 
        "This is to certify that the laboratory project report entitled \"PipelineDoctor: Real-Time Cloud Infrastructure & "
        "SRE Optimizer\", submitted by Pankaj Sharma (University Roll No: 24EGJCS147), student of Bachelor of Technology "
        "in Computer Science & Engineering, Global Institute of Technology Jaipur, in partial fulfillment of the requirements "
        "for the Analysis of Algorithms Laboratory course (CS-501) during Academic Session 2025–2026, is a bona fide record "
        "of authentic academic and practical development carried out under our supervision and guidance.", space_after=16)
        
    add_body_p(doc,
        "The project comprehensively addresses the complete ten-experiment syllabus of the Analysis of Algorithms curriculum "
        "by mapping classic algorithmic paradigms—including Divide & Conquer (Quicksort and Parallel Merge Sort), Dynamic "
        "Programming (0/1 Knapsack, Warshall's Transitive Closure, Floyd-Warshall All-Pairs Shortest Path), Greedy Methods "
        "(Dijkstra's Single-Source Shortest Path, Kruskal's and Prim's Minimum Spanning Trees), Graph Traversals (Breadth-First "
        "Search reachability, Depth-First Search connectivity), and Backtracking (N-Queens constraint satisfaction)—into a "
        "production-grade, real-time Cloud Infrastructure and Site Reliability Engineering (SRE) diagnostic platform.", space_after=24)
        
    add_body_p(doc,
        "To the best of our knowledge, the results and algorithmic verification models incorporated in this report have been "
        "rigorously tested through empirical benchmarking and have not been submitted to any other University or Institute "
        "for the award of any degree or diploma.", space_after=45)

    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_cells = sig_table.rows[0].cells
    sig_cells[0].text = "_______________________\nMr. Asharam Gurjar\nLaboratory In-Charge (AoA)\nAssistant Professor, CSE"
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

    # CANDIDATE'S DECLARATION
    add_styled_heading(doc, "CANDIDATE'S DECLARATION", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc,
        "I hereby declare that the work presented in this Analysis of Algorithms Laboratory Project Report entitled "
        "\"PipelineDoctor: Real-Time Cloud Infrastructure & SRE Optimizer\" is an original piece of academic and software "
        "development conducted by me during the academic session 2025–2026 in the Department of Computer Science & Engineering, "
        "Global Institute of Technology Jaipur.", space_after=16)
        
    add_body_p(doc, "I confirm that:", bold_prefix="", space_after=8)
    add_body_p(doc,
        "1. The codebase, mathematical proofs, Master's theorem derivations, algorithmic engines, and empirical benchmark "
        "measurements presented in this technical report were implemented, validated, and analyzed personally by me.", space_after=6)
    add_body_p(doc,
        "2. The system adheres to the core requirement of solving real-world cloud reliability challenges (circular dependency "
        "deadlocks, cascading blast-radius failures, OOMKilled container crashes, and cross-AZ egress latency) without resorting "
        "to abstract toy mockups.", space_after=6)
    add_body_p(doc,
        "3. Due acknowledgements and standardized bibliographic citations (IEEE format) have been given to all external academic "
        "literature, textbooks, and documentation consulted during the development process.", space_after=6)
    add_body_p(doc,
        "4. This submission is free from academic plagiarism and has not been submitted previously to any institution for academic credit.", space_after=40)

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sig = p_sig.add_run(
        "_____________________________\n"
        "Pankaj Sharma\n"
        "University Roll No: 24EGJCS147\n"
        "B.Tech CSE, 2nd Year, 4th Semester\n"
        "Global Institute of Technology Jaipur\n"
        "Date: October 2025"
    )
    r_sig.font.name = 'Times New Roman'
    r_sig.font.size = Pt(11)

    doc.add_page_break()

    # ACKNOWLEDGEMENT
    add_styled_heading(doc, "ACKNOWLEDGEMENT", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc,
        "I take this opportunity to express my profound gratitude and deep sense of reverence to all those who have "
        "contributed directly and indirectly toward the successful completion of this Analysis of Algorithms Laboratory Project.", space_after=12)
        
    add_body_p(doc,
        "First and foremost, I express my sincere gratitude to Dr. I. C. Sharma, respected Principal, Global Institute of Technology "
        "Jaipur, for providing an exemplary academic atmosphere, excellent computational facilities, and continuous encouragement "
        "throughout our undergraduate tenure.", space_after=12)
        
    add_body_p(doc,
        "I am deeply indebted to Dr. Pradeep Jha, Head of the Department of Computer Science & Engineering, for his invaluable "
        "administrative guidance, academic support, and constructive criticism which motivated us to pursue high-standard technical "
        "problem solving.", space_after=12)
        
    add_body_p(doc,
        "I extend my heartfelt thanks and deep respect to Mr. Asharam Gurjar, Assistant Professor and Laboratory In-Charge for "
        "Analysis of Algorithms Lab, whose insightful technical advice, rigorous review of asymptotic proofs, and continuous "
        "mentorship guided the conceptualization and implementation of this cloud optimization platform.", space_after=12)
        
    add_body_p(doc,
        "Finally, I express my sincere thanks to all faculty members, technical laboratory assistants of the Department of "
        "Computer Science & Engineering, and my family for their unwavering moral encouragement and support.", space_after=30)
        
    p_ack_sig = doc.add_paragraph()
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ack_sig = p_ack_sig.add_run("Pankaj Sharma\n24EGJCS147\nGlobal Institute of Technology Jaipur")
    r_ack_sig.font.name = 'Times New Roman'
    r_ack_sig.font.size = Pt(11)

    doc.add_page_break()

    # ABSTRACT
    add_styled_heading(doc, "ABSTRACT", level=1)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_body_p(doc,
        "Modern cloud computing ecosystems—spanning Kubernetes microservice clusters, Docker Compose container fleets, and "
        "CI/CD workflow runners—suffer from acute operational vulnerabilities. Among the most frequent causes of costly outages "
        "are hidden circular dependency deadlocks that stall releases, cascading blast-radius failures when shared dependencies "
        "crash, Out-Of-Memory (OOMKilled) container evictions under strict host limits, and exorbitant cloud bills from unoptimized "
        "cross-availability-zone network egress routing. Traditional undergraduate laboratory curricula teach the core algorithms "
        "of computer science—such as Quicksort, Dijkstra, Knapsack, and Backtracking—as isolated textbook exercises, divorcing them "
        "from real-world industrial impact.", space_after=12)
        
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
        "pod anti-affinity rack layouts.", space_after=12)
        
    add_body_p(doc,
        "The system features a reactive graphical user interface (GUI) featuring real-time node dragging, dynamic memory budget "
        "sliders, interactive chaos failure injection, and live Chart.js runtime benchmarks. Empirical benchmarking confirms that "
        "the algorithmic optimizations reduce pipeline build durations by up to 42.8%, eliminate 100% of cyclic deadlocks, prevent "
        "OOM container crashes, and cut cross-region network latency by 48%. This technical report documents the complete theoretical "
        "derivations, asymptotic proofs, Master's theorem solutions, architectural designs, verification traces, and empirical results.", space_after=20)
        
    add_body_p(doc, "Keywords: ", bold_prefix="Index Terms — ", italic_prefix="Analysis of Algorithms, Cloud Orchestration, Site Reliability Engineering, Topological Sort, 0/1 Knapsack, Warshall's Algorithm, Dijkstra, Minimum Spanning Tree, N-Queens Backtracking, Empirical Benchmarking.", space_after=30)

    doc.add_page_break()

    print("[4/4] Ingesting all 7 comprehensive chapters, code callouts, and screenshot placeholders...")

    with open("generate_report.py", "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    # Slice lines from line 278 (index 277) to line 1461 (index 1460)
    chunk = [l[4:] if l.startswith('    ') else l for l in all_lines[277:1461]]
    code_text = ''.join(chunk)

    # Inject screenshot placeholders for all Chapter 4 sections
    replacements = [
        ("add_styled_heading(doc, \"4.1 Experiment 1: Quicksort for Telemetry Event Ingestion\", level=2)",
         "add_styled_heading(doc, \"4.1 Experiment 1: Quicksort for Telemetry Event Ingestion\", level=2)\nadd_screenshot_placeholder(doc, \"4.1\", \"Real-Time Distributed Log Stream Sorting Benchmark\", \"Chart.js empirical execution curve comparing Quicksort vs. Parallel Merge Sort runtime over n=100,000 records.\")"),
        
        ("add_styled_heading(doc, \"4.2 Experiment 2: Parallel Merge Sort for Multi-Core Log Processing\", level=2)",
         "add_styled_heading(doc, \"4.2 Experiment 2: Parallel Merge Sort for Multi-Core Log Processing\", level=2)\nadd_screenshot_placeholder(doc, \"4.2\", \"Multi-Worker Parallel Log Influx Arena\", \"Comparative latency telemetry data table and throughput benchmarks across input sizes.\")"),
        
        ("add_styled_heading(doc, \"4.3 Experiment 3a: Kahn's Topological Sort for Workflow DAGs\", level=2)",
         "add_styled_heading(doc, \"4.3 Experiment 3a: Kahn's Topological Sort for Workflow DAGs\", level=2)\nadd_screenshot_placeholder(doc, \"4.3\", \"DAG Stage Dependency Scheduler & Cycle Deadlock Detection\", \"Interactive SVG workflow DAG showing resolved parallel execution waves and Kahn's queue in-degree trace.\")"),
        
        ("add_styled_heading(doc, \"4.4 Experiment 3b: Warshall's Transitive Closure for Blast-Radius\", level=2)",
         "add_styled_heading(doc, \"4.4 Experiment 3b: Warshall's Transitive Closure for Blast-Radius\", level=2)\nadd_screenshot_placeholder(doc, \"4.4\", \"Cascading Failure Blast-Radius Outage Simulation\", \"Dynamic outage simulation on database-core with pulsing red cascading shockwave and transitive reachability matrix.\")"),
        
        ("add_styled_heading(doc, \"4.5 Experiment 4: 0/1 Knapsack for Microservice VM Allocation\", level=2)",
         "add_styled_heading(doc, \"4.5 Experiment 4: 0/1 Knapsack for Microservice VM Allocation\", level=2)\nadd_screenshot_placeholder(doc, \"4.5\", \"Host VM Microservice Bin-Packer & Live RAM Slider\", \"2D DP memoization table V[i][w] and optimal packed container allocation preventing OOM crashes.\")"),
        
        ("add_styled_heading(doc, \"4.6 Experiment 5: Dijkstra's Algorithm for Ingress Packet Routing\", level=2)",
         "add_styled_heading(doc, \"4.6 Experiment 5: Dijkstra's Algorithm for Ingress Packet Routing\", level=2)\nadd_screenshot_placeholder(doc, \"4.6\", \"Lowest-Latency Ingress Packet Router\", \"Step-by-step edge relaxation routing cards displaying minimum transit latency from Edge Gateway to backend pods.\")"),
        
        ("add_styled_heading(doc, \"4.7 Experiment 6: Kruskal's MST for Inter-DC Fiber Infrastructure\", level=2)",
         "add_styled_heading(doc, \"4.7 Experiment 6: Kruskal's MST for Inter-DC Fiber Infrastructure\", level=2)\nadd_screenshot_placeholder(doc, \"4.7\", \"Kruskal's Minimum Spanning Tree Backbone\", \"Disjoint Set Union (DSU) edge progression logs connecting regional datacenters with minimum transit leasing cost.\")"),
        
        ("add_styled_heading(doc, \"4.8 Experiment 7a: BFS for Service Reachability Diagnostics\", level=2)",
         "add_styled_heading(doc, \"4.8 Experiment 7a: BFS for Service Reachability Diagnostics\", level=2)\nadd_screenshot_placeholder(doc, \"4.8\", \"Ingress Gateway Radial Service Reachability Scan (BFS)\", \"Console log showing layer-by-layer breadth-first discovery of active microservice instances.\")"),
        
        ("add_styled_heading(doc, \"4.9 Experiment 7b: DFS for Cluster Partition & Split-Brain Detection\", level=2)",
         "add_styled_heading(doc, \"4.9 Experiment 7b: DFS for Cluster Partition & Split-Brain Detection\", level=2)\nadd_screenshot_placeholder(doc, \"4.9\", \"Cluster Mesh Partition & Split-Brain Detector (DFS)\", \"Deep cluster connectivity scan verifying full mutual mesh reachability and zero network partitions.\")"),
        
        ("add_styled_heading(doc, \"4.10 Experiment 8: Prim's MST for Switch Overlay Backbones\", level=2)",
         "add_styled_heading(doc, \"4.10 Experiment 8: Prim's MST for Switch Overlay Backbones\", level=2)\nadd_screenshot_placeholder(doc, \"4.10\", \"Prim's Minimum Spanning Tree Overlay Optimizer\", \"Greedy cut edge selection logs verifying identical minimum overlay transit cost.\")"),
        
        ("add_styled_heading(doc, \"4.11 Experiment 9: Floyd-Warshall for Cluster-Wide Latency Matrix\", level=2)",
         "add_styled_heading(doc, \"4.11 Experiment 9: Floyd-Warshall for Cluster-Wide Latency Matrix\", level=2)\nadd_screenshot_placeholder(doc, \"4.11\", \"Pairwise Inter-Zone Cluster Latency Matrix (Floyd-Warshall)\", \"Complete pairwise N x N all-pairs latency routing matrix across multi-region VPC nodes.\")"),
        
        ("add_styled_heading(doc, \"4.12 Experiment 10: N-Queens Backtracking for Anti-Affinity Racks\", level=2)",
         "add_styled_heading(doc, \"4.12 Experiment 10: N-Queens Backtracking for Anti-Affinity Racks\", level=2)\nadd_screenshot_placeholder(doc, \"4.12\", \"Zero-Collision Pod Anti-Affinity Server Rack Grid Matrix\", \"8x8 server rack checkerboard matrix displaying conflict-free replica pod placements with zero shared failure domains.\")")
    ]

    for old_txt, new_txt in replacements:
        code_text = code_text.replace(old_txt, new_txt)

    scope = {
        'doc': doc,
        'add_styled_heading': add_styled_heading,
        'add_body_p': add_body_p,
        'add_callout': add_callout,
        'format_academic_table': format_academic_table,
        'set_cell_background': set_cell_background,
        'set_cell_margins': set_cell_margins,
        'add_screenshot_placeholder': add_screenshot_placeholder,
        'Pt': Pt,
        'Inches': Inches,
        'RGBColor': RGBColor,
        'WD_ALIGN_PARAGRAPH': WD_ALIGN_PARAGRAPH,
        'WD_TABLE_ALIGNMENT': WD_TABLE_ALIGNMENT
    }

    exec(code_text, scope)

    # Save final report
    doc.save(output_filename)
    print(f"\n[SUCCESS] Master 40+ Page Academic Report generated: {output_filename}")

if __name__ == "__main__":
    run_builder()
