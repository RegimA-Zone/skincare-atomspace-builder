"""API endpoints for skincare multiscale modeling."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
import logging
from ..models.schemas import (
    SkincareSchemaRequest,
    SkincareSchemaResponse, 
    SkincareSchemaTemplate,
    SkincareMultiscaleSchema
)
from ..services.skincare_schema_service import SkincareSchemaService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/skincare", tags=["skincare"])

# Dependency to get skincare schema service
def get_skincare_service() -> SkincareSchemaService:
    return SkincareSchemaService()


@router.post("/schema/generate", response_model=SkincareSchemaResponse)
async def generate_skincare_schema(
    request: SkincareSchemaRequest,
    service: SkincareSchemaService = Depends(get_skincare_service)
):
    """Generate a skincare-specific multiscale schema."""
    try:
        logger.info(f"Generating skincare schema for use case: {request.use_case}")
        response = service.generate_schema(request)
        logger.info(f"Schema generated successfully with {len(response.schema.molecular_components + response.schema.cellular_components + response.schema.tissue_components + response.schema.environmental_components)} components")
        return response
    except Exception as e:
        logger.error(f"Failed to generate skincare schema: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate schema: {str(e)}")


@router.get("/templates", response_model=List[SkincareSchemaTemplate])
async def get_skincare_templates(
    service: SkincareSchemaService = Depends(get_skincare_service)
):
    """Get all available skincare schema templates."""
    try:
        templates = service.get_available_templates()
        logger.info(f"Retrieved {len(templates)} skincare templates")
        return templates
    except Exception as e:
        logger.error(f"Failed to retrieve templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve templates: {str(e)}")


@router.get("/templates/{template_id}", response_model=SkincareSchemaTemplate)
async def get_skincare_template(
    template_id: str,
    service: SkincareSchemaService = Depends(get_skincare_service)
):
    """Get a specific skincare schema template by ID."""
    try:
        template = service.get_template(template_id)
        if not template:
            raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
        
        logger.info(f"Retrieved template: {template_id}")
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve template {template_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve template: {str(e)}")


@router.post("/schema/validate", response_model=Dict[str, Any])
async def validate_skincare_schema(
    schema: SkincareMultiscaleSchema,
    service: SkincareSchemaService = Depends(get_skincare_service)
):
    """Validate a skincare multiscale schema."""
    try:
        logger.info("Validating skincare schema")
        validation_result = service.validate_schema(schema)
        logger.info(f"Schema validation completed - Valid: {validation_result['valid']}")
        return validation_result
    except Exception as e:
        logger.error(f"Failed to validate schema: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to validate schema: {str(e)}")


@router.get("/scale-levels")
async def get_scale_levels():
    """Get available scale levels for skincare modeling."""
    from ..models.schemas import SkincareScaleLevel
    
    scale_levels = [
        {
            "value": level.value,
            "description": {
                "molecular": "Proteins, lipids, vitamins, and other molecular components",
                "cellular": "Skin cells like keratinocytes, fibroblasts, melanocytes",
                "tissue": "Skin layers and structures like epidermis, dermis, glands",
                "functional": "Skin functions like barrier protection, aging, healing",
                "environmental": "External factors like UV, pollution, skincare products"
            }.get(level.value, "")
        }
        for level in SkincareScaleLevel
    ]
    
    return {"scale_levels": scale_levels}


@router.get("/functional-aspects")
async def get_functional_aspects():
    """Get available functional aspects for skincare modeling."""
    from ..models.schemas import SkincareFunctionalAspect
    
    aspects = [
        {
            "value": aspect.value,
            "description": {
                "barrier_function": "Skin's protective barrier against external factors",
                "moisture_retention": "Skin's ability to retain and maintain hydration",
                "uv_protection": "Natural and enhanced UV radiation protection",
                "wound_healing": "Skin repair and regeneration processes",
                "aging_process": "Age-related changes in skin structure and function",
                "pigmentation": "Melanin production and skin color regulation",
                "sebum_production": "Oil production by sebaceous glands",
                "inflammation": "Immune responses and inflammatory processes"
            }.get(aspect.value, "")
        }
        for aspect in SkincareFunctionalAspect
    ]
    
    return {"functional_aspects": aspects}


@router.get("/component-types")
async def get_component_types():
    """Get available component types for each scale level."""
    from ..models.schemas import (
        SkincareMolecularType,
        SkincareCellularType,
        SkincareTissueLevel,
        SkincareEnvironmentalFactor
    )
    
    return {
        "molecular_types": [{"value": t.value, "name": t.value.replace("_", " ").title()} for t in SkincareMolecularType],
        "cellular_types": [{"value": t.value, "name": t.value.replace("_", " ").title()} for t in SkincareCellularType],
        "tissue_levels": [{"value": t.value, "name": t.value.replace("_", " ").title()} for t in SkincareTissueLevel],
        "environmental_factors": [{"value": t.value, "name": t.value.replace("_", " ").title()} for t in SkincareEnvironmentalFactor]
    }


@router.get("/use-cases")
async def get_use_cases():
    """Get common skincare use cases with descriptions."""
    use_cases = [
        {
            "id": "anti_aging",
            "name": "Anti-Aging",
            "description": "Modeling aging processes and anti-aging interventions",
            "recommended_scales": ["molecular", "cellular", "tissue"],
            "key_components": ["collagen", "elastin", "retinoids", "peptides"]
        },
        {
            "id": "barrier_function",
            "name": "Barrier Function",
            "description": "Skin barrier protection and hydration maintenance",
            "recommended_scales": ["molecular", "tissue", "environmental"],
            "key_components": ["ceramides", "stratum corneum", "humidity", "TEWL"]
        },
        {
            "id": "acne_treatment",
            "name": "Acne Treatment",
            "description": "Acne formation mechanisms and treatment effects",
            "recommended_scales": ["cellular", "tissue", "environmental"],
            "key_components": ["sebocytes", "P. acnes", "inflammation", "sebaceous glands"]
        },
        {
            "id": "pigmentation",
            "name": "Pigmentation",
            "description": "Melanin production and skin tone regulation",
            "recommended_scales": ["molecular", "cellular", "environmental"],
            "key_components": ["melanocytes", "tyrosinase", "UV exposure", "melanin"]
        },
        {
            "id": "wound_healing",
            "name": "Wound Healing",
            "description": "Skin repair and regeneration processes",
            "recommended_scales": ["cellular", "tissue", "functional"],
            "key_components": ["fibroblasts", "keratinocytes", "collagen synthesis", "angiogenesis"]
        },
        {
            "id": "moisturizing",
            "name": "Moisturizing",
            "description": "Hydration and water retention mechanisms",
            "recommended_scales": ["molecular", "tissue", "environmental"],
            "key_components": ["hyaluronic acid", "glycerin", "natural moisturizing factors", "humidity"]
        }
    ]
    
    return {"use_cases": use_cases}


@router.get("/health")
async def skincare_health_check():
    """Health check for skincare service."""
    try:
        service = get_skincare_service()
        templates = service.get_available_templates()
        return {
            "status": "healthy",
            "service": "skincare_multiscale_modeling",
            "available_templates": len(templates),
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Skincare service health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")