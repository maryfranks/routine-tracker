import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base, get_db
from backend.models import User, View, Task, CompletionLog


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_database_setup_and_models(db_session):
    user = User(email="test@example.com", password_hash="hashedpassword")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.created_at is not None

    view = View(user_id=user.id, name="Health & Fitness", cadence="daily")
    db_session.add(view)
    db_session.commit()
    db_session.refresh(view)

    assert view.id is not None
    assert view.name == "Health & Fitness"
    assert view.cadence == "daily"
    assert len(user.views) == 1
    assert user.views[0].id == view.id

    task = Task(view_id=view.id, title="Morning Run")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.id is not None
    assert task.title == "Morning Run"
    assert len(view.tasks) == 1
    assert view.tasks[0].id == task.id

    log = CompletionLog(task_id=task.id, period_key="2026-10-27", done=True)
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    assert log.id is not None
    assert log.period_key == "2026-10-27"
    assert log.done is True
    assert len(task.logs) == 1
    assert task.logs[0].id == log.id


def test_get_db_generator():
    gen = get_db()
    db = next(gen)
    assert db is not None
    with pytest.raises(StopIteration):
        next(gen)
