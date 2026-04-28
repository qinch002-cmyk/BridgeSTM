# BridgeSTM
BridgeSTM：A Low-Cost and Easy-to-Maintain Scanning Tunneling Microscope with a Flexure-Hinge Coarse-Approach Mechanism

V1.0
Introduction
The Scanning Tunneling Microscope (STM) is a crucial experimental instrument that achieves
atomic-scale surface imaging and material characterization by measuring the tunneling current
between a metal probe and a conductive sample. It finds extensive applications in condensed
matter physics, materials science, and nanotechnology research. However, commercial STM
systems are typically expensive, structurally complex, and demand high standards for operating
environments and maintenance levels. These factors have somewhat limited their adoption and
application in resource-constrained research settings and entry-level scientific platforms.
In recent years, research efforts, along with related patents and open-source designs, have
explored simplified mechanical structures and low-cost STM implementation strategies. These
projects demonstrate that low-cost nanoscale atomic imaging can be achieved through self-built
STMs featuring independently constructed circuits, customized mechanical designs, and
simplified piezoelectric scanners. Most projects have successfully scanned the standard STM
sample HOPG and obtained high-quality atomic images. This preliminary research provides a
crucial foundation for the feasibility of constructing structurally simplified STM systems.
However, existing designs still commonly face the following issues: First, coarse-approach
mechanisms are structurally complex, requiring significant time for maintenance or relying on
inefficient manual operation. Second, the cost of building a system remains relatively high for
most departments with limited budgets. Third, most STM designs, particularly mechanical
components, experience frequent friction during operation, leading to noticeable vibrations and
thermal expansion effects at the microscopic level.

This research builds upon my first STM prototype system (sixth-generation design). The current
system has achieved: (1) A coarse-approach mechanism based on a bridge-type flexible hinge
structure, enabling the probe to gradually approach the sample surface; (2) A 1/4-quadrant
piezoelectric scanning actuator providing micro-displacement drive in a single direction; (3)
Application of a controlled 0-3V bias voltage to the metal sample stage. However, the system
lacks completed tunnel current detection and closed-loop feedback circuitry, and critical
experimental data (e.g., I–Z characteristic curves) remain unobtained. Its stability and
repeatability require systematic evaluation.

This project aims to integrate and experimentally characterize the flexible hinge coarse-drive
mechanism and embedded electronic control system through engineering integration and
experimental characterization, building upon prior research and relevant design concepts while
incorporating numerous patents and solutions. The goal is to upgrade the existing engineering
prototype into an STM system with basic experimental capabilities. The research focuses on
constructing a simplified, maintainable STM architecture with stable operational capabilities.
Through experimental measurements, it will validate the feasibility of this architecture for
tunneling current detection and displacement control, thereby providing a reference for designing
simplified scanning probe instrument systems.

[1]Chen, Wei, et al. “A Novel Bridge-Type Compliant Displacement Amplification Mechanism
under Compound Loads Based on the Topology Optimisation of Flexure Hinge and Its
Application in Micro-Force Sensing.” Smart Materials and Structures, vol. 33, no. 1, 2024,
article 015020, doi:10.1088/1361-665X/aaf1316.

[2]Lavanya, S. B., and G. R. Jayanth. “Modeling and Optimal Design of Bridge-Type
Displacement Amplifier.” Recent Advances in Machines and Mechanisms, edited by V . K. Gupta
et al., Springer, 2023, pp. 117–124. doi:10.1007/978-981-19-3716-3_9.

[3]Slusher, Richard B. Motion Reducing Flexure Structure. U.S. Patent No. 5,969,892, U.S.
Patent and Trademark Office, 19 Oct. 1999.

[4]Warden, R. M. “Cryogenic Nano-Actuator for JWST.” Proceedings of the 38th Aerospace
Mechanisms Symposium, NASA Langley Research Center, 2006, pp. 239–252.

[5]Wei, H., et al. “Development of Piezo-Driven Compliant Bridge Mechanisms: General
Analytical Equations and Optimization of Displacement Amplification.” Micromachines, vol. 8,
no. 8, 2017, article 238, doi:10.3390/mi8080238.

[6]Yong, Yuen Kuan, et al. “High-Speed Flexure-Guided Nanopositioning: Mechanical Design
and Control Issues.” Review of Scientific Instruments, vol. 83, no. 12, 2012, article 121101,
doi:10.1063/1.4765048.

Updated:
# BridgeSTM V2.0

BridgeSTM V2 is the second-stage development of my low-cost educational scanning tunneling microscope project. This version focuses on upgrading the system from a basic actuator-and-bias prototype into a documented closed-loop STM development platform.

## V2 Update Overview

BridgeSTM V1 verified several basic subsystems:

- sample bias output around 3V;
- single-quadrant piezo actuation;
- coarse motor control;
- early hardware control experiments.

However, V1 did not include the core closed-loop STM chain. BridgeSTM V2 is designed to fill that gap.

The main V2 updates include:

- building a tunneling current measurement path;
- designing and testing a transimpedance amplifier, or TIA;
- adding ADC-based current and voltage logging;
- developing a Z-axis feedback simulation;
- preparing firmware for constant-current feedback control;
- organizing motor coarse approach into a safer state-machine structure;
- separating X, Y, and Z piezo control concepts;
- designing a new mechanical structure with a future Z-axis thermal drift compensation stage;
- documenting safety limits for bias, motor motion, Z command, and current threshold;
- creating daily engineering logs for hardware, firmware, software, and mechanical progress.

The key V2 control chain is:
sample bias
↓
tunneling current
↓
transimpedance amplifier
↓
ADC measurement
↓
Z feedback controller
↓
DAC output
↓
Z piezo actuation
