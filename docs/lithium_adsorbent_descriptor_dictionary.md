# Lithium Adsorbent Descriptor Dictionary

Each field must be extracted from full text, tables, figures, or SI. If unavailable, write `missing`; do not infer numeric values from abstracts.

| Field | Meaning | Suggested unit | Type | ML role | Notes |
|---|---|---|---|---|---|
| `record_id` | record id | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |
| `paper_id` | paper id | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |
| `title` | title | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |
| `year` | year | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |
| `journal` | journal | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |
| `DOI` | DOI | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |
| `material_name` | material name | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `material_family` | material family | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `material_subfamily` | material subfamily | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `active_phase` | active phase | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `support_or_matrix` | support or matrix | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `composite_component` | composite component | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `morphology` | morphology | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `particle_size` | particle size | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `granulated_or_powder` | granulated or powder | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `membrane_or_bead_or_powder` | membrane or bead or powder | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `Ti_based_or_not` | Ti based or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `Mn_based_or_not` | Mn based or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `Al_based_or_not` | Al based or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `LDH_or_not` | LDH or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `crystal_structure` | crystal structure | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `precursor_phase` | precursor phase | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `acid_treatment_or_not` | acid treatment or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `H_exchange_or_not` | H exchange or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `Li_extraction_method` | Li extraction method | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `calcination_temperature` | calcination temperature | deg C | numeric | input feature | Use `missing` when not explicitly available. |
| `interlayer_spacing` | interlayer spacing | nm or Angstrom | numeric | input feature | Use `missing` when not explicitly available. |
| `lattice_parameter` | lattice parameter | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `crystallinity_indicator` | crystallinity indicator | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `organic_material_or_not` | organic material or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `ion_imprinted_or_not` | ion imprinted or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `template_ion` | template ion | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `functional_monomer` | functional monomer | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `crosslinker` | crosslinker | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `ligand_or_binding_group` | ligand or binding group | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `polymer_matrix` | polymer matrix | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `porogen_or_solvent` | porogen or solvent | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `imprinting_factor` | imprinting factor | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `crown_ether_or_macrocycle_type` | crown ether or macrocycle type | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `functional_group_type` | functional group type | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `synthesis_method` | synthesis method | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `synthesis_pH` | synthesis pH | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `synthesis_temperature` | synthesis temperature | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `synthesis_time` | synthesis time | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `hydrothermal_temperature` | hydrothermal temperature | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `hydrothermal_time` | hydrothermal time | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `aging_time` | aging time | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `drying_temperature` | drying temperature | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `activation_method` | activation method | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `BET_surface_area` | BET surface area | m2/g | numeric | input feature | Use `missing` when not explicitly available. |
| `pore_volume` | pore volume | cm3/g | numeric | input feature | Use `missing` when not explicitly available. |
| `average_pore_size` | average pore size | nm | numeric | input feature | Use `missing` when not explicitly available. |
| `zeta_potential` | zeta potential | mV | numeric | input feature | Use `missing` when not explicitly available. |
| `pHpzc` | pHpzc | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `functional_group_density` | functional group density | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `ion_exchange_capacity` | ion exchange capacity | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `surface_OH_density` | surface OH density | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `water_contact_angle` | water contact angle | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `mechanical_stability_indicator` | mechanical stability indicator | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `Li_initial_concentration` | Li initial concentration | mg/L or mmol/L | numeric | input feature | Use `missing` when not explicitly available. |
| `adsorbent_dosage` | adsorbent dosage | g/L or g | numeric | input feature | Use `missing` when not explicitly available. |
| `solution_pH` | solution pH | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `temperature` | temperature | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `contact_time` | contact time | min or h | numeric | input feature | Use `missing` when not explicitly available. |
| `liquid_solid_ratio` | liquid solid ratio | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `ionic_strength` | ionic strength | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `real_brine_or_synthetic_solution` | real brine or synthetic solution | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `brine_type` | brine type | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `Mg_Li_ratio` | Mg Li ratio | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `Na_Li_ratio` | Na Li ratio | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `K_Li_ratio` | K Li ratio | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `Ca_Li_ratio` | Ca Li ratio | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `coexisting_ions` | coexisting ions | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `boron_present_or_not` | boron present or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `sulfate_present_or_not` | sulfate present or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `carbonate_present_or_not` | carbonate present or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `silica_present_or_not` | silica present or not | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `Li_adsorption_capacity_qe` | Li adsorption capacity qe | mg/g or mmol/g | numeric | output target | Use `missing` when not explicitly available. |
| `Li_maximum_capacity_Qmax` | Li maximum capacity Qmax | mg/g or mmol/g | numeric | output target | Use `missing` when not explicitly available. |
| `Li_removal_efficiency` | Li removal efficiency | % | numeric | output target | Use `missing` when not explicitly available. |
| `distribution_coefficient_Kd` | distribution coefficient Kd | mL/g | numeric | output target | Use `missing` when not explicitly available. |
| `Li_Mg_separation_factor` | Li Mg separation factor | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `Li_Na_separation_factor` | Li Na separation factor | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `Li_K_separation_factor` | Li K separation factor | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `Li_Ca_separation_factor` | Li Ca separation factor | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `selectivity_coefficient` | selectivity coefficient | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `equilibrium_time` | equilibrium time | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `kinetic_model` | kinetic model | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `isotherm_model` | isotherm model | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `regeneration_method` | regeneration method | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `desorption_agent` | desorption agent | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `cycle_number` | cycle number | as reported / not applicable | numeric | input feature | Use `missing` when not explicitly available. |
| `capacity_retention` | capacity retention | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `dissolution_loss` | dissolution loss | as reported / not applicable | numeric | output target | Use `missing` when not explicitly available. |
| `structural_stability_after_cycles` | structural stability after cycles | as reported / not applicable | categorical/text | output target | Use `missing` when not explicitly available. |
| `possible_ML_task` | possible ML task | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `suggested_target_property` | suggested target property | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `feature_completeness_level` | feature completeness level | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `data_quality_level` | data quality level | as reported / not applicable | categorical/text | input feature | Use `missing` when not explicitly available. |
| `extraction_source` | extraction source | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |
| `notes` | notes | as reported / not applicable | categorical/text | metadata | Use `missing` when not explicitly available. |