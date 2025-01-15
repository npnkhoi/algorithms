from train import train
import argparse
import json

if __name__ == "__main__":
    all_results = {}
    for k in [2, 8, 32, 128]:
        for r in [0.05, 0.2]:
            args = argparse.Namespace(**{
                "model_type": "forest",
                "n_components": k,
                "hidden_rate": r,
                "n_samples": 1,
                "eval_set": "valid",
                "dataset": "first"
            })

            print(f"k={k}, r={r}")  
            results = train(args)
            print(f"results:\n{results}")
            all_results[f"{k}-{r}"] = results

    json.dump(
        all_results,
        open("all_results.json", "w")
    )
