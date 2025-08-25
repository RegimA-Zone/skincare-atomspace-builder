"""Pydantic models for the AtomSpace Builder API."""

from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from .enums import WriterType


class PropertyKey(BaseModel):
    name: str
    type: str
    cardinality: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


class VertexLabel(BaseModel):
    name: str
    properties: List[str]
    primary_keys: Optional[List[str]] = None
    nullable_keys: Optional[List[str]] = None
    id_strategy: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


class EdgeLabel(BaseModel):
    name: str
    source_label: str
    target_label: str
    properties: Optional[List[str]] = None
    sort_keys: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None


class SchemaDefinition(BaseModel):
    property_keys: List[PropertyKey]
    vertex_labels: List[VertexLabel]
    edge_labels: List[EdgeLabel]


class HugeGraphLoadResponse(BaseModel):
    job_id: str
    status: str
    message: str
    details: Optional[Dict[str, Any]] = None
    output_files: Optional[List[str]] = None
    output_dir: Optional[str] = None
    schema_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    writer_type: Optional[str] = None


class JobSelectionRequest(BaseModel):
    job_id: str


class UploadSession(BaseModel):
    session_id: str
    created_at: datetime
    expires_at: datetime
    uploaded_files: List[str] = []
    status: str = "active"  # active, expired, consumed
    metadata: Dict[str, Any] = {}


class UploadFileInfo(BaseModel):
    filename: str
    size: int
    uploaded_at: str


class UploadResponse(BaseModel):
    session_id: str
    uploaded_files: List[UploadFileInfo]
    total_files: int
    files_in_session: List[str]

class FileInfo(BaseModel):
    name: str
    size: int
    type: str

class DataSource(BaseModel):
    id: str
    file: FileInfo
    columns: List[str]
    sampleRow: List[str]


class SessionStatusResponse(BaseModel):
    session_id: str
    status: str
    expires_at: str
    files: List[UploadFileInfo]  # Original file info
    total_files: int
    datasources: List[DataSource]  # New preprocessed data sources

class CreateSessionResponse(BaseModel):
    session_id: str
    expires_at: str
    upload_url: str


class GraphInfo(BaseModel):
    job_id: str
    writer_type: str
    node_count: int
    edge_count: int
    dataset_count: int
    data_size: str
    imported_on: str
    top_entities: List[Dict[str, Any]]
    top_connections: List[Dict[str, Any]]
    frequent_relationships: List[Dict[str, Any]]
    schema: Dict[str, Any]


class AnnotationSchema(BaseModel):
    job_id: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


class JobMetadata(BaseModel):
    job_id: str
    writer_type: str
    created_at: str
    neo4j_config: Optional[Dict[str, Any]] = None


class Neo4jLoadResult(BaseModel):
    status: str
    job_id: Optional[str] = None
    tenant_id: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class DeleteJobResponse(BaseModel):
    message: str
    history: Dict[str, Any]
    directory_deleted: bool
    selected_job_affected: bool
    new_selected_job: Optional[str] = None


class HistoryResponse(BaseModel):
    selected_job_id: str
    history: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    status: str


class SchemaConversionResponse(BaseModel):
    status: str
    schema_groovy: str


# Schema Suggestion Models
class FileInfo(BaseModel):
    name: str
    size: int
    type: str


class DataSource(BaseModel):
    id: str
    file: FileInfo
    columns: List[str]
    sampleRow: List[str]


class SchemaProperty(BaseModel):
    name: Optional[str] = None
    col: str
    type: str  # 'int' | 'text' | 'double'
    checked: bool = True


class NodeData(BaseModel):
    name: Optional[str] = None
    table: Optional[str] = None
    primaryKey: Optional[str] = None
    properties: Dict[str, SchemaProperty]


class SchemaNode(BaseModel):
    id: str
    type: str = "entity"
    position: Dict[str, int] = {"x": 0, "y": 0}
    data: NodeData


class RelationData(BaseModel):
    name: Optional[str] = None
    reversed: Optional[bool] = None
    table: Optional[str] = None
    source: Optional[str] = None
    target: Optional[str] = None
    primaryKey: Optional[str] = None
    error: Optional[Dict[str, str]] = None
    properties: Dict[str, SchemaProperty]


class SchemaEdge(BaseModel):
    id: str
    type: str = "relation"
    source: str
    target: str
    name: str
    data: Dict[str, RelationData]


class SuggestedSchema(BaseModel):
    nodes: List[SchemaNode]
    edges: List[SchemaEdge]


class SuggestSchemaRequest(BaseModel):
    dataSources: List[DataSource]


class SuggestSchemaResponse(BaseModel):
    schema: SuggestedSchema
    message: str = "Schema generated successfully"


# Skincare Multiscale Model Schemas
class SkincareScaleLevel(str, Enum):
    """Different scale levels in skincare modeling."""
    MOLECULAR = "molecular"
    CELLULAR = "cellular" 
    TISSUE = "tissue"
    FUNCTIONAL = "functional"
    ENVIRONMENTAL = "environmental"


class SkincareMolecularType(str, Enum):
    """Types of molecular components in skin."""
    PROTEIN = "protein"
    LIPID = "lipid"
    PEPTIDE = "peptide"
    ENZYME = "enzyme"
    DNA_RNA = "dna_rna"
    ANTIOXIDANT = "antioxidant"
    VITAMIN = "vitamin"
    ACID = "acid"


