from app.database.mongodb import database


class ResearchService:

    def search_papers(self, keyword: str):

        collection = database["papers"]

        papers = list(
            collection.find(
                {
                    "title": {
                        "$regex": keyword,
                        "$options": "i"
                    }
                },
                {
                    "_id": 0
                }
            ).limit(10)
        )

        return papers
