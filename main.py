from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

def main():
    while True:
        user_input = input(
            "Enter command (name:<author_name>, tag:<tag>, tags:<tag1>,<tag2>, exit): "
        ).strip()
        if user_input.lower() == "exit":
            print("Exiting the program.")
            break
        elif user_input.startswith("name:"):
            author_name = user_input[5:].strip()
            print(find_by_author(author_name))
        elif user_input.startswith("tag:"):
            tag = user_input[4:].strip()
            print(find_by_tag(tag))
        elif user_input.startswith("tags:"):
            tags_input = user_input[5:].strip()
            tags = [tag.strip() for tag in tags_input.split(",")]
            print(find_by_tag(tags))
        else:
            print("Invalid command. Please enter a valid command or 'exit'.\n")



if __name__ == '__main__':
    main()
    # print(find_by_tag('mi'))
    # print(find_by_tag('mi'))
    #
    # print(find_by_author('in'))
    # print(find_by_author('in'))
    # quotes = Quote.objects().all()
    # print([e.to_json() for e in quotes])