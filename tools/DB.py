import os
import configparser
import datetime
import psycopg2

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

config = configparser.ConfigParser()
config.read("./BD_config.ini")
conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USERNAME'),
                        password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'))
cursor = conn.cursor()


# <editor-fold desc="Schemas">
@dataclass
class Member:
    UserID: int
    GuildID: int


@dataclass
class VoiceRoom:
    UserID: int
    GuildID: int


@dataclass
class Punishment:
    UserID: int
    GuildID: int
    Type: int
    ExpiringTime: datetime.datetime
# </editor-fold>


# <editor-fold desc="Users">
def get_user(user_id: int):
    cursor.execute(f'SELECT * FROM users WHERE id={user_id}')
    return cursor.fetchone()


def insert_user(user_id: int):
    cursor.execute(f'INSERT INTO users VALUES ({user_id})')
    conn.commit()
# </editor-fold>


# <editor-fold desc="Guilds">
def get_guild(guild_id: int):
    cursor.execute(f'SELECT * FROM guilds WHERE id={guild_id}')
    return cursor.fetchone()


def insert_guild(guild_id: int, owner_id: int):
    if not get_user(owner_id):
        insert_user(owner_id)
    cursor.execute(f'INSERT INTO guilds VALUES ({guild_id}, {owner_id})')
    conn.commit()


def remove_guild(guild_id: int):
    cursor.execute(f'DELETE FROM guilds WHERE id={guild_id}')
    conn.commit()
# </editor-fold>


# <editor-fold desc="Members">
def insert_member(member: Member):
    cursor.execute('INSERT INTO members VALUES (%s, %s)', (member.UserID, member.GuildID))
    conn.commit()


def get_member(user_id: int, guild_id: int):
    cursor.execute(f'SELECT * FROM members WHERE user_id={user_id} AND guild_id={guild_id}')
    return cursor.fetchone()
# </editor-fold>


# <editor-fold desc="Voice Rooms">
def get_user_voice_room(user_id: int):
    cursor.execute(f'SELECT * FROM voice_rooms WHERE user_id={user_id}')
    return cursor.fetchone()
# </editor-fold>


# <editor-fold desc="Punishments">
def get_punishments():
    cursor.execute('SELECT * FROM punishments')
    return cursor.fetchall()


def insert_punishment(punishmentData: Punishment):
    try:
        cursor.execute('''INSERT INTO punishments VALUES (%s, %s, %s, %s)''',
                       (punishmentData.UserID, punishmentData.GuildID, punishmentData.Type, punishmentData.ExpiringTime))
        conn.commit()
        return True
    finally:
        return False


def get_expired_punishments():
    cursor.execute('SELECT * FROM punishments WHERE duration < %s', (datetime.datetime.utcnow(), ))
    return cursor.fetchall()
# </editor-fold>