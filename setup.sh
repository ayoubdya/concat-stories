PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
printf "${PURPLE}instagram setup initialized ...${NC}\n"
git clone https://github.com/armm29393/PyInstaStories.git instagram
cd instagram
python -m venv venv
source venv/bin/activate
pip install git+https://git@github.com/ping/instagram_private_api.git@1.6.0 psutil
deactivate
cd ..
printf "${PURPLE}instagram setup done${NC}\n\n"

printf "${YELLOW}snapchat setup initialized ...${NC}\n"
mkdir snapchat && cd snapchat/
python -m venv venv
source venv/bin/activate
pip install snapchat-dl
deactivate
cd ..
printf "${YELLOW}snapchat setup done${NC}\n"
