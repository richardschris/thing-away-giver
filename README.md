# thing-away-giver
A small web app for allocating things you're giving away

## Installing

It is only tested with Python 3.4. A standard setup will need either WSGI or Passenger config files; they are simple, but may vary based on host. You'd want to do the following to create your virtualenv (changing paths as you need to).

`cd ~
virtualenv --python=python3.4 pyenv
source pyenv/bin/activate
pip install flask`

## Using

The app expects an SQLite database with the following columns

1: title (text)
2: author (text)
3: id (integer)
4: claimed (integer)
5: claimedby (text)

The most important is the 'claimed' column. This governs the behavior of the pages. If `claimed == 0`, then it will appear on the main page (at the root of the directory you set for the app). If `claimed == 1`, then it will appear on the `/view_results` page. Finally, once you actually give it away, you can check the items on the `/view_results` page and click "Book Given", which sets `claimed = 2`. If `claimed == 2`, then it is pushed to the bottom of the page and struck through. You can also remove any submissions by checking the boxes and clicking "Remove Submission" on the `/view_results` page.

A simple, straightforward way to refactor the code would be to build an object model for the data, rather than getting the raw SQL data in each of the view functions. But, for the simple purposes of this app, it does the job. In any event, it is easy to modify.
