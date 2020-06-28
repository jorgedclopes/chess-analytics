## chess-analytics

This project has the intention of analysing the history of a player and draw some conclusions on the person's play style.
One of the objectives is to find where the player can improve.

---

**Setup**

To run this project it is necessary to set PYTHONPATH to include the project folder.
You can run the following command on the root directory of the project
(change this command if `PYTHONPATH` is already defined):

```
export PYTHONPATH=$(pwd)
```

This project is still under development.
At this point it downloads a set of games from a lichess account into a folder of jsons or pgns.

* There is no analysis done at this point.

---
**Project Structure**

* The requirements file has the necessary dependencies to run the project.
* The py files have the functions to process the games.
* Jupyter files are used for any graphical output.
* A makefile will be made at some point in the future.

---
**PGN structure**

It is necessary to unify the PGN import format. The games are to be imported as a list of dictionaries.
Each of the games should have the fields
* White
* Black
* ECO
* UTC Date and Time (to be unified)
* White ELO
* Black ELO
* Time Control
* Termination (to be unified)
* Move List

Fields to be unified should be taken care of, later... Dictionaries can have other optional fields, originally from the raw data from some specific source. Examples of this are games from lichess or chess.com, that have different formats. 