from datetime import datetime, timedelta
from website.domain.models import Post

class ServiceCalendar:

    @staticmethod
    def get(month, year,pacient):
        start_date = datetime(year=year, month=month, day=1)
        end_date = datetime(year=year, month=month + 1, day=1) - timedelta(days=1)

        posts = Post.query.filter_by(author=pacient)
        rows = []
        for post in posts:
            if post.date_created >= start_date and post.date_created <=end_date:
                rows.append(post)

        if len(rows) == 0:
            return None

        data = {}
        for r in rows:
            if r.result == 'depressed':
                data[r.id] = {"result": r.result, "color": "gray", "date":r.date_created}
            else:
                data[r.id] = {"result": r.result, "color": "green", "date":r.date_created}
        return data


