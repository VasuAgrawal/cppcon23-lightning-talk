import argparse
import pathlib

def ensurePathExists(path: str):
    p = pathlib.Path(path)
    if not p.exists():
        raise argparse.ArgumentError(f"{p} does not exist.")
    return p

parser = argparse.ArgumentParser(description="")
parser.add_argument("folder", nargs="+", help="folder name to analyze", type=ensurePathExists)
args = parser.parse_args()

import subprocess
import tqdm

def gitCheckout(arg, ref):
    error_chars = 0
    error_chars += len(subprocess.run(["git", "reset", "--hard", ref], cwd=str(arg), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, encoding="utf8").stderr)
    error_chars += len(subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=str(arg), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, encoding="utf8").stderr)
    return error_chars

def resetToMaster(arg: pathlib.Path):
    # for head in ["origin/master", "origin/main", "origin/dev", "origin/devel"]:
    for head in ["origin/HEAD"]:
        try:
            gitCheckout(arg, head)
            return
        except Exception as e:
            # pass
            print("Failed:", e)

    raise RuntimeError("failed to checkout master")


def processFolder(arg: pathlib.Path):
    resetToMaster(arg)

    parents = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=str(arg), check=True, capture_output=True, encoding="utf8")
    all_commits = list()
    for parent in parents.stdout.splitlines():
        commits = subprocess.run(["git", "rev-list", f"{parent}..HEAD"], cwd=str(arg), check=True, capture_output=True, encoding="utf8")
        all_commits.extend(commits.stdout.splitlines())

    step_size = max(len(all_commits) // 2000, 1)
    print(f"Total of {len(all_commits)} commits to parse in {arg}, using step size {step_size}")

    error_chars = 0
    with open(f"outputs/{arg.name}.txt", "w", encoding="utf8") as output:
        for commit in tqdm.tqdm(all_commits[::step_size], desc=arg.name):
            try:
                error_chars += gitCheckout(arg, commit)
            except subprocess.CalledProcessError as e:
                print(f"Unable to check out commit {commit} for repo {arg}, continuing anyway: {e}")
                continue

            metadata = subprocess.run("git show --format=%ct,%cI --quiet", cwd=str(arg), shell=True, check=True, capture_output=True, encoding="utf8").stdout.strip()
            constexpr_count = subprocess.run("git grep constexpr | wc -l", cwd=str(arg), shell=True, check=True, capture_output=True, encoding="utf8").stdout.strip()
            output.write(f"{metadata},{commit},{constexpr_count}\n")

    resetToMaster(arg)
    return error_chars


def main():
    for arg in args.folder:
        try:
            error_chars = processFolder(arg)
            if error_chars > 0:
                print(f"{arg} processing finished with {error_chars} errors")
        except Exception as e:
            print(f"{arg} failed with exception: {e}")


if __name__ == "__main__":
    main()
