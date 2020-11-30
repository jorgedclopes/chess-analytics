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
**Structure**

* The requirements file has the necessary dependencies to run the project.
* The py files have the functions to process the games.
* Jupyter files are used for any graphical output.
* A makefile will be made at some point in the future.

---
**Findings/Limitations**

* Games with clocks are only available for games after March/May 2017.