import sys


class KnapsackSolver:
    def __init__(self, max_capacity, accuracy):
        self.max_capacity = max_capacity
        self.accuracy = accuracy
        self.items = []
        self.scaled_items = []
        self.selected_items = []
        self.result_ves = 0
        self.result_value = 0

    def add_item(self, wei, value, index):
        self.items.append({"wei": wei, "value": value, "index": index})

    def scale_items(self):
        max_value = max(item["value"] for item in self.items)
        if self.accuracy > 0:
            k = -(-self.accuracy * max_value // (len(self.items) * (1 + self.accuracy)))
        else:
            k = 1  

        self.scaled_items = [
            {
                "scaled_value": item["value"] if k <= 1 else item["value"] // k,
                "wei": item["wei"],
                "index": item["index"],
            } for item in self.items
        ]

    def calculater(self):
        dec = {}
        dec[0] = {"wei": 0, "items": []}  # Начальное состояние

        for item in self.scaled_items:
            current_states = list(dec.items())
            for value, data in current_states:
                new_value = value + item["scaled_value"]
                new_wei = data["wei"] + item["wei"]

                if new_wei <= self.max_capacity:
                    new_items = data["items"] + [item["index"]]
                    if new_value not in dec or dec[new_value]["wei"] > new_wei:
                        dec[new_value] = {"wei": new_wei, "items": new_items}

        valid_values = [value for value in dec if dec[value]["wei"] <= self.max_capacity]
        best_value = max(valid_values) if valid_values else 0

        if best_value in dec:
            result = dec[best_value]
            self.result_ves = result["wei"]
            self.result_value = sum(self.items[i - 1]["value"] for i in result["items"])
            self.selected_items = sorted(result["items"])

    def solve(self):
        self.scale_items()
        self.calculater()
        return self.result_ves, self.result_value, self.selected_items


def main():
    input_data = sys.stdin.read().strip().splitlines()

    if not input_data:
        print("error")
        return

    try:
        accuracy = float(input_data[0])
        if accuracy < 0 or accuracy > 1:
            raise ValueError()
    except ValueError:
        print("error")
        return

    try:
        max_capacity = int(input_data[1])
        if max_capacity < 0:
            raise ValueError()
    except ValueError:
        print("error")
        return

    items_data = input_data[2:]
    if not items_data:
        print("error")
        return

    knapsack_solver = KnapsackSolver(max_capacity, accuracy)

    for line in items_data:
        components = line.split()
        if len(components) != 2:
            print("error")
            return
        try:
            wei, value = map(int, components)
            if wei < 0 or value < 0:
                raise ValueError()
            knapsack_solver.add_item(wei, value, len(knapsack_solver.items) + 1)
        except ValueError:
            print("error")
            return

    if not knapsack_solver.items:
        print("error")
        return

    total_wei, total_value, selected_items = knapsack_solver.solve()

    print(f"{total_wei} {total_value}")
    for item_index in selected_items:
        print(item_index)


if __name__ == "__main__":
    main()
