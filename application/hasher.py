import bcrypt


class Hasher:
    def hash_passwd(self, passwd: str) -> str:
        arr = passwd.encode("utf-8")
        hashed = bcrypt.hashpw(arr, bcrypt.gensalt())
        return hashed.decode("utf-8")

    def compare_hash_and_passwd(self, hash: str, passwd: str) -> bool:
        return bcrypt.checkpw(passwd.encode("utf-8"), hash.encode("utf-8"))
