from typing import Any
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult

# from ..router.router_get_favorites import ShanyrakPreview


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
                "$set": content,
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

    def add_media(self, shanyrak_id: str, media_urls: list[str]):
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$push": {
                    "media": {"$each": media_urls}
                },  # Each media url is added to the media array
            },
        )

    def get_shanyrak_media(self, shanyrak_id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        if shanyrak is not None:
            # convert user_id and media items to strings
            shanyrak["user_id"] = str(shanyrak["user_id"])
            shanyrak["media"] = [{"url": url} for url in shanyrak["media"]]
        return shanyrak

    def delete_media(self, shanyrak_id: str):
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$set": {"media": []},
            },
        )

    # def create_shanyrak(self, user_id: str, data: dict[str, Any]):
    #     data["user_id"] = ObjectId(user_id)
    #     insert_result = self.database["shanyraks"].insert_one(data)
    #     return insert_result.inserted_id

    def add_favorites(self, data: dict[str, Any]):
        return self.database["favorites"].insert_one(data)

    # def get_favorites(self):
    #     return self.database["favorites"].all

    # def get_user_favorites(self, user_id: str):
    #     favorites = self.database["favorites"].find({"user_id": user_id})
    #     shanyrak_previews = []
    #     for favorite in favorites:
    #         shanyrak_id = favorite["shanyrak_id"]
    #         shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)}, {"_id": 1, "address": 1})
    #         if shanyrak is not None:
    #             shanyrak_previews.append(ShanyrakPreview(**shanyrak))
    #     return shanyrak_previews

    def get_user_favorites(self, user_id: str):
        favorites_cursor = self.database["favorites"].find(
            {"user_id": ObjectId(user_id)}
        )
        favorites = list(favorites_cursor)
        shanyrak_previews = []
        for favorite in favorites:
            shanyrak_previews.append(
                {"_id": str(favorite["_id"]), "address": favorite["address"]}
            )
        return shanyrak_previews

    def delete_favorite(self, user_id: str, shanyrak_id: str):
        result = self.database["favorites"].delete_one({"user_id": ObjectId(user_id), "_id": ObjectId(shanyrak_id)})
        if result.deleted_count == 0:
            raise Exception("Favorite not found or deletion was unsuccessful")

