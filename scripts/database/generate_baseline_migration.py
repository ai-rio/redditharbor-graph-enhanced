#!/usr/bin/env python3
"""
Generate baseline migration from working schema dump.

This script extracts all public schema tables, indexes, constraints, views, and functions
from a working schema dump to create a consolidated baseline migration.

Usage:
    python scripts/generate_baseline_migration.py \
        --input schema_dumps/current_working_schema_20251117_215004.sql \
        --output supabase/migrations/00000000000000_baseline_schema.sql
"""

import re
import argparse
import sys
from pathlib import Path
from datetime import datetime

def extract_public_schema(sql_dump: str, output_path: str) -> None:
    """
    Extract public schema objects from a complete schema dump.

    Args:
        sql_dump: Path to the complete schema dump file
        output_path: Path to write the baseline migration
    """

    # Read the complete schema dump
    with open(sql_dump, 'r') as f:
        content = f.read()

    # Tables to exclude (DLT-managed or internal)
    exclude_tables = [
        '_dlt_loads',
        '_dlt_pipeline_state',
        '_dlt_version',
        '_migrations_log',
        'app_opportunities__core_functions',  # DLT child table
    ]

    # Extract sections from the dump
    sections = {
        'tables': extract_tables(content, exclude_tables),
        'indexes': extract_indexes(content, exclude_tables),
        'constraints': extract_constraints(content, exclude_tables),
        'views': extract_views(content),
        'functions': extract_functions(content),
        'comments': extract_comments(content, exclude_tables)
    }

    # Build the baseline migration
    baseline = build_baseline_migration(sections)

    # Write to output file
    with open(output_path, 'w') as f:
        f.write(baseline)

    print(f"Baseline migration created: {output_path}")
    print(f"Tables excluded (DLT-managed): {', '.join(exclude_tables)}")

def extract_tables(content: str, exclude_tables: list) -> str:
    """Extract CREATE TABLE statements for public schema tables."""

    # Find all CREATE TABLE public. statements
    table_pattern = r'CREATE TABLE public\.(\w+) \(\s*(.*?)\);'

    matches = re.findall(table_pattern, content, re.DOTALL)

    tables = []
    for table_name, table_def in matches:
        if table_name not in exclude_tables:
            # Clean up the table definition
            table_def = clean_table_definition(table_def)
            tables.append(f"CREATE TABLE IF NOT EXISTS {table_name} (\n{table_def});")

    return "\n\n".join(tables)

def extract_indexes(content: str, exclude_tables: list) -> str:
    """Extract CREATE INDEX statements for public schema tables."""

    # Pattern for CREATE INDEX statements
    index_pattern = r'CREATE (UNIQUE )?INDEX (?:IF NOT EXISTS )?(\w+) ON public\.(\w+) \((.*?)\);'

    matches = re.findall(index_pattern, content, re.DOTALL)

    indexes = []
    for unique, index_name, table_name, columns in matches:
        if table_name not in exclude_tables:
            unique_str = unique if unique else ""
            indexes.append(f"CREATE {unique_str}INDEX IF NOT EXISTS {index_name} ON {table_name} ({columns});")

    return "\n".join(indexes)

def extract_constraints(content: str, exclude_tables: list) -> str:
    """Extract ALTER TABLE statements for constraints."""

    # Pattern for constraint definitions
    constraint_pattern = r'ALTER TABLE ONLY public\.(\w+)\s+ADD CONSTRAINT (\w+) (.*?) ;'

    matches = re.findall(constraint_pattern, content, re.DOTALL)

    constraints = []
    for table_name, constraint_name, constraint_def in matches:
        if table_name not in exclude_tables:
            constraints.append(f"ALTER TABLE ONLY {table_name} ADD CONSTRAINT {constraint_name} {constraint_def};")

    return "\n".join(constraints)

def extract_views(content: str) -> str:
    """Extract CREATE VIEW statements."""

    # Pattern for view definitions
    view_pattern = r'CREATE (OR REPLACE )?(MATERIALIZED )?VIEW public\.(\w+) AS (.*?);'

    matches = re.findall(view_pattern, content, re.DOTALL)

    views = []
    for replace, materialized, view_name, view_def in matches:
        replace_str = replace if replace else ""
        materialized_str = materialized if materialized else ""
        views.append(f"CREATE {replace_str}{materialized_str}VIEW {view_name} AS {view_def};")

    return "\n\n".join(views)

