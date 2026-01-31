import click
import pandas as pd
from pathlib import Path
from flask import current_app

from app.extensions import get_db


def normalize_status(value: str) -> str:
    if pd.isna(value):
        return "INACTIVE"

    v = str(value).strip().lower()
    return "ACTIVE" if "ativo" in v else "INACTIVE"


def generate_codes(cur, start=1010):
    cur.execute("""
        SELECT id
        FROM employees
        ORDER BY id
    """)

    rows = cur.fetchall()

    updates = [
        (f"{start + i:06}", r["id"])
        for i, r in enumerate(rows)
    ]

    cur.executemany("""
        UPDATE employees
        SET employee_code = %s
        WHERE id = %s
    """, updates)


@click.command("import-employees")
def import_employees():
    """
    flask import-employees
    """

    project_root = Path(current_app.root_path).parent
    data_dir = project_root / "data"

    excel_file = next(data_dir.glob("Lista-de-Funcionarios-Venttos-17-12-25-Completo.*"))

    engine = "xlrd" if excel_file.suffix.lower() == ".xls" else "openpyxl"

    df = pd.read_excel(excel_file, engine=engine)

    df = df.rename(columns={
        df.columns[1]: "full_name",
        df.columns[2]: "job_title",
        df.columns[3]: "department",
        df.columns[4]: "hired_at",
        df.columns[5]: "status",
        df.columns[6]: "branch_name",
    })

    df["status"] = df["status"].apply(normalize_status)
    df["hired_at"] = pd.to_datetime(df["hired_at"], errors="coerce").dt.date

    rows = [
        (
            str(r.full_name).strip(),
            r.job_title,
            r.department,
            r.hired_at,
            r.status,
            r.branch_name
        )
        for r in df.itertuples(index=False)
        if r.full_name
    ]

    with get_db() as conn:
        with conn.cursor() as cur:

            cur.execute("TRUNCATE TABLE employees RESTART IDENTITY;")

            cur.executemany("""
                INSERT INTO employees (
                    full_name,
                    job_title,
                    department,
                    hired_at,
                    status,
                    branch_name
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """, rows)

            generate_codes(cur)

        conn.commit()

    print("✅ Employees imported with employee_code!")
