import os
import pandas as pd
import logging
import json
from queries import get_active_users, get_daily_lessons_count
from database import connect_postgressql, connect_mysql
from s3_utils import upload_to_minio

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def initialize_config():
    try:
        with open("config.json") as f:
            config = json.load(f)
            return config
    except Exception as e:
        logger.exception("An exception occurred while initializing config: %s", str(e))

def generate_report_data(active_users, daily_lessons_count):
    try:
        active_users_df = pd.DataFrame(active_users, columns=["user_id", "user_name"])
        daily_lesson_count_df = pd.DataFrame(daily_lessons_count.items(), columns=["user_id", "daily_lessons"])
        report_df = active_users_df.merge(daily_lesson_count_df, on="user_id", how="left")
        report_df["daily_lessons"].fillna(0, inplace=True)
        return report_df
    except Exception as e:
        logger.exception("An exception occurred: %s", str(e))
        return pd.DataFrame()  # Return an empty DataFrame on error

def main():
    try:
        config = initialize_config()

        # Connect to PostgreSQL
        pg_conn = connect_postgressql()
        if not pg_conn:
            logger.error("Failed to connect to PostgreSQL.")
            return

        pg_cursor = pg_conn.cursor()

        # Connect to MySQL
        my_sql_conn = connect_mysql()
        if not my_sql_conn:
            logger.error("Failed to connect to MySQL.")
            return

        my_sql_cursor = my_sql_conn.cursor()

        # Fetching active user ids
        active_users = get_active_users(pg_cursor)
        active_user_ids = [user_id for user_id, _ in active_users]

        # Fetching daily lesson count
        daily_lesson_count = get_daily_lessons_count(my_sql_cursor, active_user_ids)

        # Generating the report data
        report_data = generate_report_data(active_users, daily_lesson_count)

        # Saving the report to a CSV file
        report_file_path = 'active_users_report.csv'
        report_data.to_csv(report_file_path, index=False)

        # Uploading the report to S3
        minio_endpoint = config['MINIO_API']
        minio_access_key = os.environ.get('MINIO_ACCESS_KEY_ID')
        minio_secret_key = os.environ.get('MINIO_SECRET_ACCESS_KEY')
        minio_bucket_name = config['MINIO_STORAGE_BUCKET_NAME']
        minio_object_name = config["FILE_PATH"]
        
        upload_to_minio(report_file_path, minio_endpoint, minio_access_key, minio_secret_key, minio_bucket_name, minio_object_name)

    except Exception as e:
        logger.exception("An exception occurred: %s", str(e))

    finally:
        # Cleaning up resources and close database connections
        if 'pg_cursor' in locals() and pg_cursor:
            pg_cursor.close()
            pg_conn.close()

        if 'my_sql_cursor' in locals() and my_sql_cursor:
            my_sql_cursor.close()
            my_sql_conn.close()

if __name__ == "__main__":
    main()
