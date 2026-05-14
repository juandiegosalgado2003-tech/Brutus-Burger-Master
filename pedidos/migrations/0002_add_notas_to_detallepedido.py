from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name='pedidos_detallepedido' AND column_name='notas'
                ) THEN
                    ALTER TABLE pedidos_detallepedido ADD COLUMN notas varchar(200) DEFAULT '' NOT NULL;
                END IF;
            END $$;
            """,
            reverse_sql="ALTER TABLE pedidos_detallepedido DROP COLUMN IF EXISTS notas;",
        ),
    ]
