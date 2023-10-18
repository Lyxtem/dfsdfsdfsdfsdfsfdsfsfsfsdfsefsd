# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import fileio

RESOURCES_FOLDER_PATH = "./resources"
RESULTS_FOLDER_PATH = "./results"

PROXIES_FILE_PATH = RESOURCES_FOLDER_PATH + "/proxies.txt"
COSMETIC_IDS_FILE_PATH = RESOURCES_FOLDER_PATH + "/cosmetic_ids.json"

FORTNITE_IOS_CLIENT_ID = "3446cd72694c4a4485d81b77adbb2141"
FORTNITE_IOS_CLIENT_SECRET = "9209d4a5e25a457fb9b07489d313b41a"

ACCOUNT_PUBLIC_SERVICE_URL = "https://account-public-service-prod.ol.epicgames.com/account/api"
MCP_URL = "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile"

OAUTH_URL = ACCOUNT_PUBLIC_SERVICE_URL + "/oauth/token"
PUBLIC_ACCOUNT_URL = ACCOUNT_PUBLIC_SERVICE_URL + "/public/account"
EXTERNAL_AUTH_URL = PUBLIC_ACCOUNT_URL + "/lookup/externalAuth"

COSMETIC_IDS = fileio.read_json(COSMETIC_IDS_FILE_PATH)