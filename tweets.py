import my_markov
import twitter
import os
import sys

chains = {}
input_text = ""
for arg in sys.argv[2:]:
    input_path = arg

    # Open the file and turn it into one long string
    input_text = my_markov.open_and_read_file(input_path)

    # Get a Markov chain
    chains = my_markov.make_chains(input_text, int(sys.argv[1]), chains)


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                      consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                      access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
                      access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    api.PostUpdate(my_markov.make_text(chains))

tweet(chains)
