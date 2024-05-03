import configparser
import datetime
from dataclasses import dataclass

import psycopg2

config = configparser.ConfigParser()
config.read("./BD_config.ini")
conn = psycopg2.connect(dbname=config['db']["dbname"], user=config['db']["user"],
                        password=config['db']["password"], host=config['db']["host"])
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


# <editor-fold desc="Guilds">
def create_guild(guild_id: int):
    cursor.execute(f'INSERT INTO guilds VALUES ({guild_id})')
    conn.commit()


def get_guild(guild_id: int):
    cursor.execute(f'SELECT * FROM guilds WHERE id={guild_id}')
    return cursor.fetchone()
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