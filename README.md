Something something Titanium API

# Setup
0. Set up a virtual environment if necessary (`python -m venv [path to venv]`) and activate it (`. [path to venv]/bin/activate`).
1. Install the dependencies (`dotenv` and `requests`) by either running `pip install -r requirements.txt` or installing them with your package manager.
2. If you're not placing the script where Titanium V2 is located, configure the `example.env` file according to Titanium V2's config if the default configuration for it wouldn't work and rename it to `.env`.
3. Run the script (`./api-cli.py` or `python3 api-cli.py`).
4. Run the `help` command.

# Limitations
- Anything that requires a `PUT` request (modifying configuration) is not supported.
- No shell completion or history (idk why you'd need those for something like this anyway).

# Special thanks
go check out [Titanium](https://github.com/RestartB/titanium) btw (Titanium V2 is on the v2 branch)