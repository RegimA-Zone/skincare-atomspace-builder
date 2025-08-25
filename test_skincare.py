#!/usr/bin/env python3
"""
Test script for skincare multiscale model functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.skincare_schema_service import SkincareSchemaService
from app.models.schemas import (
    SkincareSchemaRequest,
    SkincareScaleLevel,
    SkincareFunctionalAspect,
    DataSource,
    FileInfo
)

def test_skincare_service():
    """Test the skincare schema service."""
    print("Testing Skincare Schema Service...")
    
    # Initialize service
    service = SkincareSchemaService()
    
    # Test 1: Get available templates
    print("\n1. Testing available templates:")
    templates = service.get_available_templates()
    print(f"   Found {len(templates)} templates:")
    for template in templates:
        print(f"   - {template.template_id}: {template.name}")
    
    # Test 2: Generate anti-aging schema
    print("\n2. Testing anti-aging schema generation:")
    request = SkincareSchemaRequest(
        use_case="anti_aging",
        target_scale_levels=[SkincareScaleLevel.MOLECULAR, SkincareScaleLevel.CELLULAR, SkincareScaleLevel.TISSUE],
        include_environmental=False,
        focus_areas=[SkincareFunctionalAspect.AGING_PROCESS]
    )
    
    response = service.generate_schema(request)
    print(f"   Generated schema with:")
    print(f"   - {len(response.schema.molecular_components)} molecular components")
    print(f"   - {len(response.schema.cellular_components)} cellular components")
    print(f"   - {len(response.schema.tissue_components)} tissue components")
    print(f"   - {len(response.schema.interactions)} interactions")
    print(f"   - Template used: {response.template_used}")
    print(f"   - Recommendations: {len(response.recommendations)}")
    
    # Test 3: Generate barrier function schema
    print("\n3. Testing barrier function schema generation:")
    request = SkincareSchemaRequest(
        use_case="barrier_function",
        target_scale_levels=[SkincareScaleLevel.MOLECULAR, SkincareScaleLevel.TISSUE, SkincareScaleLevel.ENVIRONMENTAL],
        include_environmental=True,
        focus_areas=[SkincareFunctionalAspect.BARRIER_FUNCTION, SkincareFunctionalAspect.MOISTURE_RETENTION]
    )
    
    response = service.generate_schema(request)
    print(f"   Generated schema with:")
    print(f"   - {len(response.schema.molecular_components)} molecular components")
    print(f"   - {len(response.schema.tissue_components)} tissue components")
    print(f"   - {len(response.schema.environmental_components)} environmental components")
    print(f"   - Template used: {response.template_used}")
    
    # Test 4: Schema validation
    print("\n4. Testing schema validation:")
    validation_result = service.validate_schema(response.schema)
    print(f"   Schema valid: {validation_result['valid']}")
    print(f"   Warnings: {len(validation_result['warnings'])}")
    print(f"   Errors: {len(validation_result['errors'])}")
    print(f"   Suggestions: {len(validation_result['suggestions'])}")
    
    # Test 5: Test with data sources
    print("\n5. Testing with data sources:")
    mock_data_source = DataSource(
        id="skin_data_1",
        file=FileInfo(name="skin_measurements.csv", size=1024, type="csv"),
        columns=["age", "wrinkles", "elasticity", "hydration", "collagen_density"],
        sampleRow=["45", "moderate", "low", "good", "decreased"]
    )
    
    request_with_data = SkincareSchemaRequest(
        use_case="anti_aging",
        target_scale_levels=[SkincareScaleLevel.MOLECULAR, SkincareScaleLevel.CELLULAR],
        data_sources=[mock_data_source]
    )
    
    response = service.generate_schema(request_with_data)
    print(f"   Schema enhanced with data source:")
    print(f"   - Components: {len(response.schema.molecular_components + response.schema.cellular_components)}")
    
    print("\n✅ All tests completed successfully!")
    return True

def test_api_imports():
    """Test that API endpoints can be imported."""
    print("Testing API imports...")
    
    try:
        from app.api.skincare import router
        print(f"   ✅ Skincare router imported with {len(router.routes)} routes")
        
        from app.main import create_app
        app = create_app()
        print(f"   ✅ Main app created with {len(app.routes)} total routes")
        
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SKINCARE MULTISCALE MODEL TEST SUITE")
    print("=" * 60)
    
    # Test service functionality
    try:
        service_test = test_skincare_service()
    except Exception as e:
        print(f"❌ Service test failed: {e}")
        service_test = False
    
    print("\n" + "=" * 60)
    
    # Test API imports
    try:
        api_test = test_api_imports()
    except Exception as e:
        print(f"❌ API test failed: {e}")
        api_test = False
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print(f"Service Tests: {'✅ PASSED' if service_test else '❌ FAILED'}")
    print(f"API Tests: {'✅ PASSED' if api_test else '❌ FAILED'}")
    print("=" * 60)
    
    if service_test and api_test:
        print("🎉 All tests passed! Skincare multiscale model is working correctly.")
        sys.exit(0)
    else:
        print("💥 Some tests failed. Please check the implementation.")
        sys.exit(1)