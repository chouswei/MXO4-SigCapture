<!-- MemNet initial snap: MXO4 skill matrix (user + cursor + repo packs).
Anchor: TSK_mxo4_skill_matrix. Wire format: memnet-format.
Load: memnet query_warm(anchor="TSK_mxo4_skill_matrix", depth=2)
Fallback: read @TAG rows inside the memnet fence. -->

```memnet
@TSK: TSK_mxo4_skill_matrix|MXO4 SigCapture skill routing matrix|active|persistent
@SKG: SKG_mxo4|v0.2|repo:MXO4-SigCapture|persistent
@EDG: E_sm_01|TSK_mxo4_skill_matrix|owns|SKG_mxo4|skill_graph|persistent

@CLM: CLM_mat_hdr|type=pipe|domain|skill_id|pack|path|when|persistent
@IDX: IDX_skill_matrix|116|skill routing index|persistent
@SET: SET_skills_repo|SKL_rs_scpi|persistent
@SET: SET_skills_user|SKL_academic_report_generator,SKL_adr_generator,SKL_api_client_pattern,SKL_architecture_reviewer,SKL_bayesian_reasoner,SKL_causal_investigator,SKL_code_reviewer,SKL_commit_message_generator,SKL_control_theory_planner,SKL_decision_inverter,SKL_empirical_paradox_synthesis,SKL_engineering_practices_learner,SKL_entropy_reasoner,SKL_falsification_tester,SKL_file_operations,SKL_first_principle_thinker,SKL_game_theory_strategist,SKL_incentive_alignment_reviewer,SKL_inversion_thinker,SKL_knowledge_consolidator,SKL_launch_readiness_assessor,SKL_llm_model_suggester,SKL_markdown_preview_enhanced,SKL_markdown_viewer_user_pack,SKL_mcdm_decider,SKL_mcp_chrome_devtools,SKL_mcp_latex,SKL_mcp_memnet,SKL_mcp_novel_writer,SKL_mcp_sysml_v2,SKL_mcp_sysmledgraph,SKL_md_to_tex,SKL_mdtohtml,SKL_meeting_notes_generator,SKL_memnet_codebase_snap,SKL_memnet_format,SKL_mermaid,SKL_mermaid_doc_readability,SKL_mmdc,SKL_optimization_planner,SKL_pandas_expert,SKL_paradox_method,SKL_pcba_design_reviewer,SKL_pcba_netlist_reader,SKL_polarfire_soc_setup,SKL_pr_reviewer,SKL_pretty_mermaid,SKL_project_output_article,SKL_project_planner,SKL_reasoning_strategy_selector,SKL_rfc_generator,SKL_risk_assessor,SKL_scientific_method_first_principles,SKL_security_reviewer,SKL_skill_creator,SKL_skill_reviewer,SKL_skillfish,SKL_sysml_allocate_generator,SKL_sysml_behaviour_generator,SKL_sysml_common_file_scale,SKL_sysml_common_lib_contribution,SKL_sysml_common_library_naming,SKL_sysml_connections,SKL_sysml_eagle_netlist_bridge,SKL_sysml_eagle_netlist_parser_tool,SKL_sysml_hardware_part_generator,SKL_sysml_import_order_helper,SKL_sysml_interconnection_mermaid,SKL_sysml_item_generator,SKL_sysml_memnet_cache,SKL_sysml_memnet_documentation,SKL_sysml_modeling_session_checklist,SKL_sysml_modeling_workflow,SKL_sysml_nested_structure_modeling,SKL_sysml_new_project,SKL_sysml_part_reviewer,SKL_sysml_pcba_de_facto_alignment,SKL_sysml_physical_port_generator,SKL_sysml_refactorer,SKL_sysml_requirements_audit,SKL_sysml_requirements_generator,SKL_sysml_root_config,SKL_sysml_signal_processing_pipeline,SKL_sysml_software_part_generator,SKL_sysml_software_port_generator,SKL_sysml_stakeholder_use_case,SKL_sysml_traceability,SKL_sysml_v2_release_how_to_use,SKL_sysml_v2_syntax_reference,SKL_sysml_view_doc_sync,SKL_system_design_report_generator,SKL_tech_report_generator,SKL_tech_report_reviewer,SKL_toon_prompt_format,SKL_traceability_footprint_to_sysml,SKL_tron_format|persistent
@SET: SET_skills_cursor|SKL_automate,SKL_babysit,SKL_canvas,SKL_create_hook,SKL_create_rule,SKL_create_skill,SKL_create_subagent,SKL_loop,SKL_migrate_to_skills,SKL_onboard,SKL_review,SKL_review_bugbot,SKL_review_security,SKL_sdk,SKL_shell,SKL_split_to_prs,SKL_statusline,SKL_update_cli_config,SKL_update_cursor_settings|persistent
@EDG: E_sm_02|IDX_skill_matrix|indexes|SET_skills_repo|repo|persistent
@EDG: E_sm_03|IDX_skill_matrix|indexes|SET_skills_user|user|persistent
@EDG: E_sm_04|IDX_skill_matrix|indexes|SET_skills_cursor|cursor|persistent
@EDG: E_sm_05|IDX_skill_matrix|documents|CLM_mat_hdr|columns|persistent

@SKL: SKL_rs_scpi|repo|tool-wrapper|rs-scpi-scopes|rs-scpi|high|high|structural|.cursor/skills/rs-scpi-scopes/SKILL.md|persistent
@EDG: E_sm_06|SKG_mxo4|default_stack|SKL_rs_scpi|scpi_primary|persistent
@EDG: E_sm_07|SET_skills_repo|memberOf|SKL_rs_scpi|repo|persistent
@CLM: CLM_mat_001|rs-scpi|SKL_rs_scpi|repo|.cursor/skills/rs-scpi-scopes/SKILL.md|on trigger|persistent
@SKL: SKL_academic_report_generator|user|skill|academic-report-generator|doc|low|low|conceptual|~/.cursor/skills/academic-report-generator/SKILL.md|persistent
@CLM: CLM_mat_002|doc|SKL_academic_report_generator|user|academic-report-generator|on trigger|persistent
@SKL: SKL_adr_generator|user|skill|adr-generator|doc|low|low|conceptual|~/.cursor/skills/adr-generator/SKILL.md|persistent
@CLM: CLM_mat_003|doc|SKL_adr_generator|user|adr-generator|on trigger|persistent
@SKL: SKL_api_client_pattern|user|skill|api-client-pattern|meta|low|low|conceptual|~/.cursor/skills/api-client-pattern/SKILL.md|persistent
@CLM: CLM_mat_004|meta|SKL_api_client_pattern|user|api-client-pattern|on trigger|persistent
@SKL: SKL_architecture_reviewer|user|skill|architecture-reviewer|review|low|low|conceptual|~/.cursor/skills/architecture-reviewer/SKILL.md|persistent
@CLM: CLM_mat_005|review|SKL_architecture_reviewer|user|architecture-reviewer|on trigger|persistent
@SKL: SKL_bayesian_reasoner|user|skill|bayesian-reasoner|reasoning|low|low|conceptual|~/.cursor/skills/bayesian-reasoner/SKILL.md|persistent
@CLM: CLM_mat_006|reasoning|SKL_bayesian_reasoner|user|bayesian-reasoner|on trigger|persistent
@SKL: SKL_causal_investigator|user|skill|causal-investigator|reasoning|low|low|conceptual|~/.cursor/skills/causal-investigator/SKILL.md|persistent
@CLM: CLM_mat_007|reasoning|SKL_causal_investigator|user|causal-investigator|on trigger|persistent
@SKL: SKL_code_reviewer|user|skill|code-reviewer|review|low|low|conceptual|~/.cursor/skills/code-reviewer/SKILL.md|persistent
@CLM: CLM_mat_008|review|SKL_code_reviewer|user|code-reviewer|on trigger|persistent
@SKL: SKL_commit_message_generator|user|skill|commit-message-generator|git|low|low|conceptual|~/.cursor/skills/commit-message-generator/SKILL.md|persistent
@CLM: CLM_mat_009|git|SKL_commit_message_generator|user|commit-message-generator|on trigger|persistent
@SKL: SKL_control_theory_planner|user|skill|control-theory-planner|reasoning|low|low|conceptual|~/.cursor/skills/control-theory-planner/SKILL.md|persistent
@CLM: CLM_mat_010|reasoning|SKL_control_theory_planner|user|control-theory-planner|on trigger|persistent
@SKL: SKL_decision_inverter|user|skill|decision-inverter|reasoning|low|low|conceptual|~/.cursor/skills/decision-inverter/SKILL.md|persistent
@CLM: CLM_mat_011|reasoning|SKL_decision_inverter|user|decision-inverter|on trigger|persistent
@SKL: SKL_empirical_paradox_synthesis|user|skill|empirical-paradox-synthesis|reasoning|low|low|conceptual|~/.cursor/skills/empirical-paradox-synthesis/SKILL.md|persistent
@CLM: CLM_mat_012|reasoning|SKL_empirical_paradox_synthesis|user|empirical-paradox-synthesis|on trigger|persistent
@SKL: SKL_engineering_practices_learner|user|skill|engineering-practices-learner|meta|low|low|conceptual|~/.cursor/skills/engineering-practices-learner/SKILL.md|persistent
@CLM: CLM_mat_013|meta|SKL_engineering_practices_learner|user|engineering-practices-learner|on trigger|persistent
@SKL: SKL_entropy_reasoner|user|skill|entropy-reasoner|reasoning|low|low|conceptual|~/.cursor/skills/entropy-reasoner/SKILL.md|persistent
@CLM: CLM_mat_014|reasoning|SKL_entropy_reasoner|user|entropy-reasoner|on trigger|persistent
@SKL: SKL_falsification_tester|user|skill|falsification-tester|reasoning|low|low|conceptual|~/.cursor/skills/falsification-tester/SKILL.md|persistent
@CLM: CLM_mat_015|reasoning|SKL_falsification_tester|user|falsification-tester|on trigger|persistent
@SKL: SKL_file_operations|user|skill|file-operations|meta|low|low|conceptual|~/.cursor/skills/file-operations/SKILL.md|persistent
@CLM: CLM_mat_016|meta|SKL_file_operations|user|file-operations|on trigger|persistent
@SKL: SKL_first_principle_thinker|user|skill|first-principle-thinker|reasoning|low|low|conceptual|~/.cursor/skills/first-principle-thinker/SKILL.md|persistent
@CLM: CLM_mat_017|reasoning|SKL_first_principle_thinker|user|first-principle-thinker|on trigger|persistent
@SKL: SKL_game_theory_strategist|user|skill|game-theory-strategist|reasoning|low|low|conceptual|~/.cursor/skills/game-theory-strategist/SKILL.md|persistent
@CLM: CLM_mat_018|reasoning|SKL_game_theory_strategist|user|game-theory-strategist|on trigger|persistent
@SKL: SKL_incentive_alignment_reviewer|user|skill|incentive-alignment-reviewer|reasoning|low|low|conceptual|~/.cursor/skills/incentive-alignment-reviewer/SKILL.md|persistent
@CLM: CLM_mat_019|reasoning|SKL_incentive_alignment_reviewer|user|incentive-alignment-reviewer|on trigger|persistent
@SKL: SKL_inversion_thinker|user|skill|inversion-thinker|reasoning|low|low|conceptual|~/.cursor/skills/inversion-thinker/SKILL.md|persistent
@CLM: CLM_mat_020|reasoning|SKL_inversion_thinker|user|inversion-thinker|on trigger|persistent
@SKL: SKL_knowledge_consolidator|user|skill|knowledge-consolidator|reasoning|low|low|conceptual|~/.cursor/skills/knowledge-consolidator/SKILL.md|persistent
@CLM: CLM_mat_021|reasoning|SKL_knowledge_consolidator|user|knowledge-consolidator|on trigger|persistent
@SKL: SKL_launch_readiness_assessor|user|skill|launch-readiness-assessor|reasoning|low|low|conceptual|~/.cursor/skills/launch-readiness-assessor/SKILL.md|persistent
@CLM: CLM_mat_022|reasoning|SKL_launch_readiness_assessor|user|launch-readiness-assessor|on trigger|persistent
@SKL: SKL_llm_model_suggester|user|skill|llm-model-suggester|meta|low|low|conceptual|~/.cursor/skills/llm-model-suggester/SKILL.md|persistent
@CLM: CLM_mat_023|meta|SKL_llm_model_suggester|user|llm-model-suggester|on trigger|persistent
@SKL: SKL_markdown_preview_enhanced|user|skill|markdown-preview-enhanced|doc|low|low|conceptual|~/.cursor/skills/markdown-preview-enhanced/SKILL.md|persistent
@CLM: CLM_mat_024|doc|SKL_markdown_preview_enhanced|user|markdown-preview-enhanced|on trigger|persistent
@SKL: SKL_markdown_viewer_user_pack|user|skill|markdown-viewer-user-pack|doc|low|low|conceptual|~/.cursor/skills/markdown-viewer-user-pack/SKILL.md|persistent
@CLM: CLM_mat_025|doc|SKL_markdown_viewer_user_pack|user|markdown-viewer-user-pack|on trigger|persistent
@SKL: SKL_mcdm_decider|user|skill|mcdm-decider|reasoning|low|low|conceptual|~/.cursor/skills/mcdm-decider/SKILL.md|persistent
@CLM: CLM_mat_026|reasoning|SKL_mcdm_decider|user|mcdm-decider|on trigger|persistent
@SKL: SKL_mcp_chrome_devtools|user|skill|mcp-chrome-devtools|meta|low|low|conceptual|~/.cursor/skills/mcp-chrome-devtools/SKILL.md|persistent
@CLM: CLM_mat_027|meta|SKL_mcp_chrome_devtools|user|mcp-chrome-devtools|on trigger|persistent
@SKL: SKL_mcp_latex|user|skill|mcp-latex|meta|low|low|conceptual|~/.cursor/skills/mcp-latex/SKILL.md|persistent
@CLM: CLM_mat_028|meta|SKL_mcp_latex|user|mcp-latex|on trigger|persistent
@SKL: SKL_mcp_memnet|user|skill|mcp-memnet|meta|low|low|conceptual|~/.cursor/skills/mcp-memnet/SKILL.md|persistent
@CLM: CLM_mat_029|meta|SKL_mcp_memnet|user|mcp-memnet|on trigger|persistent
@SKL: SKL_mcp_novel_writer|user|skill|mcp-novel-writer|meta|low|low|conceptual|~/.cursor/skills/mcp-novel-writer/SKILL.md|persistent
@CLM: CLM_mat_030|meta|SKL_mcp_novel_writer|user|mcp-novel-writer|on trigger|persistent
@SKL: SKL_mcp_sysml_v2|user|skill|mcp-sysml-v2|sysml-tool|low|low|conceptual|~/.cursor/skills/mcp-sysml-v2/SKILL.md|persistent
@CLM: CLM_mat_031|sysml-tool|SKL_mcp_sysml_v2|user|mcp-sysml-v2|on trigger|persistent
@SKL: SKL_mcp_sysmledgraph|user|skill|mcp-sysmledgraph|sysml-tool|low|low|conceptual|~/.cursor/skills/mcp-sysmledgraph/SKILL.md|persistent
@CLM: CLM_mat_032|sysml-tool|SKL_mcp_sysmledgraph|user|mcp-sysmledgraph|on trigger|persistent
@SKL: SKL_md_to_tex|user|skill|md-to-tex|doc|low|low|conceptual|~/.cursor/skills/md-to-tex/SKILL.md|persistent
@CLM: CLM_mat_033|doc|SKL_md_to_tex|user|md-to-tex|on trigger|persistent
@SKL: SKL_mdtohtml|user|skill|mdtohtml|doc|low|low|conceptual|~/.cursor/skills/mdtohtml/SKILL.md|persistent
@CLM: CLM_mat_034|doc|SKL_mdtohtml|user|mdtohtml|on trigger|persistent
@SKL: SKL_meeting_notes_generator|user|skill|meeting-notes-generator|doc|low|low|conceptual|~/.cursor/skills/meeting-notes-generator/SKILL.md|persistent
@CLM: CLM_mat_035|doc|SKL_meeting_notes_generator|user|meeting-notes-generator|on trigger|persistent
@SKL: SKL_memnet_codebase_snap|user|skill|memnet-codebase-snap|meta|low|low|conceptual|~/.cursor/skills/memnet-codebase-snap/SKILL.md|persistent
@CLM: CLM_mat_036|meta|SKL_memnet_codebase_snap|user|memnet-codebase-snap|on trigger|persistent
@SKL: SKL_memnet_format|user|skill|memnet-format|meta|low|low|conceptual|~/.cursor/skills/memnet-format/SKILL.md|persistent
@CLM: CLM_mat_037|meta|SKL_memnet_format|user|memnet-format|on trigger|persistent
@SKL: SKL_mermaid|user|skill|mermaid|doc|low|low|conceptual|~/.cursor/skills/mermaid/SKILL.md|persistent
@CLM: CLM_mat_038|doc|SKL_mermaid|user|mermaid|on trigger|persistent
@SKL: SKL_mermaid_doc_readability|user|skill|mermaid-doc-readability|doc|low|low|conceptual|~/.cursor/skills/mermaid-doc-readability/SKILL.md|persistent
@CLM: CLM_mat_039|doc|SKL_mermaid_doc_readability|user|mermaid-doc-readability|on trigger|persistent
@SKL: SKL_mmdc|user|skill|mmdc|doc|low|low|conceptual|~/.cursor/skills/mmdc/SKILL.md|persistent
@CLM: CLM_mat_040|doc|SKL_mmdc|user|mmdc|on trigger|persistent
@SKL: SKL_optimization_planner|user|skill|optimization-planner|reasoning|low|low|conceptual|~/.cursor/skills/optimization-planner/SKILL.md|persistent
@CLM: CLM_mat_041|reasoning|SKL_optimization_planner|user|optimization-planner|on trigger|persistent
@SKL: SKL_pandas_expert|user|skill|pandas-expert|reasoning|low|low|conceptual|~/.cursor/skills/pandas-expert/SKILL.md|persistent
@CLM: CLM_mat_042|reasoning|SKL_pandas_expert|user|pandas-expert|on trigger|persistent
@SKL: SKL_paradox_method|user|skill|paradox-method|reasoning|low|low|conceptual|~/.cursor/skills/paradox-method/SKILL.md|persistent
@CLM: CLM_mat_043|reasoning|SKL_paradox_method|user|paradox-method|on trigger|persistent
@SKL: SKL_pcba_design_reviewer|user|skill|pcba-design-reviewer|pcba|low|low|conceptual|~/.cursor/skills/pcba-design-reviewer/SKILL.md|persistent
@CLM: CLM_mat_044|pcba|SKL_pcba_design_reviewer|user|pcba-design-reviewer|on trigger|persistent
@SKL: SKL_pcba_netlist_reader|user|skill|pcba-netlist-reader|pcba|low|low|conceptual|~/.cursor/skills/pcba-netlist-reader/SKILL.md|persistent
@CLM: CLM_mat_045|pcba|SKL_pcba_netlist_reader|user|pcba-netlist-reader|on trigger|persistent
@SKL: SKL_polarfire_soc_setup|user|skill|polarfire-soc-setup|pcba|low|low|conceptual|~/.cursor/skills/polarfire-soc-setup/SKILL.md|persistent
@CLM: CLM_mat_046|pcba|SKL_polarfire_soc_setup|user|polarfire-soc-setup|on trigger|persistent
@SKL: SKL_pr_reviewer|user|skill|pr-reviewer|review|low|low|conceptual|~/.cursor/skills/pr-reviewer/SKILL.md|persistent
@CLM: CLM_mat_047|review|SKL_pr_reviewer|user|pr-reviewer|on trigger|persistent
@SKL: SKL_pretty_mermaid|user|skill|pretty-mermaid|doc|low|low|conceptual|~/.cursor/skills/pretty-mermaid/SKILL.md|persistent
@CLM: CLM_mat_048|doc|SKL_pretty_mermaid|user|pretty-mermaid|on trigger|persistent
@SKL: SKL_project_output_article|user|skill|project-output-article|doc|low|low|conceptual|~/.cursor/skills/project-output-article/SKILL.md|persistent
@CLM: CLM_mat_049|doc|SKL_project_output_article|user|project-output-article|on trigger|persistent
@SKL: SKL_project_planner|user|skill|project-planner|doc|low|low|conceptual|~/.cursor/skills/project-planner/SKILL.md|persistent
@CLM: CLM_mat_050|doc|SKL_project_planner|user|project-planner|on trigger|persistent
@SKL: SKL_reasoning_strategy_selector|user|skill|reasoning-strategy-selector|reasoning|low|low|conceptual|~/.cursor/skills/reasoning-strategy-selector/SKILL.md|persistent
@CLM: CLM_mat_051|reasoning|SKL_reasoning_strategy_selector|user|reasoning-strategy-selector|on trigger|persistent
@SKL: SKL_rfc_generator|user|skill|rfc-generator|doc|low|low|conceptual|~/.cursor/skills/rfc-generator/SKILL.md|persistent
@CLM: CLM_mat_052|doc|SKL_rfc_generator|user|rfc-generator|on trigger|persistent
@SKL: SKL_risk_assessor|user|skill|risk-assessor|reasoning|low|low|conceptual|~/.cursor/skills/risk-assessor/SKILL.md|persistent
@CLM: CLM_mat_053|reasoning|SKL_risk_assessor|user|risk-assessor|on trigger|persistent
@SKL: SKL_scientific_method_first_principles|user|skill|scientific-method-first-principles|reasoning|low|low|conceptual|~/.cursor/skills/scientific-method-first-principles/SKILL.md|persistent
@CLM: CLM_mat_054|reasoning|SKL_scientific_method_first_principles|user|scientific-method-first-principles|on trigger|persistent
@SKL: SKL_security_reviewer|user|skill|security-reviewer|review|low|low|conceptual|~/.cursor/skills/security-reviewer/SKILL.md|persistent
@CLM: CLM_mat_055|review|SKL_security_reviewer|user|security-reviewer|on trigger|persistent
@SKL: SKL_skill_creator|user|skill|skill-creator|meta|low|low|conceptual|~/.cursor/skills/skill-creator/SKILL.md|persistent
@CLM: CLM_mat_056|meta|SKL_skill_creator|user|skill-creator|on trigger|persistent
@SKL: SKL_skill_reviewer|user|skill|skill-reviewer|review|low|low|conceptual|~/.cursor/skills/skill-reviewer/SKILL.md|persistent
@CLM: CLM_mat_057|review|SKL_skill_reviewer|user|skill-reviewer|on trigger|persistent
@SKL: SKL_skillfish|user|skill|skillfish|meta|low|low|conceptual|~/.cursor/skills/skillfish/SKILL.md|persistent
@CLM: CLM_mat_058|meta|SKL_skillfish|user|skillfish|on trigger|persistent
@SKL: SKL_sysml_allocate_generator|user|skill|sysml-allocate-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-allocate-generator/SKILL.md|persistent
@CLM: CLM_mat_059|sysml|SKL_sysml_allocate_generator|user|sysml-allocate-generator|on trigger|persistent
@SKL: SKL_sysml_behaviour_generator|user|skill|sysml-behaviour-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-behaviour-generator/SKILL.md|persistent
@CLM: CLM_mat_060|sysml|SKL_sysml_behaviour_generator|user|sysml-behaviour-generator|on trigger|persistent
@SKL: SKL_sysml_common_file_scale|user|skill|sysml-common-file-scale|sysml|low|low|conceptual|~/.cursor/skills/sysml-common-file-scale/SKILL.md|persistent
@CLM: CLM_mat_061|sysml|SKL_sysml_common_file_scale|user|sysml-common-file-scale|on trigger|persistent
@SKL: SKL_sysml_common_lib_contribution|user|skill|sysml-common-lib-contribution|sysml|low|low|conceptual|~/.cursor/skills/sysml-common-lib-contribution/SKILL.md|persistent
@CLM: CLM_mat_062|sysml|SKL_sysml_common_lib_contribution|user|sysml-common-lib-contribution|on trigger|persistent
@SKL: SKL_sysml_common_library_naming|user|skill|sysml-common-library-naming|sysml|low|low|conceptual|~/.cursor/skills/sysml-common-library-naming/SKILL.md|persistent
@CLM: CLM_mat_063|sysml|SKL_sysml_common_library_naming|user|sysml-common-library-naming|on trigger|persistent
@SKL: SKL_sysml_connections|user|skill|sysml-connections|sysml|low|low|conceptual|~/.cursor/skills/sysml-connections/SKILL.md|persistent
@CLM: CLM_mat_064|sysml|SKL_sysml_connections|user|sysml-connections|on trigger|persistent
@SKL: SKL_sysml_eagle_netlist_bridge|user|skill|sysml-eagle-netlist-bridge|sysml|low|low|conceptual|~/.cursor/skills/sysml-eagle-netlist-bridge/SKILL.md|persistent
@CLM: CLM_mat_065|sysml|SKL_sysml_eagle_netlist_bridge|user|sysml-eagle-netlist-bridge|on trigger|persistent
@SKL: SKL_sysml_eagle_netlist_parser_tool|user|skill|sysml-eagle-netlist-parser-tool|sysml|low|low|conceptual|~/.cursor/skills/sysml-eagle-netlist-parser-tool/SKILL.md|persistent
@CLM: CLM_mat_066|sysml|SKL_sysml_eagle_netlist_parser_tool|user|sysml-eagle-netlist-parser-tool|on trigger|persistent
@SKL: SKL_sysml_hardware_part_generator|user|skill|sysml-hardware-part-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-hardware-part-generator/SKILL.md|persistent
@CLM: CLM_mat_067|sysml|SKL_sysml_hardware_part_generator|user|sysml-hardware-part-generator|on trigger|persistent
@SKL: SKL_sysml_import_order_helper|user|skill|sysml-import-order-helper|sysml|low|low|conceptual|~/.cursor/skills/sysml-import-order-helper/SKILL.md|persistent
@CLM: CLM_mat_068|sysml|SKL_sysml_import_order_helper|user|sysml-import-order-helper|on trigger|persistent
@SKL: SKL_sysml_interconnection_mermaid|user|skill|sysml-interconnection-mermaid|sysml|low|low|conceptual|~/.cursor/skills/sysml-interconnection-mermaid/SKILL.md|persistent
@CLM: CLM_mat_069|sysml|SKL_sysml_interconnection_mermaid|user|sysml-interconnection-mermaid|on trigger|persistent
@SKL: SKL_sysml_item_generator|user|skill|sysml-item-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-item-generator/SKILL.md|persistent
@CLM: CLM_mat_070|sysml|SKL_sysml_item_generator|user|sysml-item-generator|on trigger|persistent
@SKL: SKL_sysml_memnet_cache|user|skill|sysml-memnet-cache|sysml|low|low|conceptual|~/.cursor/skills/sysml-memnet-cache/SKILL.md|persistent
@CLM: CLM_mat_071|sysml|SKL_sysml_memnet_cache|user|sysml-memnet-cache|on trigger|persistent
@SKL: SKL_sysml_memnet_documentation|user|skill|sysml-memnet-documentation|sysml|low|low|conceptual|~/.cursor/skills/sysml-memnet-documentation/SKILL.md|persistent
@CLM: CLM_mat_072|sysml|SKL_sysml_memnet_documentation|user|sysml-memnet-documentation|on trigger|persistent
@SKL: SKL_sysml_modeling_session_checklist|user|skill|sysml-modeling-session-checklist|sysml|low|low|conceptual|~/.cursor/skills/sysml-modeling-session-checklist/SKILL.md|persistent
@CLM: CLM_mat_073|sysml|SKL_sysml_modeling_session_checklist|user|sysml-modeling-session-checklist|on trigger|persistent
@SKL: SKL_sysml_modeling_workflow|user|skill|sysml-modeling-workflow|sysml|low|low|conceptual|~/.cursor/skills/sysml-modeling-workflow/SKILL.md|persistent
@CLM: CLM_mat_074|sysml|SKL_sysml_modeling_workflow|user|sysml-modeling-workflow|on trigger|persistent
@SKL: SKL_sysml_nested_structure_modeling|user|skill|sysml-nested-structure-modeling|sysml|low|low|conceptual|~/.cursor/skills/sysml-nested-structure-modeling/SKILL.md|persistent
@CLM: CLM_mat_075|sysml|SKL_sysml_nested_structure_modeling|user|sysml-nested-structure-modeling|on trigger|persistent
@SKL: SKL_sysml_new_project|user|skill|sysml-new-project|sysml|low|low|conceptual|~/.cursor/skills/sysml-new-project/SKILL.md|persistent
@CLM: CLM_mat_076|sysml|SKL_sysml_new_project|user|sysml-new-project|on trigger|persistent
@SKL: SKL_sysml_part_reviewer|user|skill|sysml-part-reviewer|sysml|low|low|conceptual|~/.cursor/skills/sysml-part-reviewer/SKILL.md|persistent
@CLM: CLM_mat_077|sysml|SKL_sysml_part_reviewer|user|sysml-part-reviewer|on trigger|persistent
@SKL: SKL_sysml_pcba_de_facto_alignment|user|skill|sysml-pcba-de-facto-alignment|sysml|low|low|conceptual|~/.cursor/skills/sysml-pcba-de-facto-alignment/SKILL.md|persistent
@CLM: CLM_mat_078|sysml|SKL_sysml_pcba_de_facto_alignment|user|sysml-pcba-de-facto-alignment|on trigger|persistent
@SKL: SKL_sysml_physical_port_generator|user|skill|sysml-physical-port-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-physical-port-generator/SKILL.md|persistent
@CLM: CLM_mat_079|sysml|SKL_sysml_physical_port_generator|user|sysml-physical-port-generator|on trigger|persistent
@SKL: SKL_sysml_refactorer|user|skill|sysml-refactorer|sysml|low|low|conceptual|~/.cursor/skills/sysml-refactorer/SKILL.md|persistent
@CLM: CLM_mat_080|sysml|SKL_sysml_refactorer|user|sysml-refactorer|on trigger|persistent
@SKL: SKL_sysml_requirements_audit|user|skill|sysml-requirements-audit|sysml|low|low|conceptual|~/.cursor/skills/sysml-requirements-audit/SKILL.md|persistent
@CLM: CLM_mat_081|sysml|SKL_sysml_requirements_audit|user|sysml-requirements-audit|on trigger|persistent
@SKL: SKL_sysml_requirements_generator|user|skill|sysml-requirements-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-requirements-generator/SKILL.md|persistent
@CLM: CLM_mat_082|sysml|SKL_sysml_requirements_generator|user|sysml-requirements-generator|on trigger|persistent
@SKL: SKL_sysml_root_config|user|skill|sysml-root-config|sysml|low|low|conceptual|~/.cursor/skills/sysml-root-config/SKILL.md|persistent
@CLM: CLM_mat_083|sysml|SKL_sysml_root_config|user|sysml-root-config|on trigger|persistent
@SKL: SKL_sysml_signal_processing_pipeline|user|skill|sysml-signal-processing-pipeline|sysml|low|low|conceptual|~/.cursor/skills/sysml-signal-processing-pipeline/SKILL.md|persistent
@CLM: CLM_mat_084|sysml|SKL_sysml_signal_processing_pipeline|user|sysml-signal-processing-pipeline|on trigger|persistent
@SKL: SKL_sysml_software_part_generator|user|skill|sysml-software-part-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-software-part-generator/SKILL.md|persistent
@CLM: CLM_mat_085|sysml|SKL_sysml_software_part_generator|user|sysml-software-part-generator|on trigger|persistent
@SKL: SKL_sysml_software_port_generator|user|skill|sysml-software-port-generator|sysml|low|low|conceptual|~/.cursor/skills/sysml-software-port-generator/SKILL.md|persistent
@CLM: CLM_mat_086|sysml|SKL_sysml_software_port_generator|user|sysml-software-port-generator|on trigger|persistent
@SKL: SKL_sysml_stakeholder_use_case|user|skill|sysml-stakeholder-use-case|sysml|low|low|conceptual|~/.cursor/skills/sysml-stakeholder-use-case/SKILL.md|persistent
@CLM: CLM_mat_087|sysml|SKL_sysml_stakeholder_use_case|user|sysml-stakeholder-use-case|on trigger|persistent
@SKL: SKL_sysml_traceability|user|skill|sysml-traceability|sysml|low|low|conceptual|~/.cursor/skills/sysml-traceability/SKILL.md|persistent
@CLM: CLM_mat_088|sysml|SKL_sysml_traceability|user|sysml-traceability|on trigger|persistent
@SKL: SKL_sysml_v2_release_how_to_use|user|skill|sysml-v2-release-how-to-use|sysml|low|low|conceptual|~/.cursor/skills/sysml-v2-release-how-to-use/SKILL.md|persistent
@CLM: CLM_mat_089|sysml|SKL_sysml_v2_release_how_to_use|user|sysml-v2-release-how-to-use|on trigger|persistent
@SKL: SKL_sysml_v2_syntax_reference|user|skill|sysml-v2-syntax-reference|sysml|low|low|conceptual|~/.cursor/skills/sysml-v2-syntax-reference/SKILL.md|persistent
@CLM: CLM_mat_090|sysml|SKL_sysml_v2_syntax_reference|user|sysml-v2-syntax-reference|on trigger|persistent
@SKL: SKL_sysml_view_doc_sync|user|skill|sysml-view-doc-sync|sysml|low|low|conceptual|~/.cursor/skills/sysml-view-doc-sync/SKILL.md|persistent
@CLM: CLM_mat_091|sysml|SKL_sysml_view_doc_sync|user|sysml-view-doc-sync|on trigger|persistent
@SKL: SKL_system_design_report_generator|user|skill|system-design-report-generator|doc|low|low|conceptual|~/.cursor/skills/system-design-report-generator/SKILL.md|persistent
@CLM: CLM_mat_092|doc|SKL_system_design_report_generator|user|system-design-report-generator|on trigger|persistent
@SKL: SKL_tech_report_generator|user|skill|tech-report-generator|doc|low|low|conceptual|~/.cursor/skills/tech-report-generator/SKILL.md|persistent
@CLM: CLM_mat_093|doc|SKL_tech_report_generator|user|tech-report-generator|on trigger|persistent
@SKL: SKL_tech_report_reviewer|user|skill|tech-report-reviewer|doc|low|low|conceptual|~/.cursor/skills/tech-report-reviewer/SKILL.md|persistent
@CLM: CLM_mat_094|doc|SKL_tech_report_reviewer|user|tech-report-reviewer|on trigger|persistent
@SKL: SKL_toon_prompt_format|user|skill|toon-prompt-format|meta|low|low|conceptual|~/.cursor/skills/toon-prompt-format/SKILL.md|persistent
@CLM: CLM_mat_095|meta|SKL_toon_prompt_format|user|toon-prompt-format|on trigger|persistent
@SKL: SKL_traceability_footprint_to_sysml|user|skill|traceability-footprint-to-sysml|meta|low|low|conceptual|~/.cursor/skills/traceability-footprint-to-sysml/SKILL.md|persistent
@CLM: CLM_mat_096|meta|SKL_traceability_footprint_to_sysml|user|traceability-footprint-to-sysml|on trigger|persistent
@SKL: SKL_tron_format|user|skill|tron-format|meta|low|low|conceptual|~/.cursor/skills/tron-format/SKILL.md|persistent
@CLM: CLM_mat_097|meta|SKL_tron_format|user|tron-format|on trigger|persistent
@SKL: SKL_automate|cursor|skill|automate|cursor|low|low|conceptual|~/.cursor/skills-cursor/automate/SKILL.md|persistent
@CLM: CLM_mat_098|cursor|SKL_automate|cursor|automate|on trigger|persistent
@SKL: SKL_babysit|cursor|skill|babysit|cursor|low|low|conceptual|~/.cursor/skills-cursor/babysit/SKILL.md|persistent
@CLM: CLM_mat_099|cursor|SKL_babysit|cursor|babysit|on trigger|persistent
@SKL: SKL_canvas|cursor|skill|canvas|cursor|low|low|conceptual|~/.cursor/skills-cursor/canvas/SKILL.md|persistent
@CLM: CLM_mat_100|cursor|SKL_canvas|cursor|canvas|on trigger|persistent
@SKL: SKL_create_hook|cursor|skill|create-hook|cursor|low|low|conceptual|~/.cursor/skills-cursor/create-hook/SKILL.md|persistent
@CLM: CLM_mat_101|cursor|SKL_create_hook|cursor|create-hook|on trigger|persistent
@SKL: SKL_create_rule|cursor|skill|create-rule|cursor|low|low|conceptual|~/.cursor/skills-cursor/create-rule/SKILL.md|persistent
@CLM: CLM_mat_102|cursor|SKL_create_rule|cursor|create-rule|on trigger|persistent
@SKL: SKL_create_skill|cursor|skill|create-skill|cursor|low|low|conceptual|~/.cursor/skills-cursor/create-skill/SKILL.md|persistent
@CLM: CLM_mat_103|cursor|SKL_create_skill|cursor|create-skill|on trigger|persistent
@SKL: SKL_create_subagent|cursor|skill|create-subagent|cursor|low|low|conceptual|~/.cursor/skills-cursor/create-subagent/SKILL.md|persistent
@CLM: CLM_mat_104|cursor|SKL_create_subagent|cursor|create-subagent|on trigger|persistent
@SKL: SKL_loop|cursor|skill|loop|cursor|low|low|conceptual|~/.cursor/skills-cursor/loop/SKILL.md|persistent
@CLM: CLM_mat_105|cursor|SKL_loop|cursor|loop|on trigger|persistent
@SKL: SKL_migrate_to_skills|cursor|skill|migrate-to-skills|cursor|low|low|conceptual|~/.cursor/skills-cursor/migrate-to-skills/SKILL.md|persistent
@CLM: CLM_mat_106|cursor|SKL_migrate_to_skills|cursor|migrate-to-skills|on trigger|persistent
@SKL: SKL_onboard|cursor|skill|onboard|cursor|low|low|conceptual|~/.cursor/skills-cursor/onboard/SKILL.md|persistent
@CLM: CLM_mat_107|cursor|SKL_onboard|cursor|onboard|on trigger|persistent
@SKL: SKL_review|cursor|skill|review|cursor|low|low|conceptual|~/.cursor/skills-cursor/review/SKILL.md|persistent
@CLM: CLM_mat_108|cursor|SKL_review|cursor|review|on trigger|persistent
@SKL: SKL_review_bugbot|cursor|skill|review-bugbot|cursor|low|low|conceptual|~/.cursor/skills-cursor/review-bugbot/SKILL.md|persistent
@CLM: CLM_mat_109|cursor|SKL_review_bugbot|cursor|review-bugbot|on trigger|persistent
@SKL: SKL_review_security|cursor|skill|review-security|cursor|low|low|conceptual|~/.cursor/skills-cursor/review-security/SKILL.md|persistent
@CLM: CLM_mat_110|cursor|SKL_review_security|cursor|review-security|on trigger|persistent
@SKL: SKL_sdk|cursor|skill|sdk|cursor|low|low|conceptual|~/.cursor/skills-cursor/sdk/SKILL.md|persistent
@CLM: CLM_mat_111|cursor|SKL_sdk|cursor|sdk|on trigger|persistent
@SKL: SKL_shell|cursor|skill|shell|cursor|low|low|conceptual|~/.cursor/skills-cursor/shell/SKILL.md|persistent
@CLM: CLM_mat_112|cursor|SKL_shell|cursor|shell|on trigger|persistent
@SKL: SKL_split_to_prs|cursor|skill|split-to-prs|cursor|low|low|conceptual|~/.cursor/skills-cursor/split-to-prs/SKILL.md|persistent
@CLM: CLM_mat_113|cursor|SKL_split_to_prs|cursor|split-to-prs|on trigger|persistent
@SKL: SKL_statusline|cursor|skill|statusline|cursor|low|low|conceptual|~/.cursor/skills-cursor/statusline/SKILL.md|persistent
@CLM: CLM_mat_114|cursor|SKL_statusline|cursor|statusline|on trigger|persistent
@SKL: SKL_update_cli_config|cursor|skill|update-cli-config|cursor|low|low|conceptual|~/.cursor/skills-cursor/update-cli-config/SKILL.md|persistent
@CLM: CLM_mat_115|cursor|SKL_update_cli_config|cursor|update-cli-config|on trigger|persistent
@SKL: SKL_update_cursor_settings|cursor|skill|update-cursor-settings|cursor|low|low|conceptual|~/.cursor/skills-cursor/update-cursor-settings/SKILL.md|persistent
@CLM: CLM_mat_116|cursor|SKL_update_cursor_settings|cursor|update-cursor-settings|on trigger|persistent
@EDG: E_sm_08|SET_skills_user|memberOf|SKG_mxo4|user_pack|persistent
@EDG: E_sm_09|SET_skills_cursor|memberOf|SKG_mxo4|cursor_pack|persistent
@ROU: ROU_skill_graph|global skill disambiguation|SKL_reasoning_strategy_selector|persistent
@EDG: E_sm_10|SKG_mxo4|routes|ROU_skill_graph|meta|persistent
```
