# configure openai apikey environment variable
# using mac latests versions
nano ~/.zshrc
export OPENAI_API_KEY='your-api-key'

### Instructions for development on a mac ###
# install rye to manage python and project dependencies
curl -sSf https://rye.astral.sh/get | bash

### Dependencies installed ###
rye add langchain
rye add langchain-openai
rye add langchain-community
rya add langchainhub
rye add duckduckgo-search
rye add wikipedia

# after adding a new dependency, execute to sync the virtual environment
rye sync

# execute examples
python travelAgent.py