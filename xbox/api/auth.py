# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import requests
import random
import utils

from urllib.parse import (
    urlencode,
    urlsplit,
    parse_qs
)

from typing import Union

from xbox.models.account import Account
from xbox.models.login_parameters import LoginParameters


def try_account_reauth(account: Account) -> bool:
    print(f"\n\nREAUTHORIZING...\n\n")
    new_account = do_account_auth(account.email, account.password)
    if new_account is None:
        return False

    account = new_account
    return True

def do_account_auth(
    email: str,
    password: str
) -> Union[Account, None]:
    account = Account(email, password)

    with requests.Session() as session:
        # Access & refresh tokens are required for getting
        # security and user tokens.
        if not __do_xbox_account_login(session, account):
            return

        # A security token is required for friends list lookup
        if not __do_get_security_token(session, account):
            return

        return account

#region Live Authentication
def __do_xbox_account_login(
    session: requests.Session,
    account: Account
):
    parameters = __get_login_parameters(session)
    if parameters is None:
        return

    successful_login = __xbox_account_login(session, parameters, account)
    return successful_login

def __get_login_parameters(
    session: requests.Session
) -> Union[LoginParameters, None]:
    query = urlencode({
        "client_id": "0000000048093EE3",
        "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
        "response_type": "token",
        "display": "touch",
        "scope": "service::user.auth.xboxlive.com::MBI_SSL",
        "locale": "en"
    })

    url = "https://login.live.com/oauth20_authorize.srf?" + query
    with session.get(url) as resp:
        src = resp.text

        # Get required parameters for live login
        flow_token = utils.get_inner_substring(src, "PPFT\" id=\"i0327\" value=\"", "\"")
        url_post = utils.get_inner_substring(src, "urlPost:'", "'")

        if utils.is_none_or_empty(flow_token, url_post):
            return

        parameters = LoginParameters(flow_token, url_post)
        return parameters

def __xbox_account_login(
    session: requests.Session,
    parameters: LoginParameters,
    account: Account
) -> bool:
    form_data = urlencode({
        "i13": "1",
        "login": account.email,
        "loginfmt": account.email,
        "type": "11",
        "LoginOptions": "1",
        "lrt": "",
        "lrtPartition": "",
        "hisRegion": "",
        "hisScaleUnit": "",
        "passwd": account.password,
        "ps": "2",
        "psRNGCDefaultType": "",
        "psRNGCEntropy": "",
        "psRNGCSLK": "",
        "canary": "",
        "ctx": "",
        "hpgrequestid": "",
        "PPFT": parameters.flow_token,
        "PPSX": "Passport",
        "NewUser": "1",
        "FoundMSAs": "",
        "fspost": "0",
        "i21": "0",
        "CookieDisclosure": "0",
        "IsFidoSupported": "1",
        "isSignupPost": "0",
        "i19": str(random.randint(10000, 99999))
    })

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Attempt login. We disable redirects because the access & refresh tokens
    # will be in the `Location` header.
    url = parameters.url_post
    with session.post(url, headers=headers, data=form_data, allow_redirects=False) as resp:
        if "Location" not in resp.headers:
            return False

        # Login has succeeded
        location = resp.headers["Location"]

        # The access and refresh tokens are
        # located in the redirect url's fragment
        fragment = urlsplit(location).fragment
        parsed_fragment = parse_qs(fragment)

        # Redundant check to prevent errors
        if "access_token" not in parsed_fragment:
            return False

        access_token = parsed_fragment["access_token"][0]
        refresh_token = parsed_fragment["refresh_token"][0]

        account.access_token = access_token
        account.refresh_token = refresh_token

        return True
#endregion

#region 2.0 Authentication
def __do_get_security_token(
    session: requests.Session,
    account: Account
) -> bool:
    for _ in range(3):
        if __get_security_token(session, account):
            return True

    return False

def __get_security_token(
    session: requests.Session,
    account: Account
) -> bool:
    headers = {
        "Authorization": account.live_id,
        "Content-Type": "application/soap+xml"
    }

    xml_data = """<s:Envelope
        xmlns:s='http://www.w3.org/2003/05/soap-envelope'
        xmlns:a='http://www.w3.org/2005/08/addressing'>
        <s:Header>
            <a:Action s:mustUnderstand='1'>http://docs.oasis-open.org/ws-sx/ws-trust/200512/RST/Issue</a:Action>
            <a:MessageID>urn:uuid:65a489e9-bada-45f8-bbb6-7ee616139525</a:MessageID>
            <a:ReplyTo>
                <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
            </a:ReplyTo>
            <a:To s:mustUnderstand='1'>http://activeauth.xboxlive.com//XSts/xsts.svc/IWSTrust13</a:To>
        </s:Header>
        <s:Body>
            <trust:RequestSecurityToken
                xmlns:trust='http://docs.oasis-open.org/ws-sx/ws-trust/200512'>
                <wsp:AppliesTo
                    xmlns:wsp='http://schemas.xmlsoap.org/ws/2004/09/policy'>
                    <EndpointReference
                        xmlns='http://www.w3.org/2005/08/addressing'>
                        <Address>http://xboxlive.com</Address>
                    </EndpointReference>
                </wsp:AppliesTo>
                <trust:KeyType>http://docs.oasis-open.org/ws-sx/ws-trust/200512/Bearer</trust:KeyType>
                <trust:RequestType>http://docs.oasis-open.org/ws-sx/ws-trust/200512/Issue</trust:RequestType>
                <trust:TokenType>http://docs.oasis-open.org/wss/oasis-wss-saml-token-profile-1.1#SAMLV2.0</trust:TokenType>
            </trust:RequestSecurityToken>
        </s:Body>
    </s:Envelope>"""

    url = "https://activeauth.xboxlive.com/XSts/xsts.svc/IWSTrust13"
    with session.post(url, headers=headers, data=xml_data) as resp:
        if resp.status_code != 200:
            return False

        src = resp.text

        security_token = utils.get_inner_substring(src, ":RequestedSecurityToken>", "</trust")
        if security_token is None:
            return False

        account.security_token = security_token
        return True
#endregion
