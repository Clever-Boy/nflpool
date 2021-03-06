from nflpool.data.dbsession import DbSessionFactory
from nflpool.data.account import Account
from nflpool.data.player_picks import PlayerPicks
from nflpool.data.teaminfo import TeamInfo
from nflpool.data.conferenceinfo import ConferenceInfo
from nflpool.data.divisioninfo import DivisionInfo
from nflpool.data.activeplayers import ActiveNFLPlayers
from sqlalchemy import and_


class ViewPicksService:
    @classmethod
    def get_account_info(cls, user_id):
        session = DbSessionFactory.create_session()

        account_info = session.query(Account).filter(Account.id == user_id).all()

        return account_info

    @classmethod
    def seasons_played(cls, user_id):
        session = DbSessionFactory.create_session()

        seasons_played = (
            session.query(PlayerPicks.season)
            .distinct(PlayerPicks.season)
            .filter(Account.id == user_id)
        )

        return seasons_played

    @staticmethod
    def display_picks(user_id, season):

        session = DbSessionFactory.create_session()

        picks_query = (
            session.query(
                PlayerPicks.pick_type,
                ConferenceInfo.conference,
                DivisionInfo.division,
                TeamInfo.name,
                PlayerPicks.rank,
                ActiveNFLPlayers.firstname,
                ActiveNFLPlayers.lastname,
                PlayerPicks.multiplier,
            )
            .outerjoin(ConferenceInfo)
            .outerjoin(DivisionInfo)
            .outerjoin(TeamInfo)
            .outerjoin(
                ActiveNFLPlayers,
                and_(
                    PlayerPicks.player_id == ActiveNFLPlayers.player_id,
                    PlayerPicks.season == ActiveNFLPlayers.season,
                ),
            )
            .filter(PlayerPicks.user_id == user_id, PlayerPicks.season == season)
            .all()
        )

        return picks_query

    @staticmethod
    def change_picks(user_id, season):

        session = DbSessionFactory.create_session()

        picks_query = (
            session.query(
                PlayerPicks.pick_type,
                ConferenceInfo.conference,
                DivisionInfo.division,
                TeamInfo.name,
                PlayerPicks.rank,
                TeamInfo.team_id,
                PlayerPicks.rank,
                DivisionInfo.division_id,
                ConferenceInfo.conf_id,
                ActiveNFLPlayers.firstname,
                ActiveNFLPlayers.lastname,
                PlayerPicks.multiplier,
                PlayerPicks.player_id,
            )
            .outerjoin(ConferenceInfo)
            .outerjoin(DivisionInfo)
            .outerjoin(TeamInfo)
            .outerjoin(
                ActiveNFLPlayers,
                and_(
                    PlayerPicks.player_id == ActiveNFLPlayers.player_id,
                    PlayerPicks.season == ActiveNFLPlayers.season,
                ),
            )
            .filter(PlayerPicks.user_id == user_id, PlayerPicks.season == season)
            .all()
        )

        return picks_query
