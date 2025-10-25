import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item):
        hashes = []
        for i in range(self.num_hashes):
            hash_result = hashlib.md5((item + str(i)).encode()).hexdigest()
            index = int(hash_result, 16) % self.size
            hashes.append(index)
        return hashes

    def add(self, item):
        if not isinstance(item, str) or item == "":
            return
        for index in self._hashes(item):
            self.bit_array[index] = 1

    def __contains__(self, item):
        if not isinstance(item, str) or item == "":
            return False
        return all(self.bit_array[index] for index in self._hashes(item))


def check_password_uniqueness(bloom_filter, password_list):
    results = {}
    for password in password_list:
        if not isinstance(password, str) or password == "":
            results[password] = "некоректний пароль"
            continue
        if password in bloom_filter:
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None, 12345]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
