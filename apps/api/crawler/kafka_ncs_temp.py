import pickle

from kafka import KafkaProducer

# from apps.api.crawler.youtube_crawler.result import Post

producer = KafkaProducer(bootstrap_servers=["10.11.101.129:9092"])


def push_kafka(posts, comments):
    try: 
        if posts:
            bytes_obj = pickle.dumps([ob.__dict__ for ob in posts])
            producer.send('lnmxh', bytes_obj)
            print("Đã đẩy vào kafka")
            return 1
        else:
            return 0
    except Exception as e:
        print(e)
    # try: 
    #     if posts:
    #         bytes_obj = pickle.dumps([ob.__dict__ for ob in posts])
    #         producer.send('osint-posts-update', bytes_obj)
    #         print("Đã đẩy vào kafka: osint-posts-update ")
    #         return 1
    #     else:
    #         return 0
    # except Exception as e:
    #     print(e)

# def write_log_post(post: Post, file = ""):
#         if file == "":
#             file = "log_post.txt"
#         with open(file, "a", encoding="utf-8") as fp:
#             fp.write(f"{str(post)}\n")
#             fp.write(f"🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈\n")

class GeneratorPost:
    def __init__(self, target, args: list = []) -> None:
        self.target = target
        self.args = args

    def run(self):
        for posts in self.target(*self.args):
            print(f"số bài post group đẩy qua kafka là {len(posts)}")
            push_kafka(posts=posts)
            # for post in posts:
            #     write_log_post(post)
            # if self.is_return:
            #     return post

    def get_posts(self, list_posts: list):
        for posts in self.target(*self.args):
            print(f"số bài posts là {len(posts)}")
            list_posts.extend(posts)
            push_kafka(posts=posts)
            # for post in posts:
            #     write_log_post(post)


## Hàm test kết quả đẩy qua kafka => trả về list các object Post
# def Test(paramater):
#     post = Post
#     for i in range(100):
#         print(i)
#         yield [post]


# ##Demo sử dụng
# if __name__ == "__main__":
#     # Đẩy liên tục
#     GeneratorPost(target=Test, args=[1]).run()
#     # Đẩy 1 lần
#     post = Post
#     push_kafka(posts=[post])
