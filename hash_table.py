"""CSC 225 - Hash table starter. Complete the TODO sections."""

# These prime sizes are provided; you do not need to test for prime numbers.
SIZES = [11, 23, 47, 97, 197, 397]

# Maximum load factor allowed for each collision method.
LIMITS = {"linear": 0.70, "quadratic": 0.50, "chaining": 0.75}


class HashTable:
    def __init__(self, method="linear", hash_method="mod"):
        self.method = method           # linear, quadratic, or chaining
        self.hash_method = hash_method # mod or digit
        self.capacity = 11
        self.count = 0

        if method == "chaining":
            # Each position must have its OWN list.
            # [[]] * 11 would repeat references to the SAME list.
            self.table = [[] for i in range(self.capacity)]
        else:
            self.table = [None] * self.capacity

    def hash_key(self, key):
        # These two hash functions are already provided.
        if self.hash_method == "mod":
            return key % self.capacity
        total = 0
        for digit in str(abs(key)):
            total += int(digit)
        return total % self.capacity

    def insert(self, key):
        # Milestone 1/2/3, TODO 1: do not insert a duplicate.
        if self.search(key):
            print("Duplicate:", key, "is already in the table.")
            return

        # TODO 2 (Milestone 4): resize BEFORE inserting if one more key
        # would push the load factor over the limit.
        if (self.count + 1) / self.capacity > LIMITS[self.method]:
            self.resize()

        # TODO 3: find the starting position and place the key.
        start = self.hash_key(key)

        if self.method == "chaining":
            self.table[start].append(key)
            self.count += 1          # TODO 4
            return

        for i in range(self.capacity):
            if self.method == "linear":
                index = (start + i) % self.capacity
            else:  # quadratic
                index = (start + i * i) % self.capacity

            if self.table[index] is None:
                self.table[index] = key
                self.count += 1      # TODO 4
                return

        # Every probe was occupied (can happen with quadratic probing).
        print("Could not insert", key, "- table is full.")

    def search(self, key):
        start = self.hash_key(key)

        if self.method == "chaining":
            return key in self.table[start]

        for i in range(self.capacity):
            if self.method == "linear":
                index = (start + i) % self.capacity
            else:  # quadratic
                index = (start + i * i) % self.capacity

            if self.table[index] is None:
                return False         # empty slot: key cannot be further along
            if self.table[index] == key:
                return True

        return False                 # tried capacity positions

    def resize(self):
        # 1. Save the old table.
        old_table = self.table

        # 2. Move to the next capacity in SIZES.
        position = SIZES.index(self.capacity)
        if position + 1 >= len(SIZES):
            print("Table is already at the largest size.")
            return
        self.capacity = SIZES[position + 1]

        # 3. Make a new empty table of the correct kind.
        if self.method == "chaining":
            self.table = [[] for i in range(self.capacity)]
        else:
            self.table = [None] * self.capacity

        # 4. Reset count (insert() will rebuild it).
        self.count = 0

        # 5. Re-insert every old value using insert().
        if self.method == "chaining":
            for chain in old_table:
                for value in chain:
                    self.insert(value)
        else:
            for value in old_table:
                if value is not None:
                    self.insert(value)

    def show(self):
        print("\nMethod:", self.method, "| Hash:", self.hash_method)
        print("Size:", self.capacity, "| Values:", self.count)
        print("Load factor:", round(self.count / self.capacity, 2))
        for i in range(self.capacity):
            print(i, ":", self.table[i])  