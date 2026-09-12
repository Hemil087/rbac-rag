from datetime import datetime, timezone

from sqlalchemy import select
from app.core.security import hash_password
from app.db.database import SessionLocal
from app.db.models import (
    Organization,
    Role,
    User,
    Document,
    DocumentPermission,
    DocumentChunk,
    Conversation,
    Message,
)


def seed_database():
    db = SessionLocal()

    try:
        # ============================================================
        # 1. ORGANIZATIONS
        # ============================================================

        acme = Organization(
            name="Acme Corporation",
            created_at=datetime.now(timezone.utc),
            email_domain="acme.com",
        )

        globex = Organization(
            name="Globex Corporation",
            created_at=datetime.now(timezone.utc),
            email_domain="globex.com",
        )

        db.add_all([acme, globex])
        db.flush()

        print(f"Created organizations: {acme.id}, {globex.id}")

        # ============================================================
        # 2. ROLES
        # ============================================================

        # Acme roles
        acme_admin = Role(
            org_id=acme.id,
            role_name="admin",
            created_at=datetime.now(timezone.utc),
        )

        acme_manager = Role(
            org_id=acme.id,
            role_name="manager",
            created_at=datetime.now(timezone.utc),
        )

        acme_employee = Role(
            org_id=acme.id,
            role_name="employee",
            created_at=datetime.now(timezone.utc),
        )

        # Globex roles
        globex_admin = Role(
            org_id=globex.id,
            role_name="admin",
            created_at=datetime.now(timezone.utc),
        )

        globex_employee = Role(
            org_id=globex.id,
            role_name="employee",
            created_at=datetime.now(timezone.utc),
        )

        db.add_all([
            acme_admin,
            acme_manager,
            acme_employee,
            globex_admin,
            globex_employee,
        ])

        db.flush()

        print("Created roles")

        # ============================================================
        # 3. USERS
        # ============================================================

        # NOTE:
        # These are dummy hashes for database testing.
        # We will replace this with real password hashing
        # when implementing authentication.

        acme_admin_user = User(
            org_id=acme.id,
            role_id=acme_admin.id,
            email="admin@acme.com",
            hashed_password=hash_password("admin123"),
            created_at=datetime.now(timezone.utc),
        )

        acme_manager_user = User(
            org_id=acme.id,
            role_id=acme_manager.id,
            email="manager@acme.com",
            hashed_password=hash_password("manager123"),
            created_at=datetime.now(timezone.utc),
        )

        acme_employee_user = User(
            org_id=acme.id,
            role_id=acme_employee.id,
            email="employee@acme.com",
            hashed_password=hash_password("employee123"),
            created_at=datetime.now(timezone.utc),
        )

        globex_admin_user = User(
            org_id=globex.id,
            role_id=globex_admin.id,
            email="admin@globex.com",
            hashed_password=hash_password("admin123"),
            created_at=datetime.now(timezone.utc),
        )

        globex_employee_user = User(
            org_id=globex.id,
            role_id=globex_employee.id,
            email="employee@globex.com",
            hashed_password=hash_password("employee123"),
            created_at=datetime.now(timezone.utc),
        )

        db.add_all([
            acme_admin_user,
            acme_manager_user,
            acme_employee_user,
            globex_admin_user,
            globex_employee_user,
        ])

        db.flush()

        print("Created users")

        # ============================================================
        # 4. DOCUMENTS
        # ============================================================

        acme_hr = Document(
            org_id=acme.id,
            filename="acme_hr_policy.pdf",
            storage_path="/data/acme/acme_hr_policy.pdf",
            file_type="pdf",
            file_size=125000,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        acme_engineering = Document(
            org_id=acme.id,
            filename="engineering_handbook.pdf",
            storage_path="/data/acme/engineering_handbook.pdf",
            file_type="pdf",
            file_size=245000,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        acme_sales = Document(
            org_id=acme.id,
            filename="sales_playbook.pdf",
            storage_path="/data/acme/sales_playbook.pdf",
            file_type="pdf",
            file_size=185000,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        globex_hr = Document(
            org_id=globex.id,
            filename="globex_hr_policy.pdf",
            storage_path="/data/globex/globex_hr_policy.pdf",
            file_type="pdf",
            file_size=110000,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        globex_finance = Document(
            org_id=globex.id,
            filename="finance_policy.pdf",
            storage_path="/data/globex/finance_policy.pdf",
            file_type="pdf",
            file_size=210000,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        db.add_all([
            acme_hr,
            acme_engineering,
            acme_sales,
            globex_hr,
            globex_finance,
        ])

        db.flush()

        print("Created documents")

        # ============================================================
        # 5. DOCUMENT PERMISSIONS
        # ============================================================

        permissions = [

            # ---------------- ACME HR ----------------
            DocumentPermission(
                doc_id=acme_hr.id,
                role_id=acme_admin.id,
                org_id=acme.id,
            ),

            DocumentPermission(
                doc_id=acme_hr.id,
                role_id=acme_manager.id,
                org_id=acme.id,
            ),

            # ---------------- ACME ENGINEERING ----------------
            DocumentPermission(
                doc_id=acme_engineering.id,
                role_id=acme_admin.id,
                org_id=acme.id,
            ),

            DocumentPermission(
                doc_id=acme_engineering.id,
                role_id=acme_manager.id,
                org_id=acme.id,
            ),

            DocumentPermission(
                doc_id=acme_engineering.id,
                role_id=acme_employee.id,
                org_id=acme.id,
            ),

            # ---------------- ACME SALES ----------------
            DocumentPermission(
                doc_id=acme_sales.id,
                role_id=acme_admin.id,
                org_id=acme.id,
            ),

            DocumentPermission(
                doc_id=acme_sales.id,
                role_id=acme_manager.id,
                org_id=acme.id,
            ),

            # ---------------- GLOBEX HR ----------------
            DocumentPermission(
                doc_id=globex_hr.id,
                role_id=globex_admin.id,
                org_id=globex.id,
            ),

            DocumentPermission(
                doc_id=globex_hr.id,
                role_id=globex_employee.id,
                org_id=globex.id,
            ),

            # ---------------- GLOBEX FINANCE ----------------
            DocumentPermission(
                doc_id=globex_finance.id,
                role_id=globex_admin.id,
                org_id=globex.id,
            ),
        ]

        db.add_all(permissions)

        print("Created document permissions")

        # ============================================================
        # 6. DOCUMENT CHUNKS
        # ============================================================

        # IMPORTANT:
        # Vector(384) means every embedding must contain exactly
        # 384 floating-point values.
        #
        # For seed/testing purposes we use simple dummy vectors.
        # Real embeddings will be generated during document ingestion.

        def dummy_embedding(value: float):
            return [value] * 384

        chunks = [

            # ACME HR
            DocumentChunk(
                doc_id=acme_hr.id,
                chunk_index=0,
                chunk_text=(
                    "Acme Corporation employees are entitled to "
                    "twenty days of paid annual leave."
                ),
                embedding=dummy_embedding(0.01),
                chunk_metadata={
                    "page": 1,
                    "section": "Leave Policy",
                },
            ),

            DocumentChunk(
                doc_id=acme_hr.id,
                chunk_index=1,
                chunk_text=(
                    "Employees must submit leave requests "
                    "through the internal HR portal."
                ),
                embedding=dummy_embedding(0.02),
                chunk_metadata={
                    "page": 2,
                    "section": "Leave Requests",
                },
            ),

            # ACME ENGINEERING
            DocumentChunk(
                doc_id=acme_engineering.id,
                chunk_index=0,
                chunk_text=(
                    "All production code must undergo code review "
                    "before being merged into the main branch."
                ),
                embedding=dummy_embedding(0.03),
                chunk_metadata={
                    "page": 1,
                    "section": "Code Review",
                },
            ),

            DocumentChunk(
                doc_id=acme_engineering.id,
                chunk_index=1,
                chunk_text=(
                    "Production deployments must be approved by "
                    "an engineering manager."
                ),
                embedding=dummy_embedding(0.04),
                chunk_metadata={
                    "page": 3,
                    "section": "Deployment",
                },
            ),

            # ACME SALES
            DocumentChunk(
                doc_id=acme_sales.id,
                chunk_index=0,
                chunk_text=(
                    "Sales representatives should prioritize "
                    "annual contracts over monthly contracts."
                ),
                embedding=dummy_embedding(0.05),
                chunk_metadata={
                    "page": 1,
                    "section": "Sales Strategy",
                },
            ),

            # GLOBEX HR
            DocumentChunk(
                doc_id=globex_hr.id,
                chunk_index=0,
                chunk_text=(
                    "Globex employees receive fifteen days "
                    "of paid annual leave."
                ),
                embedding=dummy_embedding(0.06),
                chunk_metadata={
                    "page": 1,
                    "section": "Leave Policy",
                },
            ),

            # GLOBEX FINANCE
            DocumentChunk(
                doc_id=globex_finance.id,
                chunk_index=0,
                chunk_text=(
                    "All expenses above $5,000 require approval "
                    "from the finance department."
                ),
                embedding=dummy_embedding(0.07),
                chunk_metadata={
                    "page": 2,
                    "section": "Expense Approval",
                },
            ),
        ]

        db.add_all(chunks)

        print("Created document chunks")

        # ============================================================
        # 7. CONVERSATIONS
        # ============================================================

        acme_employee_conversation = Conversation(
            user_id=acme_employee_user.id,
            org_id=acme.id,
            title="Engineering Policy Questions",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        acme_manager_conversation = Conversation(
            user_id=acme_manager_user.id,
            org_id=acme.id,
            title="Sales Policy Discussion",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        globex_employee_conversation = Conversation(
            user_id=globex_employee_user.id,
            org_id=globex.id,
            title="HR Questions",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        db.add_all([
            acme_employee_conversation,
            acme_manager_conversation,
            globex_employee_conversation,
        ])

        db.flush()

        print("Created conversations")

        # ============================================================
        # 8. MESSAGES
        # ============================================================

        messages = [

            # ACME employee conversation
            Message(
                conversation_id=acme_employee_conversation.id,
                role="user",
                content="What is the code review policy?",
                created_at=datetime.now(timezone.utc),
            ),

            Message(
                conversation_id=acme_employee_conversation.id,
                role="assistant",
                content=(
                    "All production code must undergo code review "
                    "before being merged into the main branch."
                ),
                created_at=datetime.now(timezone.utc),
            ),

            # ACME manager conversation
            Message(
                conversation_id=acme_manager_conversation.id,
                role="user",
                content="Should we prioritize annual contracts?",
                created_at=datetime.now(timezone.utc),
            ),

            Message(
                conversation_id=acme_manager_conversation.id,
                role="assistant",
                content=(
                    "According to the sales playbook, sales "
                    "representatives should prioritize annual contracts."
                ),
                created_at=datetime.now(timezone.utc),
            ),

            # GLOBEX employee conversation
            Message(
                conversation_id=globex_employee_conversation.id,
                role="user",
                content="How many days of annual leave do we get?",
                created_at=datetime.now(timezone.utc),
            ),

            Message(
                conversation_id=globex_employee_conversation.id,
                role="assistant",
                content=(
                    "Globex employees receive fifteen days "
                    "of paid annual leave."
                ),
                created_at=datetime.now(timezone.utc),
            ),

            # Example application-level system message
            Message(
                conversation_id=globex_employee_conversation.id,
                role="system",
                content="Conversation initialized.",
                created_at=datetime.now(timezone.utc),
            ),
        ]

        db.add_all(messages)

        # ============================================================
        # COMMIT EVERYTHING
        # ============================================================

        db.commit()

        print("\n========================================")
        print("DATABASE SEED COMPLETED SUCCESSFULLY")
        print("========================================")

        print("\nOrganizations:")
        print(f"  Acme   -> id={acme.id}")
        print(f"  Globex -> id={globex.id}")

        print("\nUsers:")
        print(f"  admin@acme.com       -> id={acme_admin_user.id}")
        print(f"  manager@acme.com     -> id={acme_manager_user.id}")
        print(f"  employee@acme.com    -> id={acme_employee_user.id}")
        print(f"  admin@globex.com     -> id={globex_admin_user.id}")
        print(f"  employee@globex.com  -> id={globex_employee_user.id}")

        print("\nDocuments:")
        print(f"  Acme HR              -> id={acme_hr.id}")
        print(f"  Acme Engineering     -> id={acme_engineering.id}")
        print(f"  Acme Sales           -> id={acme_sales.id}")
        print(f"  Globex HR            -> id={globex_hr.id}")
        print(f"  Globex Finance       -> id={globex_finance.id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()