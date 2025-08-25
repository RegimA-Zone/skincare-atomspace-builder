"""Skincare multiscale schema service."""

from typing import Dict, List, Any, Optional
from ..models.schemas import (
    SkincareMultiscaleSchema,
    SkincareSchemaTemplate,
    SkincareSchemaRequest,
    SkincareSchemaResponse,
    SkincareScaleLevel,
    SkincareFunctionalAspect,
    SkincareMolecularComponent,
    SkincareCellularComponent,
    SkincareTissueComponent,
    SkincareEnvironmentalComponent,
    SkincareInteraction,
    SkincareMolecularType,
    SkincareCellularType,
    SkincareTissueLevel,
    SkincareEnvironmentalFactor,
    DataSource
)


class SkincareSchemaService:
    """Service for generating skincare-specific multiscale schemas."""
    
    def __init__(self):
        self._templates = self._initialize_templates()
    
    def generate_schema(self, request: SkincareSchemaRequest) -> SkincareSchemaResponse:
        """Generate a skincare schema based on the request."""
        
        # Select appropriate template if available
        template = self._select_template(request)
        
        if template:
            schema = self._customize_template(template, request)
            template_used = template.template_id
        else:
            schema = self._create_schema_from_scratch(request)
            template_used = None
        
        # Add data source specific components if provided
        if request.data_sources:
            schema = self._enhance_with_data_sources(schema, request.data_sources)
        
        recommendations = self._generate_recommendations(schema, request)
        
        return SkincareSchemaResponse(
            schema=schema,
            template_used=template_used,
            recommendations=recommendations
        )
    
    def get_available_templates(self) -> List[SkincareSchemaTemplate]:
        """Get all available skincare schema templates."""
        return list(self._templates.values())
    
    def get_template(self, template_id: str) -> Optional[SkincareSchemaTemplate]:
        """Get a specific template by ID."""
        return self._templates.get(template_id)
    
    def validate_schema(self, schema: SkincareMultiscaleSchema) -> Dict[str, Any]:
        """Validate a skincare schema for completeness and consistency."""
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # Check for cross-scale interactions
        molecular_ids = {comp.id for comp in schema.molecular_components}
        cellular_ids = {comp.id for comp in schema.cellular_components}
        tissue_ids = {comp.id for comp in schema.tissue_components}
        env_ids = {comp.id for comp in schema.environmental_components}
        
        all_component_ids = molecular_ids | cellular_ids | tissue_ids | env_ids
        
        # Validate interactions reference existing components
        for interaction in schema.interactions:
            if interaction.source_component not in all_component_ids:
                validation_result["errors"].append(
                    f"Interaction references non-existent source component: {interaction.source_component}"
                )
                validation_result["valid"] = False
            
            if interaction.target_component not in all_component_ids:
                validation_result["errors"].append(
                    f"Interaction references non-existent target component: {interaction.target_component}"
                )
                validation_result["valid"] = False
        
        # Check for missing scale relationships
        if schema.molecular_components and not schema.cellular_components:
            validation_result["warnings"].append(
                "Schema has molecular components but no cellular components - consider adding cellular level"
            )
        
        if schema.cellular_components and not schema.tissue_components:
            validation_result["warnings"].append(
                "Schema has cellular components but no tissue components - consider adding tissue level"
            )
        
        # Suggest functional outcomes if missing
        if not schema.functional_outcomes:
            validation_result["suggestions"].append(
                "Consider adding functional outcomes to better understand the skin health impact"
            )
        
        return validation_result
    
    def _initialize_templates(self) -> Dict[str, SkincareSchemaTemplate]:
        """Initialize pre-defined skincare schema templates."""
        templates = {}
        
        # Anti-aging template
        anti_aging_schema = self._create_anti_aging_template()
        templates["anti_aging"] = SkincareSchemaTemplate(
            template_id="anti_aging",
            name="Anti-Aging Skincare",
            description="Schema for modeling anti-aging skincare effects across multiple scales",
            use_case="anti_aging",
            target_scale_levels=[SkincareScaleLevel.MOLECULAR, SkincareScaleLevel.CELLULAR, SkincareScaleLevel.TISSUE],
            schema=anti_aging_schema,
            metadata={"focus": "collagen, elastin, wrinkles, cellular renewal"}
        )
        
        # Barrier function template
        barrier_schema = self._create_barrier_function_template()
        templates["barrier_function"] = SkincareSchemaTemplate(
            template_id="barrier_function",
            name="Skin Barrier Function",
            description="Schema for modeling skin barrier function and protection",
            use_case="barrier_protection",
            target_scale_levels=[SkincareScaleLevel.MOLECULAR, SkincareScaleLevel.TISSUE, SkincareScaleLevel.ENVIRONMENTAL],
            schema=barrier_schema,
            metadata={"focus": "stratum corneum, ceramides, TEWL, hydration"}
        )
        
        # Acne treatment template
        acne_schema = self._create_acne_treatment_template()
        templates["acne_treatment"] = SkincareSchemaTemplate(
            template_id="acne_treatment",
            name="Acne Treatment",
            description="Schema for modeling acne formation and treatment mechanisms",
            use_case="acne_treatment",
            target_scale_levels=[SkincareScaleLevel.CELLULAR, SkincareScaleLevel.TISSUE, SkincareScaleLevel.ENVIRONMENTAL],
            schema=acne_schema,
            metadata={"focus": "sebocytes, inflammation, microbiome, pore blockage"}
        )
        
        return templates
    
    def _create_anti_aging_template(self) -> SkincareMultiscaleSchema:
        """Create schema template for anti-aging skincare."""
        # Molecular components
        molecular_components = [
            SkincareMolecularComponent(
                id="collagen_i",
                name="Collagen Type I",
                scale_level=SkincareScaleLevel.MOLECULAR,
                component_type="structural_protein",
                molecular_type=SkincareMolecularType.PROTEIN,
                molecular_weight=300000.0,
                affected_functions=[SkincareFunctionalAspect.AGING_PROCESS],
                properties={"primary_function": "skin_structure", "degradation_rate": "variable_with_age"}
            ),
            SkincareMolecularComponent(
                id="elastin",
                name="Elastin",
                scale_level=SkincareScaleLevel.MOLECULAR,
                component_type="elastic_protein",
                molecular_type=SkincareMolecularType.PROTEIN,
                molecular_weight=70000.0,
                affected_functions=[SkincareFunctionalAspect.AGING_PROCESS],
                properties={"primary_function": "skin_elasticity", "degradation_rate": "high_with_age"}
            ),
            SkincareMolecularComponent(
                id="retinol",
                name="Retinol",
                scale_level=SkincareScaleLevel.MOLECULAR,
                component_type="active_ingredient",
                molecular_type=SkincareMolecularType.VITAMIN,
                molecular_weight=286.45,
                concentration_range={"min": 0.01, "max": 0.1, "optimal": 0.05},
                penetration_depth="epidermis_dermis",
                affected_functions=[SkincareFunctionalAspect.AGING_PROCESS],
                properties={"mechanism": "cellular_renewal_stimulation"}
            )
        ]
        
        # Cellular components
        cellular_components = [
            SkincareCellularComponent(
                id="fibroblasts",
                name="Dermal Fibroblasts",
                scale_level=SkincareScaleLevel.CELLULAR,
                component_type="structural_cell",
                cellular_type=SkincareCellularType.FIBROBLAST,
                proliferation_rate=0.7,
                affected_functions=[SkincareFunctionalAspect.AGING_PROCESS],
                properties={"collagen_production": "primary", "elastin_production": "secondary"}
            )
        ]
        
        # Tissue components
        tissue_components = [
            SkincareTissueComponent(
                id="dermis",
                name="Dermis",
                scale_level=SkincareScaleLevel.TISSUE,
                component_type="skin_layer",
                tissue_level=SkincareTissueLevel.RETICULAR_DERMIS,
                thickness=2000.0,  # micrometers
                affected_functions=[SkincareFunctionalAspect.AGING_PROCESS],
                properties={"primary_function": "structural_support", "collagen_density": "high"}
            )
        ]
        
        # Interactions
        interactions = [
            SkincareInteraction(
                id="retinol_fibroblast_stimulation",
                source_component="retinol",
                target_component="fibroblasts",
                interaction_type="stimulates",
                strength=0.8,
                mechanism="gene_expression_enhancement",
                scale_crossing=True
            ),
            SkincareInteraction(
                id="fibroblast_collagen_production",
                source_component="fibroblasts",
                target_component="collagen_i",
                interaction_type="produces",
                strength=0.9,
                mechanism="protein_synthesis"
            )
        ]
        
        return SkincareMultiscaleSchema(
            molecular_components=molecular_components,
            cellular_components=cellular_components,
            tissue_components=tissue_components,
            interactions=interactions,
            functional_outcomes=[SkincareFunctionalAspect.AGING_PROCESS],
            scale_relationships={
                "molecular_to_cellular": ["retinol -> fibroblasts"],
                "cellular_to_tissue": ["fibroblasts -> dermis"]
            }
        )
    
    def _create_barrier_function_template(self) -> SkincareMultiscaleSchema:
        """Create schema template for skin barrier function."""
        molecular_components = [
            SkincareMolecularComponent(
                id="ceramides",
                name="Ceramides",
                scale_level=SkincareScaleLevel.MOLECULAR,
                component_type="barrier_lipid",
                molecular_type=SkincareMolecularType.LIPID,
                affected_functions=[SkincareFunctionalAspect.BARRIER_FUNCTION, SkincareFunctionalAspect.MOISTURE_RETENTION],
                properties={"barrier_strength": "high", "water_retention": "excellent"}
            )
        ]
        
        tissue_components = [
            SkincareTissueComponent(
                id="stratum_corneum",
                name="Stratum Corneum",
                scale_level=SkincareScaleLevel.TISSUE,
                component_type="barrier_layer",
                tissue_level=SkincareTissueLevel.STRATUM_CORNEUM,
                thickness=15.0,  # micrometers
                barrier_strength=0.95,
                affected_functions=[SkincareFunctionalAspect.BARRIER_FUNCTION],
                properties={"primary_function": "barrier_protection", "turnover_rate": "14_days"}
            )
        ]
        
        environmental_components = [
            SkincareEnvironmentalComponent(
                id="humidity_exposure",
                name="Environmental Humidity",
                scale_level=SkincareScaleLevel.ENVIRONMENTAL,
                component_type="environmental_factor",
                environmental_type=SkincareEnvironmentalFactor.HUMIDITY,
                exposure_level="variable",
                affected_functions=[SkincareFunctionalAspect.BARRIER_FUNCTION, SkincareFunctionalAspect.MOISTURE_RETENTION]
            )
        ]
        
        return SkincareMultiscaleSchema(
            molecular_components=molecular_components,
            tissue_components=tissue_components,
            environmental_components=environmental_components,
            functional_outcomes=[SkincareFunctionalAspect.BARRIER_FUNCTION, SkincareFunctionalAspect.MOISTURE_RETENTION]
        )
    
    def _create_acne_treatment_template(self) -> SkincareMultiscaleSchema:
        """Create schema template for acne treatment."""
        cellular_components = [
            SkincareCellularComponent(
                id="sebocytes",
                name="Sebocytes",
                scale_level=SkincareScaleLevel.CELLULAR,
                component_type="gland_cell",
                cellular_type=SkincareCellularType.SEBOCYTE,
                metabolic_activity="high",
                affected_functions=[SkincareFunctionalAspect.SEBUM_PRODUCTION, SkincareFunctionalAspect.INFLAMMATION],
                properties={"sebum_production_rate": "high", "hormone_sensitivity": "high"}
            )
        ]
        
        tissue_components = [
            SkincareTissueComponent(
                id="sebaceous_gland",
                name="Sebaceous Gland",
                scale_level=SkincareScaleLevel.TISSUE,
                component_type="gland_structure",
                tissue_level=SkincareTissueLevel.SEBACEOUS_GLAND,
                affected_functions=[SkincareFunctionalAspect.SEBUM_PRODUCTION],
                properties={"location": "hair_follicle", "size": "variable"}
            )
        ]
        
        environmental_components = [
            SkincareEnvironmentalComponent(
                id="skin_microbiome",
                name="Skin Microbiome",
                scale_level=SkincareScaleLevel.ENVIRONMENTAL,
                component_type="microbial_community",
                environmental_type=SkincareEnvironmentalFactor.MICROBIOME,
                affected_functions=[SkincareFunctionalAspect.INFLAMMATION],
                properties={"diversity": "variable", "pathogenic_potential": "conditional"}
            )
        ]
        
        return SkincareMultiscaleSchema(
            cellular_components=cellular_components,
            tissue_components=tissue_components,
            environmental_components=environmental_components,
            functional_outcomes=[
                SkincareFunctionalAspect.SEBUM_PRODUCTION,
                SkincareFunctionalAspect.INFLAMMATION
            ]
        )
    
    def _select_template(self, request: SkincareSchemaRequest) -> Optional[SkincareSchemaTemplate]:
        """Select the most appropriate template for the request."""
        use_case_mapping = {
            "anti_aging": "anti_aging",
            "anti-aging": "anti_aging",
            "aging": "anti_aging",
            "wrinkles": "anti_aging",
            "barrier": "barrier_function",
            "barrier_function": "barrier_function",
            "hydration": "barrier_function",
            "moisture": "barrier_function",
            "acne": "acne_treatment",
            "acne_treatment": "acne_treatment",
            "sebum": "acne_treatment",
            "pimples": "acne_treatment"
        }
        
        template_id = use_case_mapping.get(request.use_case.lower())
        return self._templates.get(template_id) if template_id else None
    
    def _customize_template(self, template: SkincareSchemaTemplate, request: SkincareSchemaRequest) -> SkincareMultiscaleSchema:
        """Customize a template based on the specific request."""
        schema = template.schema.model_copy(deep=True)
        
        # Filter scale levels if specified
        if request.target_scale_levels:
            if SkincareScaleLevel.MOLECULAR not in request.target_scale_levels:
                schema.molecular_components = []
            if SkincareScaleLevel.CELLULAR not in request.target_scale_levels:
                schema.cellular_components = []
            if SkincareScaleLevel.TISSUE not in request.target_scale_levels:
                schema.tissue_components = []
            if SkincareScaleLevel.ENVIRONMENTAL not in request.target_scale_levels:
                schema.environmental_components = []
        
        # Filter by focus areas
        if request.focus_areas:
            schema.functional_outcomes = [
                outcome for outcome in schema.functional_outcomes 
                if outcome in request.focus_areas
            ]
        
        return schema
    
    def _create_schema_from_scratch(self, request: SkincareSchemaRequest) -> SkincareMultiscaleSchema:
        """Create a new schema from scratch based on the request."""
        # This is a basic implementation - in practice, this could use ML/AI
        # to analyze data sources and suggest appropriate components
        
        schema = SkincareMultiscaleSchema(functional_outcomes=request.focus_areas)
        
        # Add basic components based on target scale levels
        for scale_level in request.target_scale_levels:
            if scale_level == SkincareScaleLevel.MOLECULAR:
                # Add basic molecular components
                pass
            elif scale_level == SkincareScaleLevel.CELLULAR:
                # Add basic cellular components
                pass
            # ... etc
        
        return schema
    
    def _enhance_with_data_sources(self, schema: SkincareMultiscaleSchema, data_sources: List[DataSource]) -> SkincareMultiscaleSchema:
        """Enhance schema based on available data sources."""
        # Analyze data source columns to suggest additional components
        # This is a placeholder for more sophisticated data analysis
        
        for data_source in data_sources:
            # Look for skincare-related columns
            columns = [col.lower() for col in data_source.columns]
            
            if any(col in columns for col in ['age', 'wrinkles', 'elasticity']):
                # Suggest anti-aging components if not present
                pass
            
            if any(col in columns for col in ['hydration', 'moisture', 'tewl']):
                # Suggest barrier function components if not present
                pass
        
        return schema
    
    def _generate_recommendations(self, schema: SkincareMultiscaleSchema, request: SkincareSchemaRequest) -> List[str]:
        """Generate recommendations for improving the schema."""
        recommendations = []
        
        total_components = (
            len(schema.molecular_components) + 
            len(schema.cellular_components) + 
            len(schema.tissue_components) + 
            len(schema.environmental_components)
        )
        
        if total_components < 3:
            recommendations.append("Consider adding more components across different scales for a comprehensive model")
        
        if not schema.interactions:
            recommendations.append("Add interactions between components to model relationships and dependencies")
        
        if not request.include_environmental and len(schema.environmental_components) == 0:
            recommendations.append("Consider including environmental factors for a more complete model")
        
        if len(schema.functional_outcomes) < 2:
            recommendations.append("Define multiple functional outcomes to track various aspects of skin health")
        
        return recommendations