# Skincare Multiscale Model Documentation

## Overview

The skincare multiscale model extends the AtomSpace Builder to support domain-specific modeling of skin biology and skincare effects across multiple biological scales. This implementation provides specialized schemas, components, and relationships for modeling skin structure and function from molecular to tissue level.

## Multiscale Levels

### 1. Molecular Level
- **Components**: Proteins (collagen, elastin, keratin), lipids (ceramides), vitamins (retinol), acids, peptides
- **Focus**: Individual molecules and their properties
- **Examples**: Collagen degradation, retinol penetration, ceramide barrier function

### 2. Cellular Level  
- **Components**: Keratinocytes, fibroblasts, melanocytes, sebocytes, immune cells
- **Focus**: Cell behavior, proliferation, differentiation
- **Examples**: Fibroblast collagen production, melanocyte pigmentation, sebocyte oil production

### 3. Tissue Level
- **Components**: Epidermis layers, dermis, sebaceous glands, hair follicles
- **Focus**: Tissue structure and organization
- **Examples**: Stratum corneum barrier, dermal thickness, gland activity

### 4. Environmental Level
- **Components**: UV radiation, pollution, humidity, skincare products, microbiome
- **Focus**: External factors affecting skin
- **Examples**: UV damage, product efficacy, microbial interactions

## Schema Templates

### Anti-Aging Template
Models aging processes and anti-aging interventions:
- **Molecular**: Collagen, elastin, retinol, peptides
- **Cellular**: Fibroblasts, keratinocytes
- **Tissue**: Dermis structure
- **Interactions**: Retinol → fibroblast stimulation → collagen production

### Barrier Function Template
Models skin barrier protection and hydration:
- **Molecular**: Ceramides, natural moisturizing factors
- **Tissue**: Stratum corneum structure
- **Environmental**: Humidity, TEWL (trans-epidermal water loss)
- **Interactions**: Ceramide organization → barrier strength

### Acne Treatment Template
Models acne formation and treatment mechanisms:
- **Cellular**: Sebocytes, immune cells
- **Tissue**: Sebaceous glands, hair follicles
- **Environmental**: Microbiome (P. acnes)
- **Interactions**: Hormones → sebocyte activity → sebum production

## API Endpoints

### Schema Generation
```http
POST /api/skincare/schema/generate
```
Generate a customized skincare schema based on use case and requirements.

**Request Body:**
```json
{
  "use_case": "anti_aging",
  "target_scale_levels": ["molecular", "cellular", "tissue"],
  "include_environmental": true,
  "focus_areas": ["aging_process", "barrier_function"],
  "data_sources": []
}
```

### Templates
```http
GET /api/skincare/templates
GET /api/skincare/templates/{template_id}
```
Retrieve available schema templates or a specific template.

### Validation
```http
POST /api/skincare/schema/validate
```
Validate a skincare schema for completeness and consistency.

### Reference Data
```http
GET /api/skincare/scale-levels
GET /api/skincare/functional-aspects
GET /api/skincare/component-types
GET /api/skincare/use-cases
```
Get reference data for building skincare schemas.

## Component Types

### Molecular Components
- `SkincareMolecularComponent`: Molecules with properties like molecular weight, concentration ranges, penetration depth
- **Types**: protein, lipid, peptide, enzyme, vitamin, acid, antioxidant

### Cellular Components  
- `SkincareCellularComponent`: Cells with properties like proliferation rate, differentiation markers
- **Types**: keratinocyte, fibroblast, melanocyte, sebocyte, immune_cell, stem_cell

### Tissue Components
- `SkincareTissueComponent`: Tissues with properties like thickness, barrier strength
- **Levels**: stratum_corneum, epidermis layers, dermis layers, glands

### Environmental Components
- `SkincareEnvironmentalComponent`: External factors with exposure levels and protective measures
- **Types**: uv_radiation, pollution, humidity, microbiome, skincare_product

## Interactions

### Interaction Types
- **stimulates**: Component A enhances activity of component B
- **inhibits**: Component A reduces activity of component B  
- **modulates**: Component A changes behavior of component B
- **protects**: Component A shields component B from damage
- **produces**: Component A creates component B

### Scale-Crossing Interactions
The system supports interactions that cross scale boundaries:
- Molecular → Cellular: Retinol stimulating fibroblasts
- Cellular → Tissue: Fibroblasts affecting dermal structure
- Environmental → Molecular: UV degrading collagen

## Use Cases

### 1. Anti-Aging Research
Model how skincare ingredients affect aging processes:
```python
request = SkincareSchemaRequest(
    use_case="anti_aging",
    target_scale_levels=[SkincareScaleLevel.MOLECULAR, SkincareScaleLevel.CELLULAR],
    focus_areas=[SkincareFunctionalAspect.AGING_PROCESS]
)
```

### 2. Barrier Function Studies
Model skin barrier protection mechanisms:
```python
request = SkincareSchemaRequest(
    use_case="barrier_function", 
    target_scale_levels=[SkincareScaleLevel.MOLECULAR, SkincareScaleLevel.TISSUE],
    focus_areas=[SkincareFunctionalAspect.BARRIER_FUNCTION, SkincareFunctionalAspect.MOISTURE_RETENTION]
)
```

### 3. Product Development
Model how new skincare formulations affect skin:
```python
request = SkincareSchemaRequest(
    use_case="moisturizing",
    include_environmental=True,
    data_sources=[product_test_data]
)
```

## Integration with Existing System

The skincare multiscale model integrates seamlessly with the existing AtomSpace Builder:

### Multi-Backend Support
- Works with Neo4j, HugeGraph, and MORK backends
- Skincare schemas can be exported to any supported format

### Multi-Tenancy
- Each tenant can have their own skincare schemas
- Isolation maintained across all skincare operations

### Session Management
- Skincare schema generation works with existing session system
- Supports batch processing of multiple skincare datasets

### Schema Conversion
- Skincare schemas can be converted to HugeGraph format
- Compatible with existing graph loading pipelines

## Example Workflow

1. **Identify Use Case**: Determine the skincare research question (anti-aging, barrier function, etc.)

2. **Select Scale Levels**: Choose which biological scales are relevant (molecular, cellular, tissue, environmental)

3. **Generate Schema**: Use the API to generate an appropriate schema template

4. **Customize Schema**: Add specific components and interactions based on your data

5. **Validate Schema**: Check for completeness and consistency

6. **Load Data**: Use existing AtomSpace Builder functionality to load your skincare data using the generated schema

7. **Analyze**: Perform graph analytics on the multiscale skincare model

## Best Practices

### Schema Design
- Include multiple scale levels for comprehensive modeling
- Define clear interactions between components
- Specify functional outcomes to track skin health metrics

### Component Selection
- Choose components relevant to your specific research question
- Include environmental factors when studying real-world conditions
- Balance detail with computational complexity

### Validation
- Always validate schemas before using them for data loading
- Pay attention to warnings and suggestions for schema improvement
- Ensure all interactions reference valid components

### Performance
- Start with template schemas and customize as needed
- Use targeted scale levels to reduce schema complexity
- Consider data volume when designing comprehensive schemas