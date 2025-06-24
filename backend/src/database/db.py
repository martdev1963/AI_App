from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

#--------------------------------------------------------------------------------------------------------
# vid_time: 1:35:55 / 2:31:54

# Routes are next...
#--------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------
# function definitions...
# getting error:
# expected type Union in def get_challenge_quota(db: Session, user_id: int):
# .filter(models.ChallengeQuota.user_id == user_id) # criteria  <---------
#  got 'bool' instead...
#--------------------------------------------------------------------------------------------------------


# get challenge
def get_challenge_quota(db: Session, user_id: int):
    return (db.query(models.ChallengeQuota)
            .filter(models.ChallengeQuota.user_id == user_id) # criteria
            .first()) # first entry that matches criteria above...


# create challenge
def create_challenge_quota(db: Session, user_id: int):
    db_quota = models.ChallengeQuota(user_id=user_id)
    db.add(db_quota) # add to staging area...
    db.commit() # write it to the database...
    db.refresh(db_quota) # re-read all of the values...
    return db_quota



def reset_quota_if_needed(db: Session, quota: models.ChallengeQuota):
    now = datetime.now()
    # compare current date time with time stored in quota database to see if it's been 24 hours...
    if now - quota.last_reset_date > timedelta(hours=24):
        quota.quota_remaining = 10
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
    return quota



def create_challenge(
    db: Session,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str
):
    db_challenge = models.Challenge(
        difficulty=difficulty, # assign the parameters to the variables...
        created_by=created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def get_user_challenges(db: Session, user_id: str):
    return db.query(models.Challenge).filter(models.Challenge.created_by == user_id).all()









