import logging

logger = logging.getLogger(__name__)

def get_active_users(cursor):
    try:
        cursor.execute("SELECT USER_ID, USER_NAME FROM MINDTICKLE_USERS WHERE ACTIVE_STATUS = %s", ('active',))
        return cursor.fetchall()
    except Exception as e:
        logger.exception("An exception occurred: %s", str(e))
        return []

def get_daily_lessons_count(cursor, user_ids):
    try:
        placeholders = ', '.join(['%s'] * len(user_ids))
        sql_query = f"""
            SELECT user_id, COUNT(lesson_id) as total_lessons_completed
            FROM lesson_completion
            WHERE completion_date >= CURDATE() - INTERVAL 30 DAY
            AND user_id in ({placeholders})
            GROUP BY user_id
        """
        cursor.execute(sql_query, tuple(user_ids))
        result = cursor.fetchall()

        return {user_id: daily_lessons for user_id, daily_lessons in result}
    
    except Exception as e:
        logger.exception("An exception occurred: %s", str(e))


        
       