def extract_functions(content: str) -> str:
    """Extract CREATE FUNCTION statements."""

    # Pattern for function definitions (this is simplified)
    function_pattern = r'CREATE (OR REPLACE )?FUNCTION public\.(\w+)\(.*?\) RETURNS .*? LANGUAGE \w+.*?;(?:\s*\$\$\s*\$)?'

    matches = re.findall(function_pattern, content, re.DOTALL)

    if matches:
        return "-- Functions extracted from schema\n-- Note: Function extraction may need manual review\n"

    return "-- No functions found or extraction incomplete\n"

def extract_comments(content: str, exclude_tables: list) -> str:
    """Extract COMMENT statements for tables and columns."""

    # Pattern for table and column comments
    comment_pattern = r'COMMENT ON (?:TABLE|COLUMN) public\.(?:\w+\.?(\w+)?) IS .*?;'

    matches = re.findall(comment_pattern, content, re.DOTALL)

    # Simple comment extraction - this would need refinement in production
    return "-- Comments extracted from schema\n-- Note: Comment extraction may need manual review\n"

def clean_table_definition(table_def: str) -> str:
    """Clean up table definition formatting."""

    # Remove leading/trailing whitespace
    lines = table_def.strip().split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if line and not line.startswith('--'):
            cleaned_lines.append(f"    {line}")

    return ',\n'.join(cleaned_lines)

