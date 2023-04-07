class Hitokoto:
    def __init__(self, id, uuid, hitokoto, type, from_, from_who, creator,
                 creator_uid, reviewer, commit_from, created_at, length):
        self.id = id
        self.uuid = uuid
        self.hitokoto = hitokoto
        self.type = type
        self.from_ = from_
        self.from_who = from_who
        self.creator = creator
        self.creator_uid = creator_uid
        self.reviewer = reviewer
        self.commit_from = commit_from
        self.created_at = created_at
        self.length = length
