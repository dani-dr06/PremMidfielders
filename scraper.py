import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def scrape_player_stats(url: str):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Referer": "https://www.premierleague.com/"
    }

    try:

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Get the HTML content
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Join player first and last names
        player_name = (soup.find("div", class_="player-header__name-first").text.strip() +
                       " " + soup.find("div",class_="player-header__name-last").text.strip())

        appearances = soup.find("span", class_="allStatContainer js-all-stat-container statappearances").text.strip()

        # initialize a dict for the current row
        row = {"Player_Name": player_name, "Appearances": appearances}

        # find all stats and add them to the row dictionary
        player_stats = soup.findAll("div", class_="player-stats__stat-value")
        for stat in player_stats:
            stat = stat.text.split()
            stat_name, stat_value = " ".join(stat[:-1]), stat[-1]
            row[stat_name] = stat_value

        return row

    except:
        print(f"Failed to fetch HTML content from {url}")

if __name__ == '__main__':
    player_urls = {
        # Arsenal links
        "https://www.premierleague.com/players/11419/Martin-%C3%98degaard/stats",
        "https://www.premierleague.com/players/4936/Thomas-Partey/stats",
        "https://www.premierleague.com/players/14445/Emile-Smith-Rowe/stats",
        "https://www.premierleague.com/players/5682/Jorginho/stats",
        "https://www.premierleague.com/players/67631/F%C3%A1bio-Vieira/stats",
        "https://www.premierleague.com/players/15202/Declan-Rice/stats",
        "https://www.premierleague.com/players/10428/Ainsley-Maitland-Niles/stats",

        # Aston Villa
        "https://www.premierleague.com/players/24626/Douglas-Luiz/stats",
        "https://www.premierleague.com/players/51423/John-McGinn/stats",
        "https://www.premierleague.com/players/26408/Emiliano-Buend%C3%ADa/stats",
        "https://www.premierleague.com/players/5866/Leander-Dendoncker/stats",
        "https://www.premierleague.com/players/25067/Boubacar-Kamara/stats",
        "https://www.premierleague.com/players/19888/Jacob-Ramsey/stats",
        "https://www.premierleague.com/players/5865/Youri-Tielemans/stats"

        # Bournemouth
        "https://www.premierleague.com/players/10766/Lewis-Cook/stats",
        "https://www.premierleague.com/players/13706/David-Brooks/stats",
        "https://www.premierleague.com/players/15572/Ryan-Christie/stats",
        "https://www.premierleague.com/players/10580/Joe-Rothwell/stats",
        "https://www.premierleague.com/players/14846/Marcus-Tavernier/stats",
        "https://www.premierleague.com/players/3766/Junior-Stanislas/stats",
        "https://www.premierleague.com/players/63553/Hamed-Traor%C3%A8/stats",
        "https://www.premierleague.com/players/8882/Philip-Billing/stats",
        "https://www.premierleague.com/players/74976/Alex-Scott/stats"

        # Brentford
        "https://www.premierleague.com/players/42331/Christian-N%C3%B8rgaard/stats",
        "https://www.premierleague.com/players/49726/Mathias-Jensen/stats",
        "https://www.premierleague.com/players/127594/Kevin-Schade/stats",
        "https://www.premierleague.com/players/117497/Yoane-Wissa/stats",
        "https://www.premierleague.com/players/108612/Frank-Onyeka/stats",
        "https://www.premierleague.com/players/66360/Bryan-Mbeumo/stats",
        "https://www.premierleague.com/players/49731/Mikkel-Damsgaard/stats",
        "https://www.premierleague.com/players/24773/Shandon-Baptiste/stats",
        "https://www.premierleague.com/players/23194/Vitaly-Janelt/stats",
        "https://www.premierleague.com/players/128891/Yehor-Yarmoliuk/stats",
        "https://www.premierleague.com/players/127594/Kevin-Schade/stats",

        # Brighton
        "https://www.premierleague.com/players/8171/Solly-March/stats",
        "https://www.premierleague.com/players/22542/Pascal-Gro%C3%9F/stats",
        "https://www.premierleague.com/players/4618/Adam-Lallana/stats",
        "https://www.premierleague.com/players/108751/Jakub-Moder/stats",
        "https://www.premierleague.com/players/117732/Kaoru-Mitoma/stats",
        "https://www.premierleague.com/players/24221/Billy-Gilmour/stats",
        "https://www.premierleague.com/players/133430/Facundo-Buonanotte/stats",
        "https://www.premierleague.com/players/112739/Jack-Hinshelwood/stats",
        "https://www.premierleague.com/players/125827/Julio-Enciso/stats",
        "https://www.premierleague.com/players/2100/James-Milner/stats",
        "https://www.premierleague.com/players/124396/Carlos-Baleba/stats",

        # Chelsea
        "https://www.premierleague.com/players/63741/Enzo-Fern%C3%A1ndez/stats",
        "https://www.premierleague.com/players/53991/Mykhailo-Mudryk/stats",
        "https://www.premierleague.com/players/21887/Conor-Gallagher/stats",
        "https://www.premierleague.com/players/64140/Carney-Chukwuemeka/stats",
        "https://www.premierleague.com/players/112203/Mois%C3%A9s-Caicedo/stats",
        "https://www.premierleague.com/players/49293/Cole-Palmer/stats",
        "https://www.premierleague.com/players/75212/Cesare-Casadei/stats",
        "https://www.premierleague.com/players/99282/Rom%C3%A9o-Lavia/stats",

        # Crystal Palace
        "https://www.premierleague.com/players/32989/Michael-Olise/stats",
        "https://www.premierleague.com/players/21584/Eberechi-Eze/stats",
        "https://www.premierleague.com/players/8980/Jeffrey-Schlupp/stats",
        "https://www.premierleague.com/players/8589/Will-Hughes/stats",
        "https://www.premierleague.com/players/126670/Cheick-Doucour%C3%A9/stats",
        "https://www.premierleague.com/players/68086/Naouirou-Ahamada/stats",
        "https://www.premierleague.com/players/37776/Jefferson-Lerma/stats",

        # Everton
        "https://www.premierleague.com/players/108096/Amadou-Onana/stats",
        "https://www.premierleague.com/players/13823/Abdoulaye-Doucour%C3%A9/stats",
        "https://www.premierleague.com/players/12582/Idrissa-Gueye/stats",
        "https://www.premierleague.com/players/23841/James-Garner/stats",

        # Fulham
        "https://www.premierleague.com/players/4818/Harrison-Reed/stats",
        "https://www.premierleague.com/players/13961/Harry-Wilson/stats",
        "https://www.premierleague.com/players/3894/Tom-Cairney/stats",
        "https://www.premierleague.com/players/10476/Andreas-Pereira/stats",
        "https://www.premierleague.com/players/19858/Jo%C3%A3o-Palhinha/stats",
        "https://www.premierleague.com/players/16044/Sasa-Lukic/stats",

        # Leicester
        "https://www.premierleague.com/players/7488/Harry-Winks/stats",
        "https://www.premierleague.com/players/20479/Wilfred-Ndidi/stats",
        "https://www.premierleague.com/players/21413/Oliver-Skipp/stats",

        # Liverpool
        "https://www.premierleague.com/players/114296/Stefan-Bajcetic/stats",
        "https://www.premierleague.com/players/23815/Curtis-Jones/stats",
        "https://www.premierleague.com/players/33185/Harvey-Elliott/stats",
        "https://www.premierleague.com/players/63633/Alexis-Mac-Allister/stats",
        "https://www.premierleague.com/players/33231/Dominik-Szoboszlai/stats",
        "https://www.premierleague.com/players/43586/Wataru-Endo/stats",
        "https://www.premierleague.com/players/49909/Ryan-Gravenberch/stats",

        # Man City
        "https://www.premierleague.com/players/4260/Jack-Grealish/stats",
        "https://www.premierleague.com/players/16286/Rodri/stats",
        "https://www.premierleague.com/players/4288/Kevin-De-Bruyne/stats",
        "https://www.premierleague.com/players/5067/Bernardo-Silva/stats",
        "https://www.premierleague.com/players/14805/Phil-Foden/stats",
        "https://www.premierleague.com/players/12520/Mateo-Kovacic/stats",
        "https://www.premierleague.com/players/76204/Matheus-Nunes/stats",

        # Man Utd
        "https://www.premierleague.com/players/23396/Bruno-Fernandes/stats",
        "https://www.premierleague.com/players/4845/Christian-Eriksen/stats",
        "https://www.premierleague.com/players/5793/Casemiro/stats",
        "https://www.premierleague.com/players/14824/Scott-McTominay/stats",
        "https://www.premierleague.com/players/108936/Kobbie-Mainoo/stats",
        "https://www.premierleague.com/players/14580/Mason-Mount/stats",
        "https://www.premierleague.com/players/22744/Sofyan-Amrabat/stats",

        # Newcastle
        "https://www.premierleague.com/players/3934/Matt-Ritchie/stats",
        "https://www.premierleague.com/players/9662/Jacob-Murphy/stats",
        "https://www.premierleague.com/players/54312/Miguel-Almir%C3%B3n/stats",
        "https://www.premierleague.com/players/51593/Elliot-Anderson/stats",
        "https://www.premierleague.com/players/14897/Sean-Longstaff/stats",
        "https://www.premierleague.com/players/74761/Bruno-Guimar%C3%A3es/stats",
        "https://www.premierleague.com/players/14716/Harvey-Barnes/stats",

        # Nottingham Forest
        "https://www.premierleague.com/players/49738/Orel-Mangala/stats",
        "https://www.premierleague.com/players/15259/Morgan-Gibbs-White/stats",
        "https://www.premierleague.com/players/14238/Ryan-Yates/stats",
        "https://www.premierleague.com/players/112510/Danilo/stats",

        # Tottenham
        "https://www.premierleague.com/players/5272/Pierre-Emile-H%C3%B8jbjerg/stats",
        "https://www.premierleague.com/players/49316/Dejan-Kulusevski/stats",
        "https://www.premierleague.com/players/117318/Pape-Sarr/stats",
        "https://www.premierleague.com/players/22802/Rodrigo-Bentancur/stats",
        "https://www.premierleague.com/players/50245/Yves-Bissouma/stats",
        "https://www.premierleague.com/players/8456/James-Maddison/stats",
        "https://www.premierleague.com/players/19851/Giovani-Lo-Celso/stats",

        # West Ham
        "https://www.premierleague.com/players/25246/Pablo-Fornals/stats",
        "https://www.premierleague.com/players/55776/Lucas-Paquet%C3%A1/stats",
        "https://www.premierleague.com/players/25183/Tom%C3%A1s-Soucek/stats",
        "https://www.premierleague.com/players/40211/Edson-%C3%81lvarez/stats",
        "https://www.premierleague.com/players/4617/James-Ward-Prowse/stats",
        "https://www.premierleague.com/players/51364/Mohammed-Kudus/stats",

        # Wolves
        "https://www.premierleague.com/players/5583/Mario-Lemina/stats",
        "https://www.premierleague.com/players/117315/Boubacar-Traor%C3%A9/stats",
        "https://www.premierleague.com/players/133679/Jo%C3%A3o-Gomes/stats",
        "https://www.premierleague.com/players/24637/Tommy-Doyle/stats",
        "https://www.premierleague.com/players/126108/Jean-Ricner-Bellegarde/stats",
        "https://www.premierleague.com/players/19814/Pablo-Sarabia/stats",

    }

    df_rows = [] # list to contain rows in our dataframe

    for link in player_urls:
        new_row = scrape_player_stats(link)
        if new_row:
            df_rows.append(new_row)
        time.sleep(15) # wait 15 seconds before scraping again

    df = pd.DataFrame(df_rows)

    # Preprocess data

    # Some defensive stats are missing for attacking players (Mitoma)
    # therefore, we can fill in those values with 0s
    df.fillna(0, inplace=True)

    # A few stats are percentages and the values are string objects, including a % sign
    # let's remove the sign and make those values integers, as they do not contain decimals
    for col in df.columns:
        if "%" in col:
            df[col] = df[col].astype(str).str.replace("%", "").astype(int)


    obj_columns = df.select_dtypes(include='object').columns
    for col in obj_columns:
        df[col] = df[col].str.replace(",", "")

    df[['Appearances', 'Through balls',
        'Accurate long balls', 'Successful 50/50s', 'Aerial battles won',
        'Aerial battles lost', 'Errors leading to goal']]= df[['Appearances', 'Through balls',
        'Accurate long balls', 'Successful 50/50s', 'Aerial battles won',
        'Aerial battles lost', 'Errors leading to goal']].astype(int)

    # Done, now we can save our df as a csv

    # Save data to csv
    df.to_csv('data/notebook/Prem_player_stats.csv')