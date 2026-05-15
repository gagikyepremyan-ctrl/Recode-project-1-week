import argparse
import json
import os
from json.decoder import JSONDecodeError


def has_cycle(temp_list):
    adj = {int(s.get('index')): [int(d) for d in s.get('deps', []) if str(d).isdigit()] for s in temp_list if
           s.get('index') is not None}
    visited = set()
    path = set()

    def visit(n):
        if n in path: return True
        if n in visited: return False
        path.add(n)
        for neighbor in adj.get(n, []):
            if visit(neighbor): return True
        path.remove(n)
        visited.add(n)
        return False

    for node in adj:
        if visit(node): return True
    return False


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name")
    add_parser.add_argument("duration", type=int)
    add_parser.add_argument("deps", nargs="+")
    add_parser.add_argument("--output", default="data.json")

    subparsers.add_parser("remove").add_argument("index", type=int)
    subparsers.add_parser("list")
    subparsers.add_parser("total-time")
    subparsers.add_parser("parallel")
    subparsers.add_parser("order")

    edit_parser = subparsers.add_parser("edit", help="Edit an existing step")
    edit_parser.add_argument("index", type=int, help="ID of the step to edit")
    edit_parser.add_argument("--name", help="New name for the step")
    edit_parser.add_argument("--duration", type=int, help="New duration")
    edit_parser.add_argument("--deps", nargs="*", help="New dependencies")
    args = parser.parse_args()
    output_file = "data.json"
    if hasattr(args, 'output'):
        output_file = args.output

    if args.command == "add":
        recipe_list = []
        if os.path.exists(output_file):
            try:
                with open(output_file, "r") as f:
                    recipe_list = json.load(f)
            except JSONDecodeError:
                recipe_list = []

        if args.duration <= 0:
            print("Error: duration must be positive")
            return

        if any(s.get('name', '').lower() == args.name.lower() for s in recipe_list):
            print(f"Error: step {args.name} already exists")
            return

        existing_ids = [s.get('index') for s in recipe_list if s.get('index') is not None]
        clean_deps = []
        for d in args.deps:
            if d.lower() == "none": continue
            if not d.isdigit() or int(d) not in existing_ids:
                print(f"Error: dependency ID {d} does not exist")
                return
            clean_deps.append(int(d))

        new_index = max(existing_ids, default=0) + 1
        new_step = {
            "index": new_index,
            "name": args.name,
            "duration": args.duration,
            "deps": clean_deps
        }

        if has_cycle(recipe_list + [new_step]):
            print("Error: circular dependency detected")
            return

        recipe_list.append(new_step)
        with open(output_file, "w") as f:
            json.dump(recipe_list, f, indent=4)
        print(f"Added {args.name} as ID {new_index}")

    elif args.command == "list":
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                data = json.load(f)
                for s in data:
                    print(
                        f"ID: {s.get('index')} | Name: {s.get('name')} | Time: {s.get('duration')} | Deps: {s.get('deps')}")

    elif args.command == "remove":
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                data = json.load(f)
            new_data = [s for s in data if s.get('index') != args.index]
            with open(output_file, "w") as f:
                json.dump(new_data, f, indent=4)
            print(f"Removed ID {args.index}")

    elif args.command == "order":
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                recipe_list = json.load(f)
            steps = {s['index']: s for s in recipe_list if 'index' in s}
            in_degree = {i: 0 for i in steps}
            adj = {i: [] for i in steps}
            for i, s in steps.items():
                for d in s.get('deps', []):
                    if d in adj:
                        adj[d].append(i)
                        in_degree[i] += 1
            queue = sorted([i for i in in_degree if in_degree[i] == 0])
            order = []
            while queue:
                curr = queue.pop(0)
                order.append(curr)
                for neighbor in adj[curr]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0: queue.append(neighbor)
                queue.sort()
            print("Cooking Order:")
            for i, idx in enumerate(order, 1):
                print(f"{i}. {steps[idx]['name']}")

    elif args.command == "total-time":
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                recipe_list = json.load(f)
            if not recipe_list: return
            steps = {s['index']: s for s in recipe_list if 'index' in s}
            cache = {}

            def get_time(idx):
                if idx in cache: return cache[idx]
                s = steps[idx]
                d_times = [get_time(d) for d in s.get('deps', []) if d in steps]
                cache[idx] = s['duration'] + (max(d_times) if d_times else 0)
                return cache[idx]

            total = max([get_time(i) for i in steps]) if steps else 0
            print(f"Total Parallel Time: {total} minutes")

    elif args.command == "parallel":
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                recipe_list = json.load(f)
            steps = {s['index']: s for s in recipe_list if 'index' in s}
            completed, waves, remaining = set(), [], list(steps.keys())
            while remaining:
                wave = [i for i in remaining if all(d in completed for d in steps[i].get('deps', []))]
                if not wave: break
                waves.append(wave)
                for i in wave:
                    completed.add(i)
                    remaining.remove(i)
            for i, w in enumerate(waves, 1):
                names = [steps[idx]['name'] for idx in w]
                print(f"Wave {i}: {', '.join(names)}")
    elif args.command == "edit":
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                recipe_list = json.load(f)
            step_to_edit = next((s for s in recipe_list if s.get('index') == args.index), None)

            if not step_to_edit:
                print(f"Error: Step ID {args.index} not found.")
                return
            if args.name:
                step_to_edit['name'] = args.name
            if args.duration is not None:
                if args.duration <= 0:
                    print("Error: Duration must be positive.")
                    return
                step_to_edit['duration'] = args.duration
            if args.deps is not None:
                existing_ids = [s.get('index') for s in recipe_list]
                clean_deps = [int(d) for d in args.deps if d.isdigit() and int(d) in existing_ids]
                old_deps = step_to_edit['deps']
                step_to_edit['deps'] = clean_deps

                if has_cycle(recipe_list):
                    print("Error: Circular dependency detected with these new deps!")
                    step_to_edit['deps'] = old_deps
                    return

            # 3. Save the updated list
            with open(output_file, "w") as f:
                json.dump(recipe_list, f, indent=4)


if __name__ == "__main__":
    main()