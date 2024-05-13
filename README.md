# llm-finetuning-public

## Miniconda setup
If you are not familiar with Python and do not have python environment setup, it’s advised to use Miniconda environment. Instructions below.
 
* Download Miniconda installer from https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/. Select your operating system & architecture and installer for Python version 3.12.
* Launch the installer and follow instructions.
* Clone this repository.
* Open terminal and navigate to the repository root.
* Create a new conda environment with `conda create -n llm-finetuning-conda python pip`
* Activate the conda environment with `conda activate llm-finetuning-conda`.
* Check that you have the environment properly setup by `conda info —envs` and you should see asterix (*) next to your llm-finetuning-conda environment.
* Install the project requirements with `pip install -r requirements.txt`
* Open Jupyter with `jupyter-notebook tokenizer_example.ipynb` command
* Test that you can execute the notebook cells.


## Custom Python setup
Conda/miniconda is a convenient way to create environments but it’s not a requirement. If you are familiar with Python and have it already setup, you can use your own environments and ways of working. In that case make sure that 
* You have Python 3.12 available. For instance, tool pyenv can be used to manage multiple Python versions, see https://github.com/pyenv/pyenv.
* Make sure you have pip installed, see https://pip.pypa.io/en/stable/installation/.
* Clone this repository.
* Make sure you can install requirements.txt from the repository root. Advice way is to create a new virtual environment for the dependencies, that can be done with pyenv & venv & pip with
```
pyenv shell 3.12
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
* Make sure you can open Jupyter with `jupyter-notebook tokenizer_example.ipynb` command and execute the notebook cells.
