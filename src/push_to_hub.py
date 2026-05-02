from datasets import load_dataset, DatasetDict
import datasets

for config_name, train_path, dev_path in [
    ("trace_derived",
     "tenacious_bench_v0.1/train/trace_derived_tasks.jsonl",
     "tenacious_bench_v0.1/dev/trace_derived_tasks.jsonl"),
    ("programmatic",
     "tenacious_bench_v0.1/train/programmatic_tasks.jsonl",
     "tenacious_bench_v0.1/dev/programmatic_tasks.jsonl"),
    ("synthetic",
     "tenacious_bench_v0.1/train/synthetic_tasks.jsonl",
     "tenacious_bench_v0.1/dev/synthetic_tasks.jsonl"),
    ("hand_authored",
     "tenacious_bench_v0.1/train/hand_authored_tasks.jsonl",
     None),
]:
    splits = {"train": datasets.load_dataset("json", data_files=train_path, split="train")}
    if dev_path:
        splits["dev"] = datasets.load_dataset("json", data_files=dev_path, split="train")
    DatasetDict(splits).push_to_hub("Nebiyou21/tenacious-bench-v0.1", config_name=config_name)
    print(f"{config_name} config pushed.")

prefs = DatasetDict({
    "train": datasets.load_dataset("json", data_files="tenacious_bench_v0.1/train/orpo_preferences.jsonl", split="train"),
})
prefs.push_to_hub("Nebiyou21/tenacious-bench-v0.1", config_name="orpo_preferences")
print("orpo_preferences config pushed.")
print("All done.")
