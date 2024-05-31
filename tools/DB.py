import os
import datetime
import psycopg2.extras

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USERNAME'),
                        password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'))
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
conn.autocommit = True


# <editor-fold desc="Schemas">
@dataclass
class Member:
    UserID: int
    GuildID: int
    currentExp: int
    currentLevel: int

@dataclass
class level_rewards:
    GuildID: int
    RoleId: int
    levelToReach: int

@dataclass
class VoiceRoom:
    UserID: int
    GuildID: int
    roomName: str
    participantsLimit: int
    isVisible: bool

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
    cursor.execute(f'INSERT INTO users VALUES ({member.UserID})')
    cursor.execute('INSERT INTO members VALUES (%s, %s, %s, %s)', (member.UserID, member.GuildID, member.currentExp, member.currentLevel))
    conn.commit()


def update_member(member: Member):
    cursor.execute(f'UPDATE members SET current_exp={member.currentExp}, current_level={member.currentLevel} WHERE user_id={member.UserID} AND guild_id={member.GuildID}')
    conn.commit()


def get_member(user_id: int, guild_id: int):
    query = f'SELECT * FROM members WHERE user_id={user_id} AND guild_id={guild_id}'
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return result
    insert_member(Member(UserID=user_id, GuildID=guild_id, currentExp=0, currentLevel=0))
    cursor.execute(query)
    return cursor.fetchone()

# </editor-fold>


# <editor-fold desc="Voice Rooms">
def get_user_voice_room(user_id: int):
    cursor.execute(f'SELECT * FROM voice_rooms WHERE user_id={user_id}')
    return cursor.fetchone()
# </editor-fold>


# <editor-fold desc="Punishments">
def get_punishments(user_id: int, guild_id: int, type: int, expiring_time: datetime.datetime):
    cursor.execute(f'SELECT * FROM punishments WHERE user_id={user_id} AND guild_id={guild_id} AND punishment_type={type} AND duration={expiring_time}')
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