from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from config.database import SessionLocal
from services.cf_rec_sys_service import run_recommendation

def start_scheduler():
    scheduler = BackgroundScheduler()

    # 매일 자정에 run_recommendation 함수를 실행하는 작업 추가
    scheduler.add_job(run_recommendation, "cron", hour=0, minute=0, args=[SessionLocal()])

    # 프로그램 실행 시 즉시 추천 시스템을 실행 (테스트 용)
    run_time = datetime.now() + timedelta(seconds=1)
    scheduler.add_job(run_recommendation, "date", run_date=run_time, args=[SessionLocal()])

    scheduler.start()
    print("스케줄러가 시작되었습니다.")

if __name__ == "__main__":
    start_scheduler()

    # 프로그램이 계속 실행되도록 유지
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("스케줄러가 종료됩니다.")