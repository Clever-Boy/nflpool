import requests
from nflpool.data.dbsession import DbSessionFactory
from nflpool.data.activeplayers import ActiveNFLPlayers
import nflpool.data.secret as secret
from requests.auth import HTTPBasicAuth
from nflpool.data.seasoninfo import SeasonInfo


class ActivePlayersService:
    @classmethod
    def add_active_nflplayers(cls, season: int, team_id: int, firstname: str, lastname: str,
                              position: str, player_id: int):

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        response = requests.get('https://api.mysportsfeeds.com/v1.1/pull/nfl/' + season +
                                '-regular/active_players.json',
                                auth=HTTPBasicAuth(secret.msf_username, secret.msf_pw))

        player_info = response.json()
        player_list = player_info["activeplayers"]["playerentry"]

        for players in player_list:
            try:
                firstname = (players["player"]["FirstName"])
                lastname = (players["player"]["LastName"])
                player_id = (players["player"]["ID"])
                team_id = (players["team"]["ID"])
                position = (players["player"]["Position"])
            except KeyError:
                continue

            # TODO Update season='2017' below to a variable

            active_players = ActiveNFLPlayers(firstname=firstname, lastname=lastname, player_id=player_id,
                                              team_id=team_id, position=position, season=season)

            session.add(active_players)

            session.commit()
