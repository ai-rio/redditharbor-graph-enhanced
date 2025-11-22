#!/usr/bin/env python3
"""Check what backup tables were created"""

import asyncio
import asyncpg
from config.settings import get_database_config

async def check_backups():
    """Check backup tables"""
    db_config = get_database_config()

    try:
        conn = await asyncpg.connect(
            host=db_config.host,
            port=db_config.port,
            user=db_config.user,
            password=db_config.password,
            database=db_config.database
        )

        print("🔍 Checking backup tables...\n")

        # List all tables with backup in name
        backup_tables = await conn.fetch("""
            SELECT tablename
            FROM pg_tables
            WHERE tablename LIKE '%backup%'
            ORDER BY tablename;
        """)

        print(f"📋 Found {len(backup_tables)} backup tables:")
        for table in backup_tables:
            print(f"  - {table['tablename']}")

        # Check if unified table exists
        unified_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'opportunities_unified'
            );
        """)

        print(f"\n✅ opportunities_unified exists: {unified_exists}")

        # Check if legacy views exist
        legacy_views = await conn.fetch("""
            SELECT table_name
            FROM information_schema.views
            WHERE table_name LIKE '%legacy%'
            ORDER BY table_name;
        """)

        print(f"\n📋 Found {len(legacy_views)} legacy views:")
        for view in legacy_views:
            print(f"  - {view['table_name']}")

        await conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_backups())