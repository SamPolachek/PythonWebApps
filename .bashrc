echo 'Loading settings for BACS350'

alias l='ls -al'

alias s='git status'

alias pull='git pull'

alias dj='python manage.py'

alias u='d ..'

function d {
    cd $1 && l
}

export p=~/BACS350/week4/Superhero

cd $p

ls -al

echo "Activate environment .venv"
workon .venv