class SkincareCellularType(str, Enum):
    """Types of cells in skin."""
    KERATINOCYTE = "keratinocyte"
    FIBROBLAST = "fibroblast"
    MELANOCYTE = "melanocyte"
    LANGERHANS = "langerhans"
    STEM_CELL = "stem_cell"
    IMMUNE_CELL = "immune_cell"
    SEBOCYTE = "sebocyte"


class SkincareTissueLevel(str, Enum):
    """Skin tissue layers and structures."""
    STRATUM_CORNEUM = "stratum_corneum"
    STRATUM_GRANULOSUM = "stratum_granulosum"
    STRATUM_SPINOSUM = "stratum_spinosum"
    STRATUM_BASALE = "stratum_basale"
    PAPILLARY_DERMIS = "papillary_dermis"
    RETICULAR_DERMIS = "reticular_dermis"
    HYPODERMIS = "hypodermis"
    SEBACEOUS_GLAND = "sebaceous_gland"
    HAIR_FOLLICLE = "hair_follicle"


class SkincareFunctionalAspect(str, Enum):
    """Functional aspects of skin."""
    BARRIER_FUNCTION = "barrier_function"
    MOISTURE_RETENTION = "moisture_retention"
    UV_PROTECTION = "uv_protection"
    WOUND_HEALING = "wound_healing"
    AGING_PROCESS = "aging_process"
    PIGMENTATION = "pigmentation"
    SEBUM_PRODUCTION = "sebum_production"
    INFLAMMATION = "inflammation"


class SkincareEnvironmentalFactor(str, Enum):
    """Environmental factors affecting skin."""
    UV_RADIATION = "uv_radiation"
    POLLUTION = "pollution"
    HUMIDITY = "humidity"
    TEMPERATURE = "temperature"
    MICROBIOME = "microbiome"
    SKINCARE_PRODUCT = "skincare_product"
    LIFESTYLE = "lifestyle"


class SkincareComponent(BaseModel):
    """Base model for skincare components across scales."""
    id: str
    name: str
    scale_level: SkincareScaleLevel
    component_type: str
    properties: Dict[str, Any] = {}
    interactions: List[str] = []  # IDs of other components this interacts with
    affected_functions: List[SkincareFunctionalAspect] = []


class SkincareMolecularComponent(SkincareComponent):
    """Molecular-level skincare component."""
    molecular_type: SkincareMolecularType
    molecular_weight: Optional[float] = None
    concentration_range: Optional[Dict[str, float]] = None  # min, max, optimal
    penetration_depth: Optional[str] = None
    stability_factors: List[str] = []


class SkincareCellularComponent(SkincareComponent):
    """Cellular-level skincare component."""
    cellular_type: SkincareCellularType
    cell_cycle_stage: Optional[str] = None
    proliferation_rate: Optional[float] = None
    differentiation_markers: List[str] = []
    metabolic_activity: Optional[str] = None


class SkincareTissueComponent(SkincareComponent):
    """Tissue-level skincare component."""
    tissue_level: SkincareTissueLevel
    thickness: Optional[float] = None
    barrier_strength: Optional[float] = None
    cell_composition: List[str] = []  # Cellular components present
    extracellular_matrix: List[str] = []


class SkincareEnvironmentalComponent(SkincareComponent):
    """Environmental factor component."""
    environmental_type: SkincareEnvironmentalFactor
    exposure_level: Optional[str] = None  # high, medium, low
    duration: Optional[str] = None
    protective_measures: List[str] = []


class SkincareInteraction(BaseModel):
    """Represents interaction between skincare components."""
    id: str
    source_component: str
    target_component: str
    interaction_type: str  # stimulates, inhibits, modulates, protects
    strength: Optional[float] = None  # 0.0 to 1.0
    mechanism: Optional[str] = None
    conditions: List[str] = []  # Required conditions for interaction
    scale_crossing: bool = False  # True if interaction crosses scale levels


class SkincareMultiscaleSchema(BaseModel):
    """Complete multiscale schema for skincare modeling."""
    components: List[SkincareComponent] = []
    molecular_components: List[SkincareMolecularComponent] = []
    cellular_components: List[SkincareCellularComponent] = []
    tissue_components: List[SkincareTissueComponent] = []
    environmental_components: List[SkincareEnvironmentalComponent] = []
    interactions: List[SkincareInteraction] = []
    scale_relationships: Dict[str, List[str]] = {}  # How scales connect
    functional_outcomes: List[SkincareFunctionalAspect] = []


class SkincareSchemaTemplate(BaseModel):
    """Pre-defined schema template for common skincare scenarios."""
    template_id: str
    name: str
    description: str
    use_case: str  # anti-aging, acne, moisturizing, etc.
    target_scale_levels: List[SkincareScaleLevel]
    schema: SkincareMultiscaleSchema
    metadata: Dict[str, Any] = {}


class SkincareSchemaRequest(BaseModel):
    """Request to generate skincare-specific schema."""
    use_case: str
    target_scale_levels: List[SkincareScaleLevel] = []
    include_environmental: bool = True
    focus_areas: List[SkincareFunctionalAspect] = []
    data_sources: List[DataSource] = []


class SkincareSchemaResponse(BaseModel):
    """Response with generated skincare schema."""
    schema: SkincareMultiscaleSchema
    template_used: Optional[str] = None
    recommendations: List[str] = []
    message: str = "Skincare schema generated successfully"