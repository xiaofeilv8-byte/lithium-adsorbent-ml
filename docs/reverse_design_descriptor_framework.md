# Reverse Design Descriptor Framework for Lithium Adsorbents

## Purpose
This framework supports future ML analysis and inverse design of lithium recovery adsorbents. It is broader than the previous LDH-only review scope and includes Ti-based ion sieves, Mn-based ion sieves, LDH/aluminum-based adsorbents, ion-imprinted materials, organic ligand materials, MOF/COF systems, and composites.

## Material Descriptors
- material_family
- active phase
- metal composition
- Li vacancy / H exchange
- interlayer structure
- functional groups
- ligand type
- pore structure
- surface charge
- hydrophilicity
- stability indicators

## Solution-Environment Descriptors
- Li concentration
- Mg/Li ratio
- pH
- competing ions
- ionic strength
- brine type
- temperature

## Performance Targets
- Li capacity
- Li/Mg selectivity
- regeneration stability
- dissolution loss
- cycle retention

## Reverse Design Logic
1. Predict performance from material and solution descriptors.
2. Use feature importance / SHAP only after model validation to identify influential factors.
3. Screen combinations that may balance high capacity, high selectivity, and high stability.
4. Return to experimental design for synthesis feasibility and validation.

## Value for Ti-Based Lithium Adsorbent Research
- Enables comparison of Ti-based adsorbents with LDH, ion-imprinted polymers, Mn-based ion sieves, and organic ligand adsorbents.
- Provides data-driven reference for Ti-based modification directions, such as crystal phase, H/Li exchange, morphology, and dissolution/stability control.
- Supports doctoral work extending from literature review toward data-driven materials design.
