import re
from pathlib import Path
from sqlalchemy import create_engine, text

def test_all_sql_files_compile_without_raw_params():
    """
    Test 1 & 2: Verify every SQL file compiles under postgresql+psycopg without exceptions,
    and assert no compiled SQL contains :param style placeholders.
    """
    engine = create_engine('postgresql+psycopg://user:pass@localhost/db')
    
    # Locate all SQL files
    sql_dir = Path(__file__).resolve().parents[1] / "db" / "sql"
    sql_files = list(sql_dir.glob("*.sql"))
    
    assert len(sql_files) > 0, "No SQL files found in db/sql"
    
    for sql_file in sql_files:
        content = sql_file.read_text(encoding="utf-8")
        
        # Load through SQLAlchemy TextClause
        stmt = text(content)
        
        # Compile using postgresql+psycopg dialect
        compiled = stmt.compile(engine)
        
        # Verify bind parameter names remain intact
        if sql_file.name == "tier_comps.sql":
            assert "bedrooms" in stmt._bindparams
            assert "bathrooms" in stmt._bindparams
        
        # Verify compiled SQL no longer contains raw :param::TYPE patterns
        # or any :param placeholders at all (they should be %(param)s or similar)
        # Note: We must be careful because ::geography and ::TEXT without params are allowed.
        # But a colon followed by a word (like :bedrooms) should NOT be in the compiled string!
        
        compiled_str = compiled.string
        
        # Use a regex to find any stray :param that is NOT a PostgreSQL type cast (like ::geography)
        # This regex looks for a colon followed by a word, not preceded by a colon, and not followed by a colon.
        # If the compilation worked, all placeholders like :bedrooms should have been converted to %(bedrooms)s.
        stray_params = re.findall(r'(?<!:):([a-zA-Z_]\w*)(?!:)', compiled_str)
        
        assert not stray_params, f"Found uncompiled raw parameters in {sql_file.name}: {stray_params}"
