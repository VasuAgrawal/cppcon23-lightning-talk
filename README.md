# CppCon 2023 Lightning Talk Repo

See [this blog post](https://vasuagrawal.com/2023/10/making-friends-with-cuda-programmers/) for more details.

## Disclaimer

Unfortuntely, VSCode seems to not automatically save Jupyter notebooks when you run them, so the `combine_outputs.ipynb` file is empty. Same goes for the `notes.md` file - VSCode doesn't prompt me (at least by default) to save any files when I close it, as I guess it'll just hold on to the buffer in its own memory somewhere. This might work fine for local use, but it doesn't play nicely with SSH remote connections, where the PC on the other end might not exist later (in the case of ephemeral servers, like what I used here).

In other words, the only useful bit of code here is the `constexpr.py` script.

## Usage

First, clone any repos you want, likely into a subfolder. I used a `cloned_repos` subfolder. Some examples:
* [GCC](https://github.com/gcc-mirror/gcc)
* [TensorFlow](https://github.com/tensorflow/tensorflow)
* [OpenCV](https://github.com/opencv/opencv)
* etc (see `outputs` folder for more repo names)

Then, run the `constexpr.py` script:

```bash
# See usage
$ constexpr.py --help

# Run on everything in your cloned_repos folder
$ constexpr.py cloned_repos/*

# Or just a couple repos to test with
$ constexpr.py cloned_repos/gcc cloned_repos/tensorflow
```

All of the output will be saved to an `outputs` folder in this repo. This **folder must exist beforehand**, so create it yourself.

This would be the part where I'd say use the `combine_outputs.ipynb` notebook to merge the various outputs into a single CSV, but as noted above the script is gone. Take my word for it that the only thing happening in the script was merging some columns together, and converting unix times to fractional years. There's no data manipulation going on. The merged outputs are linked in the blog post, anyway, and in `combined2k.csv`.