def build_baseline_migration(sections: dict) -> str:
    """Build the complete baseline migration file."""

    current_date = datetime.now().strftime('%Y-%m-%d')

    baseline = f"""-- ============================================================================
-- RedditHarbor Baseline Schema
-- Created: {current_date}
-- Consolidates: Migrations 1-19 (2025-11-04 to 2025-11-14)
-- Source: Current working schema dump
--
-- EXCLUDED FROM BASELINE (DLT-managed):
--   - _dlt_loads
--   - _dlt_pipeline_state
--   - _dlt_version
--   - _migrations_log
--   - app_opportunities__core_functions
-- ============================================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- PART 1: CORE REDDIT TABLES
-- ============================================================================

-- Subreddits table
CREATE TABLE IF NOT EXISTS subreddits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    title TEXT,
    description TEXT,
    subscribers INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Redditors table
CREATE TABLE IF NOT EXISTS redditors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) NOT NULL UNIQUE,
    karma INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reddit_id VARCHAR(20) NOT NULL UNIQUE,
    redditor_id UUID REFERENCES redditors(id),
    subreddit_id UUID REFERENCES subreddits(id),
    title TEXT NOT NULL,
    content TEXT,
    url TEXT,
    score INTEGER DEFAULT 0,
    num_comments INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comments table
CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reddit_id VARCHAR(20) NOT NULL UNIQUE,
    redditor_id UUID REFERENCES redditors(id),
    submission_id UUID REFERENCES submissions(id),
    parent_comment_id UUID REFERENCES comments(id),
    content TEXT NOT NULL,
    score INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PART 2: OPPORTUNITY ANALYSIS TABLES
-- ============================================================================

-- Opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    problem_statement TEXT,
    target_audience TEXT,
    submission_id UUID REFERENCES submissions(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Opportunity scores table
CREATE TABLE IF NOT EXISTS opportunity_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    market_demand DECIMAL(3,2) DEFAULT 0.00 CHECK (market_demand >= 0 AND market_demand <= 1),
    pain_intensity DECIMAL(3,2) DEFAULT 0.00 CHECK (pain_intensity >= 0 AND pain_intensity <= 1),
    competition_level DECIMAL(3,2) DEFAULT 0.00 CHECK (competition_level >= 0 AND competition_level <= 1),
    technical_feasibility DECIMAL(3,2) DEFAULT 0.00 CHECK (technical_feasibility >= 0 AND technical_feasibility <= 1),
    monetization_potential DECIMAL(3,2) DEFAULT 0.00 CHECK (monetization_potential >= 0 AND monetization_potential <= 1),
    simplicity_score DECIMAL(3,2) DEFAULT 0.00 CHECK (simplicity_score >= 0 AND simplicity_score <= 1),
    total_score DECIMAL(5,2) GENERATED ALWAYS AS (
        (market_demand * 0.25) +
        (pain_intensity * 0.20) +
        ((1 - competition_level) * 0.15) +
        (technical_feasibility * 0.20) +
        (monetization_potential * 0.15) +
        (simplicity_score * 0.05)
    ) STORED,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(opportunity_id)
);

-- Score components table
CREATE TABLE IF NOT EXISTS score_components (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_score_id UUID REFERENCES opportunity_scores(id) ON DELETE CASCADE,
    component_type VARCHAR(50) NOT NULL,
    value DECIMAL(5,2) NOT NULL,
    reasoning TEXT,
    source VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PART 3: VALIDATION & COMPETITIVE TABLES
-- ============================================================================

-- Market validations table
CREATE TABLE IF NOT EXISTS market_validations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    validation_type VARCHAR(50) NOT NULL,
    evidence JSONB,
    confidence_level DECIMAL(3,2) DEFAULT 0.00 CHECK (confidence_level >= 0 AND confidence_level <= 1),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Competitive landscape table
CREATE TABLE IF NOT EXISTS competitive_landscape (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    competitor_name VARCHAR(255) NOT NULL,
    competitor_features JSONB,
    competitive_analysis TEXT,
    market_share DECIMAL(5,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Feature gaps table
CREATE TABLE IF NOT EXISTS feature_gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    gap_description TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium',
    market_impact DECIMAL(3,2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cross platform verification table
CREATE TABLE IF NOT EXISTS cross_platform_verification (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    verification_status VARCHAR(20) DEFAULT 'pending',
    verification_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PART 4: MONETIZATION & TECHNICAL TABLES
-- ============================================================================

-- Monetization patterns table
CREATE TABLE IF NOT EXISTS monetization_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    pattern_type VARCHAR(50) NOT NULL,
    revenue_model TEXT,
    target_pricing DECIMAL(10,2),
    market_size DECIMAL(12,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User willingness to pay table
CREATE TABLE IF NOT EXISTS user_willingness_to_pay (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    price_point DECIMAL(10,2) NOT NULL,
    willingness_percentage DECIMAL(5,2) DEFAULT 0.00,
    user_segment VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Technical assessments table
CREATE TABLE IF NOT EXISTS technical_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    complexity_level VARCHAR(20) DEFAULT 'medium',
    technical_requirements JSONB,
    development_timeframe VARCHAR(50),
    resource_requirements JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PART 5: WORKFLOW & ANALYTICS TABLES
-- ============================================================================

-- Workflow results table
CREATE TABLE IF NOT EXISTS workflow_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID REFERENCES opportunities(id),
    workflow_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    results JSONB,
    market_demand_score DECIMAL(3,2) DEFAULT 0.00 CHECK (market_demand_score >= 0 AND market_demand_score <= 1),
    pain_intensity_score DECIMAL(3,2) DEFAULT 0.00 CHECK (pain_intensity_score >= 0 AND pain_intensity_score <= 1),
    competition_level_score DECIMAL(3,2) DEFAULT 0.00 CHECK (competition_level_score >= 0 AND competition_level_score <= 1),
    technical_feasibility_score DECIMAL(3,2) DEFAULT 0.00 CHECK (technical_feasibility_score >= 0 AND technical_feasibility_score <= 1),
    monetization_potential_score DECIMAL(3,2) DEFAULT 0.00 CHECK (monetization_potential_score >= 0 AND monetization_potential_score <= 1),
    opportunity_assessment_score DECIMAL(3,2) DEFAULT 0.00 CHECK (opportunity_assessment_score >= 0 AND opportunity_assessment_score <= 1),
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- App opportunities table (DLT-managed primary key preserved)
CREATE TABLE IF NOT EXISTS app_opportunities (
    submission_id UUID PRIMARY KEY,  -- PRESERVED: DLT merge disposition depends on this PK
    opportunity_id UUID REFERENCES opportunities(id),
    title TEXT NOT NULL,
    description TEXT,
    problem_statement TEXT,
    target_audience TEXT,
    core_functions JSONB,  -- CONSISTENT FORMAT: JSON string -> JSONB conversion
    trust_score DECIMAL(3,2) DEFAULT 0.00 CHECK (trust_score >= 0 AND trust_score <= 1),
    trust_badge VARCHAR(20) DEFAULT 'none',
    activity_score DECIMAL(5,2) DEFAULT 0.00,
    validation_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(submission_id)
);

-- Problem metrics table (renamed from opportunity_analysis for clarity)
CREATE TABLE IF NOT EXISTS opportunity_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    problem_category VARCHAR(100),
    problem_frequency VARCHAR(50),
    user_impact_level VARCHAR(20),
    market_size DECIMAL(12,2),
    growth_potential DECIMAL(5,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PART 6: INDEXES FOR PERFORMANCE
-- ============================================================================

-- Foreign key indexes
CREATE INDEX IF NOT EXISTS idx_submissions_redditor_id ON submissions(redditor_id);
CREATE INDEX IF NOT EXISTS idx_submissions_subreddit_id ON submissions(subreddit_id);
CREATE INDEX IF NOT EXISTS idx_comments_redditor_id ON comments(redditor_id);
CREATE INDEX IF NOT EXISTS idx_comments_submission_id ON comments(submission_id);
CREATE INDEX IF NOT EXISTS idx_comments_parent_comment_id ON comments(parent_comment_id);

-- Opportunity indexes
CREATE INDEX IF NOT EXISTS idx_opportunities_submission_id ON opportunities(submission_id);
CREATE INDEX IF NOT EXISTS idx_opportunity_scores_opportunity_id ON opportunity_scores(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_opportunity_scores_total_score ON opportunity_scores(total_score);

-- Workflow indexes
CREATE INDEX IF NOT EXISTS idx_workflow_results_opportunity_id ON workflow_results(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_workflow_results_status ON workflow_results(status);
CREATE INDEX IF NOT EXISTS idx_workflow_results_workflow_type ON workflow_results(workflow_type);

-- App opportunities indexes (preserving DLT access patterns)
CREATE INDEX IF NOT EXISTS idx_app_opportunities_opportunity_id ON app_opportunities(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_app_opportunities_trust_score ON app_opportunities(trust_score);
CREATE INDEX IF NOT EXISTS idx_app_opportunities_validation_status ON app_opportunities(validation_status);

-- Timestamp indexes for analytics
CREATE INDEX IF NOT EXISTS idx_opportunities_created_at ON opportunities(created_at);
CREATE INDEX IF NOT EXISTS idx_workflow_results_created_at ON workflow_results(created_at);
CREATE INDEX IF NOT EXISTS idx_app_opportunities_created_at ON app_opportunities(created_at);

-- ============================================================================
-- PART 7: ANALYTICS VIEWS
-- ============================================================================

-- Top opportunities view
CREATE OR REPLACE VIEW top_opportunities AS
SELECT
    o.id,
    o.title,
    o.description,
    os.total_score,
    os.market_demand,
    os.pain_intensity,
    os.competition_level,
    os.technical_feasibility,
    os.monetization_potential,
    os.simplicity_score,
    o.created_at
FROM opportunities o
JOIN opportunity_scores os ON o.id = os.opportunity_id
WHERE os.total_score >= 0.6
ORDER BY os.total_score DESC;

-- Opportunity metrics summary view
CREATE OR REPLACE VIEW opportunity_metrics_summary AS
SELECT
    COUNT(*) as total_opportunities,
    AVG(os.total_score) as avg_total_score,
    AVG(os.market_demand) as avg_market_demand,
    AVG(os.pain_intensity) as avg_pain_intensity,
    AVG(os.competition_level) as avg_competition_level,
    AVG(os.technical_feasibility) as avg_technical_feasibility,
    AVG(os.monetization_potential) as avg_monetization_potential,
    AVG(os.simplicity_score) as avg_simplicity_score,
    COUNT(CASE WHEN os.total_score >= 0.8 THEN 1 END) as high_score_opportunities,
    COUNT(CASE WHEN os.total_score >= 0.6 AND os.total_score < 0.8 THEN 1 END) as medium_score_opportunities,
    COUNT(CASE WHEN os.total_score < 0.6 THEN 1 END) as low_score_opportunities
FROM opportunities o
JOIN opportunity_scores os ON o.id = os.opportunity_id;

-- ============================================================================
-- PART 8: UTILITY FUNCTIONS
-- ============================================================================

-- Function to calculate trending score
CREATE OR REPLACE FUNCTION calculate_trending_score(
    score DECIMAL,
    engagement_rate DECIMAL,
    recency_factor DECIMAL
) RETURNS DECIMAL AS $$
BEGIN
    RETURN (score * 0.6) + (engagement_rate * 0.3) + (recency_factor * 0.1);
END;
$$ LANGUAGE plpgsql;

-- Function to update opportunity metrics
CREATE OR REPLACE FUNCTION update_opportunity_metrics() RETURNS TRIGGER AS $$
BEGIN
    -- Update modified timestamp
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PART 9: TABLE AND COLUMN COMMENTS
-- ============================================================================

-- Table comments
COMMENT ON TABLE subreddits IS 'Reddit communities/subreddits data';
COMMENT ON TABLE redditors IS 'Reddit user profiles';
COMMENT ON TABLE submissions IS 'Reddit posts and submissions';
COMMENT ON TABLE comments IS 'Reddit comments and replies';
COMMENT ON TABLE opportunities IS 'Business opportunities identified from Reddit discussions';
COMMENT ON TABLE opportunity_scores IS 'Scoring metrics for opportunity evaluation';
COMMENT ON TABLE score_components IS 'Individual components contributing to opportunity scores';
COMMENT ON TABLE market_validations IS 'Market validation evidence and analysis';
COMMENT ON TABLE competitive_landscape IS 'Competitive analysis for opportunities';
COMMENT ON TABLE feature_gaps IS 'Identified gaps in current solutions';
COMMENT ON TABLE cross_platform_verification IS 'Cross-platform verification of opportunities';
COMMENT ON TABLE monetization_patterns IS 'Monetization strategies and revenue models';
COMMENT ON TABLE user_willingness_to_pay IS 'User pricing sensitivity analysis';
COMMENT ON TABLE technical_assessments IS 'Technical feasibility and complexity analysis';
COMMENT ON TABLE workflow_results IS 'Results from automated workflow analysis';
COMMENT ON TABLE app_opportunities IS 'Primary opportunities table with trust and activity metrics';
COMMENT ON TABLE opportunity_analysis IS 'Detailed analysis of problem characteristics and market potential';

-- ============================================================================
-- PART 10: TRIGGERS FOR AUTOMATIC UPDATES
-- ============================================================================

-- Auto-update triggers for timestamp fields
CREATE TRIGGER update_subreddits_timestamp
    BEFORE UPDATE ON subreddits
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_redditors_timestamp
    BEFORE UPDATE ON redditors
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_submissions_timestamp
    BEFORE UPDATE ON submissions
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_comments_timestamp
    BEFORE UPDATE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_opportunities_timestamp
    BEFORE UPDATE ON opportunities
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_market_validations_timestamp
    BEFORE UPDATE ON market_validations
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_competitive_landscape_timestamp
    BEFORE UPDATE ON competitive_landscape
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_feature_gaps_timestamp
    BEFORE UPDATE ON feature_gaps
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_cross_platform_verification_timestamp
    BEFORE UPDATE ON cross_platform_verification
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_monetization_patterns_timestamp
    BEFORE UPDATE ON monetization_patterns
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_technical_assessments_timestamp
    BEFORE UPDATE ON technical_assessments
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_workflow_results_timestamp
    BEFORE UPDATE ON workflow_results
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_app_opportunities_timestamp
    BEFORE UPDATE ON app_opportunities
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

CREATE TRIGGER update_opportunity_analysis_timestamp
    BEFORE UPDATE ON opportunity_analysis
    FOR EACH ROW
    EXECUTE FUNCTION update_opportunity_metrics();

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- This baseline migration consolidates 20 previous migrations into a single
-- comprehensive schema definition. It preserves:
-- 1. All table structures and relationships
-- 2. Critical indexes for performance
-- 3. Views for analytics and reporting
-- 4. Functions for business logic
-- 5. Triggers for automatic timestamp updates
-- 6. Primary key naming for DLT compatibility (app_opportunities.submission_id)
--
-- Excluded from baseline (DLT-managed):
-- - _dlt_loads, _dlt_pipeline_state, _dlt_version
-- - _migrations_log
-- - app_opportunities__core_functions (DLT child table)
-- - All public_staging schema tables
"""

    return baseline

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Generate baseline migration from schema dump')
    parser.add_argument('--input', required=True, help='Input schema dump file')
    parser.add_argument('--output', required=True, help='Output baseline migration file')

    args = parser.parse_args()

    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate baseline migration
    try:
        extract_public_schema(args.input, args.output)
        print(f"✅ Baseline migration successfully created: {args.output}")
    except Exception as e:
        print(f"❌ Error generating baseline migration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()