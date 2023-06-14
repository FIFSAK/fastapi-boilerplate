from typing import Any
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def update_shanyrak(
        self, shanyrak_id: str, user_id: str, data: dict[str, Any]
    ) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )

    def add_comment(self, shanyrak_id: str, user_id: str, content: str):
        data = {
            "_id": ObjectId(),
            "content": content,
            "created_at": datetime.utcnow(),
            "author_id": ObjectId(user_id),
        }
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$push": {"comments": data},
            },
        )

    def get_comment(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one(
            {"_id": ObjectId(shanyrak_id)},
            {"comments": 1},  # Only return the comments field
        )

    def change_comment(self, shanyrak_id: str, user_id: str, content: str):
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def update_comment(
        self, shanyrak_id: str, comment_id: str, content: str
    ) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "comments._id": ObjectId(comment_id)},
            update={
                "$set": {"comments.$.content": content},
            },
        )



    def delete_comment(self, shanyrak_id: str, comment_id: str) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$pull": {"comments": {"_id": ObjectId(comment_id)}},
            },
        )
