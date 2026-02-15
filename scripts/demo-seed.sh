#!/bin/bash

# Demo seed script to create example data

set -e

echo "🌱 Seeding demo data..."

cd backend
source venv/bin/activate

python << EOF
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.project import Project
from app.services.auth import create_magic_link

db = SessionLocal()

# Create demo user
demo_user = db.query(User).filter(User.email == "demo@example.com").first()
if not demo_user:
    demo_user = User(
        email="demo@example.com",
        name="Demo User",
        max_projects=10,
        max_edits_per_day=50,
        max_inference_per_day=20,
    )
    db.add(demo_user)
    db.commit()
    print("✅ Created demo user")

# Create demo project
demo_project = Project(
    name="Demo Living Room",
    description="Example project for demonstration",
    user_id=demo_user.id,
    room_type="living_room",
)
db.add(demo_project)
db.commit()
print("✅ Created demo project")

db.close()
print("✅ Demo data seeded!")
EOF

cd ..

echo "✅ Seeding complete!"
