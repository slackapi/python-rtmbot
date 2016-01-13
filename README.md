starter-python-bot
=============

## Overview
A simple starting point for creating a Beep Boop hostable, Python based Slack bot.

Visit [Beep Boop](https://beepboophq.com/docs/article/overview) to get the scoop on the the Beep Boop hosting platform. The Slack API documentation can be found [here](https://api.slack.com/).

## Assumptions
* You have already signed up with [Beep Boop](https://beepboophq.com) and have a local fork of this project.
* You have sufficient rights in your Slack team to configure a bot and generate/access a Slack API token.

## Usage

### Run locally
Install dependencies ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)

  pip install -r requirements.txt
	export SLACK_TOKEN=<YOUR SLACK TOKEN>; python rtmbot.py

Things are looking good if the console prints something like:

	Connected <your bot name> to <your slack team> team at https://<your slack team>.slack.com.

If you want additional logging and debugging info, prepend `export DEBUG=True; ` to the `python rtmbot.py` command.

### Run locally in Docker
	docker build -t starter-python-bot .
	docker run --rm -it -e SLACK_TOKEN=<YOUR SLACK API TOKEN> starter-python-bot

### Run in BeepBoop
If you have linked your local repo with the Beep Boop service (check [here](https://beepboophq.com/0_o/my-projects)), changes pushed to the remote master branch will automatically deploy.

## Acknowledgements

This code was forked from https://github.com/slackhq/python-rtmbot and utilizes the awesome https://github.com/slackhq/python-slackclient project by [@rawdigits](https://github.com/rawdigits).  Please see https://github.com/slackhq/python-rtmbot/blob/master/README.md for
a description about the organization of this code and using the plugins architecture.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
