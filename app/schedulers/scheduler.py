from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.services.cs_rec_sys_service import recommend_books


def start_scheduler():
    scheduler = BackgroundScheduler()

    # 매일 자정에 recommend_books 함수를 실행하는 작업 추가
    # scheduler.add_job(recommendation_job, "cron", hour=0, minute=0)

    # 프로그램 실행 1초 후에 한 번 실행되도록 스케줄 설정 (테스트 용)
    run_time = datetime.now() + timedelta(seconds=1)
    scheduler.add_job(recommendation_job, "date", run_date=run_time)

    scheduler.start()


def recommendation_job():
    session: Session = SessionLocal()

    try:
        # 추천 로직 실행
        recommend_books(session)
    except Exception as e:
        print(f"Error during recommendation: {e}")
    finally:
        session.close()
