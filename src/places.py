from typing import List


class Place:
    country: str
    city: str
    api_id: str

    def __init__(self, line: str):
        self.country = line.split(';')[0]
        self.city = line.split(';')[1]
        self.api_id = line.split(';')[2]

    def __str__(self) -> str:
        return f"{self.country}, {self.city}"


class Places:
    @staticmethod
    def load_all(file_path: str) -> List[Place]:
        with open(file_path, encoding="utf8") as f:
            content = f.readlines()

        content = [line.strip() for line in content]
        return [Place(l.replace("\"", "")) for l in content]