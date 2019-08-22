# -*- coding: utf-8 -*-
import peewee as pw

from datetime import datetime as dte
from .core import Topic, entrypoint
from ..db import BaseModel
from prompt_toolkit import print_formatted_text, HTML

BulletType = {
    "task": "•",
    "event": "o",
    "note": "-",
}


TaskStatus = {
    "incomplete": "•",
    "complete": "x",
    "movefuture": "<",
    "delaycomplete": "X",       # 延期完成
}


class Bullet(BaseModel):
    """

    bullet has serveral type, as below.
        • Tasks
            things you have to do
        o Events
            noteworth moments in time, such as date, meeting...
        - Note
            things you don't want to forget. such as thought,idea,inspiration...

    tasks has serveral status, as below.
        • incomplete
        x completed
        < move to future log

    how future bullet defined.
        when `date_str` is blank or `date_str` is a future date (the value greater than today).
    """

    date_str = pw.CharField(null=False, index=True, default="")
    content = pw.CharField(null=False)
    bullet_type = pw.CharField(choices=list(zip(BulletType.keys(), BulletType.keys())), index=True)
    task_status = pw.CharField(choices=list(zip(TaskStatus.keys(), TaskStatus.keys())), index=True, default="incomplete")
    create_date = pw.DateTimeField(default=dte.now)
    update_date = pw.DateTimeField(default=dte.now)

    def show_text(self, with_date=False):
        if self.bullet_type == "task":
            sign = TaskStatus.get(self.task_status)
        else:
            sign = BulletType[self.bullet_type]

        if with_date:
            txt = "{date}： {sign} {content} [{id}]"
        else:
            txt = "{sign} {content} [{id}]"

        params = {
            "date": self.date_str,
            "sign": sign,
            "content": self.content.strip(),
            "id": self.id,
        }
        line = HTML(txt.format(**params))
        return line


class BujoTopic(Topic):

    _name = "bujo"
    _description = "plan manager, simple version of bullet journal"

    def get_today_bullets(self):
        today = dte.today().strftime("%Y-%m-%d")
        bullets = Bullet.select().where(Bullet.date_str == today).order_by(Bullet.create_date.desc())
        return bullets

    def get_all_bullets(self):
        bullets = Bullet.select().order_by(Bullet.create_date.desc())
        return bullets

    def get_incomplete_tasks(self):
        bullets = Bullet.select() \
                        .where(Bullet.bullet_type == "task", Bullet.task_status == "incomplete") \
                        .order_by(Bullet.create_date.desc())
        return bullets

    @entrypoint(doc="eg: `> add_bullet [task|note|event] content`")
    def add_bullet(self, text):
        try:
            text = text.strip()
            btype, content = text.split(" ", 1)
        except Exception:
            self.print_fail()
            return

        today = dte.today().strftime("%Y-%m-%d")
        t = Bullet(date_str=today,
                   bullet_type=btype,
                   content=content.strip())
        t.save()
        self.print_success()

    @entrypoint(doc="remove bullet, `> remove_bullet idx`")
    def remove_bullet(self, idx):
        bullets = self.get_today_bullets()
        try:
            idx = int(idx)
            bullet = bullets[idx - 1]
        except (ValueError, IndexError):
            self.print_fail()
            return
        qs = Bullet.delete().where(Bullet.id == bullet.id)
        qs.execute()
        self.print_success()

    @entrypoint(doc="eg: `modify_bullet idx new_value`")
    def modify_bullet(self, text):
        bullets = self.get_today_bullets()
        text = text.strip()
        try:
            idx, content = text.split(" ", 1)
            idx = int(idx.strip())
            bullet = bullets[idx - 1]
        except Exception:
            self.print_fail()
            return
        bullet.content = content
        bullet.save()
        self.print_success()

    @entrypoint(doc="eg: `set_task_status idx [complete|movefuture|incomplete]`")
    def set_task_status(self, text):
        text = text.strip()
        try:
            idx, content = text.split(" ", 1)
            idx = int(idx.strip())
            bullet = Bullet.get(Bullet.id == idx)
        except Exception:
            self.print_fail()
            return
        bullet.task_status = content.strip()
        bullet.save()
        self.print_success()

    @entrypoint(doc="list today log")
    def list_bullet(self):
        bullets = self.get_today_bullets()
        if bullets:
            print_formatted_text("")

        for bullet in bullets:
            print_formatted_text(bullet.show_text())
        self.print_success()

    @entrypoint(doc="list history bullet")
    def list_history_bullet(self):
        bullets = self.get_all_bullets()
        if bullets:
            print_formatted_text("")

        for bullet in bullets:
            print_formatted_text(bullet.show_text(with_date=True))
        self.print_success()

    @entrypoint(doc="list incomplete task")
    def list_incomplete_task(self):
        tasks = self.get_incomplete_tasks()
        for bullet in tasks:
            print_formatted_text(bullet.show_text(with_date=True))
        self.print_success()
