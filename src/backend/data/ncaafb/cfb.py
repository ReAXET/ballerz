import sportsdataverse as sdv


def get_cfb_data():
    print("Getting CFB data with sdv.cfb.espn_cfb_teams()")
    print("Load cfb teams ID info and logo")
    cfb_espn_teams = sdv.cfb.espn_cfb_teams()
    print("Load cfb teams")
    