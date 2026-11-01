from backend.database import SessionLocal, engine, Base
from backend.models import User, View, Task, CompletionLog
from backend.security import get_password_hash

def seed_database():
    print("Resetting database (dropping existing tables)...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Seeding fresh test data...")

        # 1. Create Test Users (at least one user required)
        users_data = [
            {"email": "test@routine.com", "password": "password123"},
            {"email": "alice@routine.com", "password": "password123"}
        ]
        
        created_users = []
        for u_data in users_data:
            user = User(
                email=u_data["email"],
                password_hash=get_password_hash(u_data["password"])
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            created_users.append(user)
            print(f"Created user: {user.email} (ID: {user.id})")

        primary_user = created_users[0]

        # 2. Create Views for primary user
        views_data = [
            {"name": "Health & Fitness", "cadence": "daily"},
            {"name": "Professional Development", "cadence": "weekly"},
            {"name": "Financial Review", "cadence": "monthly"},
            {"name": "Mindfulness & Well-being", "cadence": "daily"}
        ]
        
        created_views = []
        for v_data in views_data:
            view = View(user_id=primary_user.id, name=v_data["name"], cadence=v_data["cadence"])
            db.add(view)
            db.commit()
            db.refresh(view)
            created_views.append(view)
            print(f"Created view: {view.name} [{view.cadence}] (ID: {view.id})")

        # 3. Create Tasks
        tasks_data = [
            {"view_id": created_views[0].id, "title": "Morning 5K Run"},
            {"view_id": created_views[0].id, "title": "Drink 8 Glasses of Water"},
            {"view_id": created_views[0].id, "title": "30 Minutes Stretching"},
            {"view_id": created_views[1].id, "title": "Complete Pull Request Review"},
            {"view_id": created_views[1].id, "title": "Read One Chapter of Architecture Book"},
            {"view_id": created_views[2].id, "title": "Review Monthly Budget & Investments"},
            {"view_id": created_views[3].id, "title": "10 Minutes Meditation"},
            {"view_id": created_views[3].id, "title": "Journal Daily Gratitude"}
        ]

        created_tasks = []
        for t_data in tasks_data:
            task = Task(view_id=t_data["view_id"], title=t_data["title"])
            db.add(task)
            db.commit()
            db.refresh(task)
            created_tasks.append(task)
            print(f"Created task: {task.title} (ID: {task.id})")

        # 4. Create Completion Logs
        logs_data = [
            {"task_id": created_tasks[0].id, "period_key": "2026-11-01", "done": True},
            {"task_id": created_tasks[1].id, "period_key": "2026-11-01", "done": True},
            {"task_id": created_tasks[2].id, "period_key": "2026-11-01", "done": False},
            {"task_id": created_tasks[3].id, "period_key": "2026-W44", "done": True},
            {"task_id": created_tasks[4].id, "period_key": "2026-W44", "done": False},
            {"task_id": created_tasks[5].id, "period_key": "2026-11", "done": True},
            {"task_id": created_tasks[6].id, "period_key": "2026-11-01", "done": True},
            {"task_id": created_tasks[7].id, "period_key": "2026-11-01", "done": True}
        ]

        for l_data in logs_data:
            log = CompletionLog(
                task_id=l_data["task_id"],
                period_key=l_data["period_key"],
                done=l_data["done"]
            )
            db.add(log)
            db.commit()
            print(f"Created completion log for task {l_data['task_id']} [Period: {l_data['period_key']}, Done: {l_data['done']}]")

        print("Database reset and seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
